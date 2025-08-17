'''
App made by:
    Eduardo Reyes Alvarez, Ph.D.
Contact:
    ed5reyes@outlook.com

App version: 
    v2.0 (Jul 21, 2025): Added feature to simplify pooled samples.

'''
###############################################################################

# Import the required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import streamlit as st

# Streamlit App setup
st.set_page_config(
    page_title="Tool 006 - App by Eduardo",
    page_icon=":bar_chart:",
    layout="wide")
st.title("Create worklist for Integra liquid handler")

################################## Single entries
st.markdown("""<hr style="border: none; height: 5px; background-color: #444;">""", 
            unsafe_allow_html=True,
            )
st.subheader("Single entries")

# Initialize a grid with 8 rows (A to H) and 12 columns (1 to 12)
rows = ["A", "B", "C", "D", "E", "F", "G", "H"]
columns_96 = range(1, 13)
row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)
columns_48 = range(1, 7)
row2_col1, row2_col2, row2_col3 = st.columns([2.5, 0.25, 1.25])

# Display widgets to enter sample information
with row1_col1:
    gene_ID = st.text_input("Gene ID", key="gene_ID", placeholder="None")
with row1_col2:
    source_spot = st.selectbox("Source Spot", options=["A", "B", "C"], index=1, key="source_spot")
with row1_col3:
    target_spot = st.selectbox("Target Spot", options=["A", "B", "C"], index=2, key="target_spot")
with row1_col4:
    transfer_volume = st.slider("Transfer Volume", min_value=5, max_value=200, step=5, value=85, key="transfer_volume")

# Create buttons in a grid
for row in rows:
    # Generate the buttons for the 96-well plate
    with row2_col1:
        cols_1to12 = st.columns(12)

        for col_index, col in enumerate(columns_96):
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
        for col_index2, col2 in enumerate(columns_48):
            # Generate button label (e.g., A1, B2, etc.)
            button_label2 = f"{row}{col2}"
            # Display button in the appropriate column ]
            with cols_1to6[col_index2]:
                if st.button(button_label2, key=button_label2+"_48"):
                    # Update session state when a button is clicked
                    st.session_state["target_well"] = button_label2

# Show additional widgets to preview and add or clear the selection
row3_col1, row3_col2, row3_col3, row3_col4, row3_col5, row3_col6, row3_col7 = st.columns([3, 1, 3, 1, 3, 2, 3])
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

###################################### BULK MODE

# Create column layout for required widgets
st.markdown("""<hr style="border: none; height: 5px; background-color: #444;">""", 
            unsafe_allow_html=True,
            )
st.subheader("Bulk Mode")
row5_col1, row5_col2 = st.columns([1, 4])
row6_col1, row6_col2 = st.columns([1, 4])

# Create initial empty df
df2 = pd.DataFrame(columns=["GeneID", "Clone", "Vector#", "Seq_well"], index=range(96))

# Create initial 96-well plate layout
plate_rows = ['A','B','C','D','E','F','G','H']
plate_cols = range(1, 13)
plate_wells = [f"(#{r}{c})" for c in plate_cols for r in plate_rows]

with row5_col1:
    source_spot2 = st.selectbox("Source spot", options=["A", "B", "C"], index=1)
    target_spot2 = st.selectbox("Target spot", options=["A", "B", "C"], index=2)
    transfer_volume2 = st.slider("Transfer Volume", min_value=5, max_value=200, step=5, value=85)
    pool_checkbox = st.checkbox("Pool replicates", value=False, key="pool_replicates")
    autowell_checkbox = st.checkbox("Auto-assign wells", value=False, key="auto_well")
    convert = st.button("Convert to worklist", type="primary")

with row5_col2:
    temp_df = st.data_editor(df2, 
                            use_container_width=True, 
                            key="temp_df",
                            column_config={
                                "Clone": None if not pool_checkbox else {},
                                "Seq_well": None if autowell_checkbox else {},
                            }
                            )

if convert or "df2" in st.session_state:
    # Don't do anything if the required identifiers are missing
    if (temp_df['GeneID'].fillna('') == '').all() or (temp_df['Vector#'].fillna('') == '').all():
        st.stop()
    
    # Make a copy of the input df and start filling the columns
    converted_df = temp_df.copy()
    converted_df["Source_spot"] = source_spot2
    converted_df["Target_spot"] = target_spot2
    converted_df["Transfer_volume"] = transfer_volume2
    
    # For now, samples have a format T0618P2A1, so removing 7 characters gives location
    converted_df["Source_well"] = converted_df["Vector#"].str.slice(7)

    if autowell_checkbox and not pool_checkbox:
        converted_df["Seq_well"] = pd.DataFrame({'Seq_well': plate_wells})
    elif autowell_checkbox and pool_checkbox:
        assigned_wells = {}
        well_index = 0
        seq_well_values = []

        for i, row in converted_df.iterrows():
            clone_id = row.get("Clone")

            # Treat empty or missing Clone as unique per row
            clone_key = clone_id if pd.notna(clone_id) and clone_id != "" else f"__row_{i}"

            if clone_key in assigned_wells:
                seq_well_values.append(assigned_wells[clone_key])
            else:
                assigned_well = plate_wells[well_index]
                assigned_wells[clone_key] = assigned_well
                seq_well_values.append(assigned_well)
                well_index += 1

        converted_df["Seq_well"] = seq_well_values

    converted_df["Target_well"] = converted_df["Seq_well"].str.replace(r"[#\(\)]", "", regex=True)
    converted_df["Automation_string"] = converted_df.apply(lambda row: f"{row["GeneID"]};{row["Source_spot"]};{row["Source_well"]};{row["Target_spot"]};{row["Target_well"]};{row["Transfer_volume"]}", axis=1)
    st.session_state["df2"] = converted_df
    
    # Get the updated df, keep only the automation string and rename column as the software utilises
    final_worklist2 = st.session_state["df2"].dropna()
    final_worklist2 = final_worklist2["Automation_string"]
    final_worklist2 = final_worklist2.rename("SampleID;SourceDeckPosition;SourceWell;TargetDeckPosition;TargetWell;TransferVolume [µl]")
    
    with row6_col1:
        st.divider()
        worklist2_name = st.text_input("Worklist Name", key="worklist2_name")
        download_worklist2 = st.download_button("Download Worklist", 
                                            data=final_worklist2.to_csv(index=False), 
                                            file_name=f"{worklist2_name}.csv", mime="text/csv", 
                                            type="primary", key="download_worklist2")
        st.divider()

    with row6_col2:
        row6_col2.empty()
        st.dataframe(st.session_state["df2"], use_container_width=True)
