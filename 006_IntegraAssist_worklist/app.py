'''
Bio Basic Inc. - Canada
Made by: Eduardo Reyes, Ph.D.
Contact: ed5reyes@outlook.com

Version: 3.0
Date: Aug 05, 2025
Notes: Added auto-well assignment and auto-sort by reaction
    number to the bulk mode. Implemented basic functionality to generate the
    validation table (Template 2 for sequencing), especially handy for pooled
    samples.
'''
###############################################################################

# Import the required libraries
import numpy as np
import pandas as pd
import streamlit as st

# Streamlit App setup
st.set_page_config(
    page_title="Worklist Automation",
    page_icon=":bar_chart:",
    layout="wide")
st.title("Create worklist for Integra liquid handler")
st.markdown("""<hr style="border: none; height: 5px; background-color: #444;">""", 
            unsafe_allow_html=True,
            )

# Make tabs for the options
bulk_mode_tab, single_entries_tab = st.tabs(["Bulk mode", "Single entries"])
st.markdown("""<hr style="border: none; height: 5px; background-color: #444;">""", 
            unsafe_allow_html=True,
            )

# Create initial plate layouts (used by all modes)
plate_rows = ['A','B','C','D','E','F','G','H']
plate_cols_48 = range(1, 7)
plate_wells_48 = [f"(#{r}{c})" for c in plate_cols_48 for r in plate_rows]
plate_cols_96 = range(1, 13)
plate_wells_96 = [f"(#{r}{c})" for c in plate_cols_96 for r in plate_rows]

################################## BULK MODE ####################################
with bulk_mode_tab:
    st.subheader("Bulk Mode")

    # Layout, first row for input widgets, second for output widgets
    bm_row1_col1, bm_row1_col2 = st.columns([1.15, 4])
    st.markdown("""<hr style="border: none; height: 5px; background-color: #444;">""", 
                unsafe_allow_html=True,
                )
    bm_row2_col1, bm_row2_col2 = st.columns([1.15, 4])

    # Show widgets for basic features
    with bm_row1_col1:
        # Basic required info
        bm_row1_col1_subcol1, bm_row1_col1_subcol2 = st.columns([1, 1], gap="medium")
        with bm_row1_col1_subcol1:
            bm_source_spot = st.selectbox("Source spot", 
                                            options=["A", "B", "C"], 
                                            index=1,
                                            )
        with bm_row1_col1_subcol2:
            bm_target_spot = st.selectbox("Target spot", 
                                            options=["A", "B", "C"], 
                                            index=2,
                                            )
        bm_transfer_volume = st.slider("Volume to transfer", 
                                        min_value=5, 
                                        max_value=200, 
                                        step=5, 
                                        value=85,
                                        )
        
        st.divider()
        
        # Additional features
        pool_checkbox = st.checkbox("Pool replicates", 
                                        value=True, 
                                        key="pool_replicates",
                                        )
        autowell_checkbox = st.checkbox("Auto-assign wells", 
                                            value=True, 
                                            key="auto_well",
                                            )
        autosort_checkbox = st.checkbox("Auto-sort by reaction number", 
                                            value=True, 
                                            key="auto_sort",
                                            )
        
        st.divider()
        
        # Buttons to create relevant docs
        bm_row1_col1_subcol3, bm_row1_col1_subcol4 = st.columns([1, 1], gap="small")
        with bm_row1_col1_subcol3:
            create_worklist = st.button("Create worklist", type="primary")
        with bm_row1_col1_subcol4:
            # The button is disabled if the worklist DF doesn't exist
            create_validation = st.button("Create validation", 
                                        type="primary", 
                                        disabled="bm_df" not in st.session_state,
                                        key="create_validation_button")

    # Create initial empty df
    bm_df_columns = ["Job_ID", 
                        "BBID", 
                        "Clone", 
                        "Vector_number", 
                        "Notes",
                        "Concentration",
                        "ratio_260_280",
                        "ratio_260_230",
                        "Seq_reactions",
                        "Seq_well",
                        ]
    bm_df = pd.DataFrame("", index=range(96), columns=bm_df_columns)

    # Show editable widget to accept input in a 96-well plate-like format
    with bm_row1_col2:
        st.caption("Paste up to 96 rows")
        bm_displayed_df = st.data_editor(bm_df, 
                                use_container_width=True, 
                                key="bm_displayed_df",
                                column_config={
                                    "Clone": None if not pool_checkbox else {},
                                    "Seq_well": None if autowell_checkbox else {},
                                    "Seq_reactions": None if not autosort_checkbox else {},
                                    }
                                )

    # Make the worklist when the button is pressed
    if create_worklist or "bm_df" in st.session_state:
        # 1. Filter for rows that the user actually filled in.
        active_df = bm_displayed_df.loc[
            (bm_displayed_df['Job_ID'].fillna('') != '') &
            (bm_displayed_df['Vector_number'].fillna('') != '')
        ].copy()

        # 2. If no valid rows, stop.
        if active_df.empty:
            if create_worklist: # Only show warning if button was clicked
                st.warning("Please fill in at least one row with both 'Job_ID' and 'Vector_number'.")
            st.stop()

        # 3. Handle Well Assignment and Pooling
        if autowell_checkbox:
            # --- AUTO-ASSIGN WELLS ---
            if pool_checkbox:
                # Auto-assign wells AND pool replicates
                assigned_wells = {}
                well_index = 0
                seq_well_values = []

                for i, row in active_df.iterrows():
                    clone_id = row.get("Clone")
                    clone_key = clone_id if pd.notna(clone_id) and clone_id != "" else f"__row_{i}"

                    if clone_key in assigned_wells:
                        seq_well_values.append(assigned_wells[clone_key])
                    else:
                        if well_index >= len(plate_wells_96):
                            st.error(f"Error: More than {len(plate_wells_96)} unique clone groups found. Cannot assign to a 96-well plate.")
                            st.stop()
                        assigned_well = plate_wells_96[well_index]
                        assigned_wells[clone_key] = assigned_well
                        seq_well_values.append(assigned_well)
                        well_index += 1
                active_df["Seq_well"] = seq_well_values
            else:
                # Auto-assign wells, NO pooling
                if len(active_df) > len(plate_wells_96):
                    st.error(f"Error: There are {len(active_df)} samples, but only {len(plate_wells_96)} wells available on the plate.")
                    st.stop()
                active_df["Seq_well"] = plate_wells_96[:len(active_df)]
        else:
            # --- MANUAL WELL ASSIGNMENT ---
            # Validation: Ensure Seq_well is filled
            if active_df['Seq_well'].isnull().any() or (active_df['Seq_well'] == '').any():
                st.error("Error: 'Auto-assign wells' is unchecked, but some rows are missing a 'Seq_well' value.")
                st.stop()

            if pool_checkbox:
                # Manual wells AND pool replicates
                # Validation: Check for consistency within clone groups
                inconsistent_clones = []
                # Filter out empty/NaN clones before grouping
                clones_to_check = active_df[active_df['Clone'].notna() & (active_df['Clone'] != '')]
                for clone_id, group in clones_to_check.groupby('Clone'):
                    if group['Seq_well'].nunique() > 1:
                        wells = ", ".join(group['Seq_well'].unique())
                        inconsistent_clones.append(f"Clone '{clone_id}' has conflicting wells: {wells}")
                
                if inconsistent_clones:
                    st.error("Error: 'Pool replicates' is checked, but there are inconsistencies in manual well assignments:\n\n" + "\n".join(inconsistent_clones))
                    st.stop()

        # 4. Handle Sorting (MOVED TO HERE)
        if autosort_checkbox:
            # Validation for sorting
            if active_df['Seq_reactions'].isnull().any() or (active_df['Seq_reactions'] == '').any():
                st.error("Error: 'Auto-sort' is checked, but some rows are missing a 'Seq_reactions' number.")
                st.stop()
            
            # Attempt to convert to numeric and check for errors
            numeric_reactions = pd.to_numeric(active_df['Seq_reactions'], errors='coerce')
            if numeric_reactions.isnull().any():
                st.error("Error: 'Auto-sort' is checked, but the 'Seq_reactions' column contains non-numeric values.")
                st.stop()

            # Ensure proper well sorting by converting to a categorical type
            active_df['Seq_well'] = pd.Categorical(active_df['Seq_well'], 
                                                    categories=plate_wells_96, 
                                                    ordered=True)

            # Perform the double sort
            active_df = active_df.sort_values(by=['Seq_reactions', 'Seq_well'], 
                                                ascending=[False, True]).reset_index(drop=True)
            
            # Convert Seq_well back to a string for a clean output
            active_df['Seq_well'] = active_df['Seq_well'].astype(str)

        # 5. Finalize the DataFrame for output
        # Add constant values from the UI
        active_df["Source_spot"] = bm_source_spot
        active_df["Target_spot"] = bm_target_spot
        active_df["Transfer_volume"] = bm_transfer_volume

        # Derive remaining columns for the automation string
        # Assumes sample format like T0618P2A1, where slicing gives the well
        active_df["Source_well"] = active_df["Vector_number"].str.slice(7)
        active_df["Target_well"] = active_df["Seq_well"].str.replace(r"[#\(\)]", "", regex=True)
        active_df["Automation_string"] = active_df.apply(
            lambda row: f"{row['Job_ID']};{row['Source_spot']};{row['Source_well']};{row['Target_spot']};{row['Target_well']};{row['Transfer_volume']}",
            axis=1
        )

        # Save the processed dataframe to session state for display
        st.session_state["bm_df"] = active_df

        # 6. Prepare for display and download
        # Get the updated df, keep only the automation string and rename column as the software utilises
        final_worklist2 = st.session_state["bm_df"]["Automation_string"]
        final_worklist2 = final_worklist2.rename("SampleID;SourceDeckPosition;SourceWell;TargetDeckPosition;TargetWell;TransferVolume [µl]")
        
        with bm_row2_col1:
            worklist2_name = st.text_input("Worklist Name", key="worklist2_name")
            download_worklist2 = st.download_button("Download Worklist", 
                                                    data=final_worklist2.to_csv(index=False), 
                                                    file_name=f"{worklist2_name}.csv", mime="text/csv", 
                                                    type="primary", key="download_worklist2")

        with bm_row2_col2:
            # Create a temporary DataFrame for display by dropping unwanted columns
            display_df = st.session_state["bm_df"].drop(columns=[
                "BBID", 
                "Notes", 
                "Concentration", 
                "ratio_260_280", 
                "ratio_260_230", 
                "Source_spot", 
                "Target_spot", 
                "Transfer_volume",
            ])
            st.dataframe(display_df, use_container_width=True)
            
    # Create the validation df only once we have generated a worklist
    if create_validation or "validation_df" in st.session_state:
        # Only create the DataFrame on the initial button click
        if create_validation and "bm_df" in st.session_state:
            st.session_state["validation_df"] = None # Reset previous validation df

            # Start with a copy of the final worklist DF
            validation_df = st.session_state["bm_df"].copy()
            
            # Define columns to keep
            validation_columns = ["Job_ID", "BBID", "Clone", "Vector_number", "Notes", 
                                "Concentration", "ratio_260_280", "ratio_260_230"]

            # --- Conditionally consolidate rows if pooling is enabled ---
            if st.session_state.get("pool_replicates", False):
                # Identify the first occurrence of each unique clone to maintain original order
                first_occurrence_order = validation_df.drop_duplicates(subset=["Clone"], keep="first")["Clone"]
                
                # Convert numeric columns to numeric types, coercing errors to NaN
                validation_df["Concentration"] = pd.to_numeric(validation_df["Concentration"], errors='coerce')
                validation_df["ratio_260_280"] = pd.to_numeric(validation_df["ratio_260_280"], errors='coerce')
                validation_df["ratio_260_230"] = pd.to_numeric(validation_df["ratio_260_230"], errors='coerce')

                # Consolidate by grouping and aggregating
                aggregated_df = validation_df.groupby("Clone").agg({
                    "Job_ID": "first",
                    "BBID": "first",
                    "Vector_number": lambda x: x.iloc[0] if len(x) == 1 else x.iloc[0] + "x" + str(len(x)),
                    "Notes": "first",
                    "Concentration": "mean",
                    "ratio_260_280": "mean",
                    "ratio_260_230": "mean",
                }).reset_index()

                # Reorder the consolidated DataFrame based on the original first occurrence
                aggregated_df['Clone'] = pd.Categorical(aggregated_df['Clone'], categories=first_occurrence_order, ordered=True)
                validation_df = aggregated_df.sort_values('Clone').reset_index(drop=True)
                
                # Round the mean values to 3 decimal places
                validation_df[["Concentration", "ratio_260_280", "ratio_260_230"]] = validation_df[["Concentration", "ratio_260_280", "ratio_260_230"]].round(3)

                # Update the columns to keep for the consolidated df
                validation_columns = ["Job_ID", "BBID", "Clone", "Vector_number", "Notes", 
                                    "Concentration", "ratio_260_280", "ratio_260_230"]
            else:
                # If not pooling, we still need to keep the row order and columns
                validation_df = validation_df[validation_columns]
            
            # Save the processed DataFrame to session state
            st.session_state["validation_df"] = validation_df
        
        # --- This part displays the widgets on every rerun ---
        st.markdown("---")
        st.subheader("Validation Data")
        
        val_row_col1, val_row_col2 = st.columns([1.15, 4])
        with val_row_col1:
            # Use a new key for the text input to avoid conflicts
            validation_name = st.text_input("Validation File Name", key="validation_name_input")
            download_validation = st.download_button("Download Validation", 
                                                    data=st.session_state["validation_df"].to_csv(index=False), 
                                                    file_name=f"{validation_name}.csv", 
                                                    mime="text/csv", 
                                                    type="primary", 
                                                    key="download_validation")
        with val_row_col2:
            st.dataframe(st.session_state["validation_df"], use_container_width=True)

############################## SINGLE ENTRIES MODE ##############################
with single_entries_tab:
    st.subheader("Single entries")

    row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)
    plate_cols_96_48 = range(1, 7)
    row2_col1, row2_col2, row2_col3 = st.columns([2.5, 0.25, 1.25])

    # Display widgets to enter sample information
    with row1_col1:
        gene_ID = st.text_input("Gene ID", 
                                key="gene_ID", 
                                placeholder="None",
                                )
    with row1_col2:
        source_spot = st.selectbox("Source Spot", 
                                    options=["A", "B", "C"], 
                                    index=1, 
                                    key="source_spot",
                                    )
    with row1_col3:
        target_spot = st.selectbox("Target Spot", 
                                    options=["A", "B", "C"], 
                                    index=2, 
                                    key="target_spot",
                                    )
    with row1_col4:
        transfer_volume = st.slider("Transfer Volume", 
                                    min_value=5, 
                                    max_value=200, 
                                    step=5, 
                                    value=85, 
                                    key="transfer_volume",
                                    )

    # Create buttons in a grid
    for row in plate_rows:
        # Generate the buttons for the 96-well plate
        with row2_col1:
            cols_1to12 = st.columns(12)

            for col_index, col in enumerate(plate_cols_96):
                # Generate button label (e.g., A1, B2, etc.)
                button_label = f"{row}{col}"
                # Display button in the appropriate column ]
                with cols_1to12[col_index]:
                    if st.button(button_label, key=button_label+"_96",):
                        # Update session state when a button is clicked
                        st.session_state["source_well"] = button_label
        
        # Generate the buttons for the 48-well plate
        with row2_col3:
            cols_1to6 = st.columns(6)
            for col_index2, col2 in enumerate(plate_cols_96_48):
                # Generate button label (e.g., A1, B2, etc.)
                button_label2 = f"{row}{col2}"
                # Display button in the appropriate column ]
                with cols_1to6[col_index2]:
                    if st.button(button_label2, key=button_label2+"_48"):
                        # Update session state when a button is clicked
                        st.session_state["target_well"] = button_label2

    # Show additional widgets to preview and add or clear the selection
    (row3_col1, row3_col2, row3_col3, row3_col4, row3_col5, 
        row3_col6, row3_col7 ) = st.columns([3, 1, 3, 1, 3, 2, 3])
    row4_col1, row4_col2 = st.columns([4, 1])

    # Error prevention/handling
    if gene_ID == "":
        st.session_state["error_1"] = True
    else:
        st.session_state["error_1"] = False
    if "source_well" not in st.session_state or st.session_state["source_well"] == "":
        st.session_state["error_2"] = True
    else:
        st.session_state["error_2"] = False
    if "target_well" not in st.session_state or st.session_state["target_well"] == "":
        st.session_state["error_3"] = True
    else:
        st.session_state["error_3"] = False

    # Messages to explicitely show what has been clicked for each sample
    message_1 = f"Transfer: {st.session_state.get('gene_ID', '')}"
    message_2 = f"From: {st.session_state.get('source_well', '')}"
    message_3 = f"To: {st.session_state.get('target_well', '')}"
    with row3_col1:
        (st.success if not st.session_state["error_1"] else st.error)(message_1)
    with row3_col3:
        (st.success if not st.session_state["error_2"] else st.error)(message_2)
    with row3_col5:
        (st.success if not st.session_state["error_3"] else st.error)(message_3)

    with row3_col7:
        add_to_worklist = st.button("Add sample", type="primary", key="add_to_worklist")
        
    # Add current selection and sample info to worklist
    if add_to_worklist:
        df = st.session_state.get("df", 
                                pd.DataFrame(columns=["Gene_ID", 
                                                    "Source_spot", "Source_well", 
                                                    "Target_spot", "Target_well", 
                                                    "Transfer_volume",
                                                    "Automation_string"]))
        
        # Check forany missing info that would trigger an error
        if st.session_state["error_1"] or st.session_state["error_2"] or st.session_state["error_3"]:
            st.rerun()
        else:
            # Add current selection and sample info to worklist
            new_row = {"Gene_ID": gene_ID, 
                        "Source_spot": source_spot, "Source_well": st.session_state["source_well"], 
                        "Target_spot": target_spot, "Target_well": st.session_state["target_well"],
                        "Transfer_volume": transfer_volume,
                        "Automation_string": f"{gene_ID};{source_spot};{st.session_state['source_well']};{target_spot};{st.session_state['target_well']};{transfer_volume}"}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            st.session_state["df"] = df

            # Reset only the well buttons (for multiple samples with same gene ID) and rerun the app
            st.session_state["source_well"] = ""
            st.session_state["target_well"] = ""
            st.rerun()
            
    # Display current worklist
    if "df" in st.session_state:
        with row4_col1: 
            st.dataframe(st.session_state["df"], use_container_width=True)
        
        final_worklist = st.session_state["df"]["Automation_string"]
        final_worklist = final_worklist.rename("SampleID;SourceDeckPosition;SourceWell;TargetDeckPosition;TargetWell;TransferVolume [µl]")
        
        with row4_col2: 
            worklist_name = st.text_input("Save worklist as")
            download_worklist = st.download_button("Download Worklist", 
                                                data=final_worklist.to_csv(index=False), 
                                                file_name=f"{worklist_name}.csv", mime="text/csv", 
                                                type="primary", key="download_worklist")
