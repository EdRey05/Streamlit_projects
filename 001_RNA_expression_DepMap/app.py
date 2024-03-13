'''
App made by:
    Eduardo Reyes Alvarez, Ph.D.
Contact:
    eduardo_reyes09@hotmail.com

DepMap release used: 
    23Q4

Data source:
    Original Website: https://depmap.org/portal/download/all/
    Note: This website does not provide the direct download links used here. Instead, when clicking 
        on -View full release details-, it shows some info and references to this Figshare data 
        repository: https://doi.org/10.25452/figshare.plus.24667905.v2
    File 1: OmicsExpressionProteinCodingGenesTPMLogp1.csv  (Downloaded as: DepMap_RNASeq_23Q4.csv)
    File 2: Model.csv  (Downloaded as: DepMap_CellInfo_23Q4.csv)

App version: 
    V08 (Mar 12, 2024): Updated to latest data release.

'''
###################################################################################################

# Import the required libraries

import os
from typing import List
import urllib.request
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_searchbox import st_searchbox
from io import BytesIO

###################################################################################################

# Cached function to download and/or read the required files just once

@st.cache_data(show_spinner=False)
def get_files():
    
    # Show a status bar indicating when each step is completed
    with st.status("Loading...", expanded=False) as status:

        # Defined file names to be used in this script
        rna_file = "DepMap_RNASeq_23Q4.csv"
        cell_info_file = "DepMap_CellInfo_23Q4.csv"

        # Check if files exist in the working directory, otherwise download tem
        if not (os.path.isfile(rna_file) and os.path.isfile(cell_info_file)):
            
            status.update(label="Downloading files...")
            directory1 = "https://plus.figshare.com/ndownloader/files/43347204"
            directory2 = "https://plus.figshare.com/ndownloader/files/43746708"
            urllib.request.urlretrieve(directory1, rna_file)
            urllib.request.urlretrieve(directory2, cell_info_file)
            status.update(label="Files downloaded!")
        else:
            status.update(label="Files found!.")

        # Import the csv files into dataframes
        status.update(label="Importing files...")
        RNA_expression = pd.read_csv(rna_file)
        sample_IDs = pd.read_csv(cell_info_file)
        
        # Sort the IDs by cell line name and get the relevant columns  
        status.update(label="Pre-processing files...")
        sample_IDs = sample_IDs.sort_values(by=["CellLineName"])
        sample_IDs = sample_IDs[sample_IDs["CellLineName"].notna()]
        sample_IDs = sample_IDs.reset_index(drop=True)
        cell_menu = sample_IDs[["ModelID", "CellLineName", "OncotreeLineage", "OncotreePrimaryDisease"]]
        cell_menu.columns = ["Achilles ID", "Cell line", "Tissue", "Disease"]

        # The first column of the RNASeq dataset has no name, and we need it transposed
        RNA_expression = RNA_expression.set_index("Unnamed: 0").T
        RNA_expression["Gene"] = RNA_expression.index
        RNA_expression["Gene"] = RNA_expression["Gene"].str.replace(r'\s\(\d+\)$', '', regex=True)
        RNA_expression = RNA_expression.reset_index(drop=True)
        RNA_expression = RNA_expression.set_index("Gene")

        # Create a dictionary to map "Achilles ID" to "Cell line" and replace the IDs for names in RNA_expression
        id_to_cell_line = dict(zip(cell_menu["Achilles ID"], cell_menu["Cell line"]))
        column_names_to_replace = RNA_expression.columns
        new_column_names = []
        for col in column_names_to_replace:
            new_name = id_to_cell_line.get(col, col)
            new_column_names.append(new_name)
        RNA_expression.columns = new_column_names
        RNA_expression = RNA_expression.sort_index(axis=1)
        RNA_expression = RNA_expression.sort_index()

        # Since not all the cell lines in the DepMap/Achilles project have RNA Seq data, remove those from both menus
        cell_menu = cell_menu[cell_menu["Cell line"].isin(RNA_expression.columns)]
        cell_menu_tissues = [""] + list(cell_menu["Tissue"].dropna().unique())
        cell_menu_tissues.sort()

        status.update(label="Ready to begin search!", state="complete", expanded=False)
        
    return RNA_expression, cell_menu, cell_menu_tissues

###################################################################################################

# Step 1 - Set app configuration and load the required files 

st.set_page_config(
    page_title="Tool 001 - App by Eduardo",
    page_icon=":bar_chart:",
    layout="wide",
    menu_items={
        'Get Help': "https://github.com/EdRey05/Streamlit_projects/tree/main/001_RNA_expression_DepMap",
        'Report a bug': "mailto:eduardo_reyes09@hotmail.com"})

# Check if the data has already been loaded, otherwise download and import it
if "cell_menu" not in st.session_state or st.session_state["cell_menu"] is None:
    
    message = st.markdown('''
        <div style='background-color: #0E6655; padding: 10px; border-radius: 5px; text-align: center; width: 75%; margin: auto;'>
            <p style='font-size: 20px; font-weight: bold;'>THE FILES ARE BEING PREPARED... The app will launch shortly</p>
            <p>This app was tailored for the RNA Seq dataset from the DepMap portal, release 23Q4.</p>
            <p>The file used was OmicsExpressionProteinCodingGenesTPMLogp1.csv and gives values in log2(TPM+1) units.</p>
            <p>For more information on the 23Q4 data or newer releases, consult: <a href="https://depmap.org/portal/download/all/" target="_blank">DepMap Portal</a>.</p>
            <p>Tutorial: <a href="https://github.com/EdRey05/Streamlit_projects/tree/main/001_RNA_expression_DepMap" target="_blank">Instructions and Demo</a> </p>
        </div>
        ''', unsafe_allow_html=True)
    a = st.markdown('<hr style="margin-top: +10px; margin-bottom: +10px;">', unsafe_allow_html=True) 

    # Start downloading or importing the files
    RNA_expression, cell_menu, cell_menu_tissues = get_files()

    # Save heavy data variables to session state so get_files only runs one time
    st.session_state["RNA_expression"] = RNA_expression
    st.session_state["cell_menu"] = cell_menu
    st.session_state["cell_menu_tissues"] = cell_menu_tissues

    # Initialize variables in the session state to enable full widget interactivity
    st.session_state["keep_cells_previous"] = []
    st.session_state["keep_cells_current"] = []
    st.session_state["search_string_temporal"] = ""
    st.session_state["search_results_interactive"] = pd.DataFrame()
    st.session_state["df_to_plot"] = pd.DataFrame()
    st.session_state["displayed_df_to_plot"] = pd.DataFrame()

    # Clear the initial message
    message.empty()
    a.empty()

###################################################################################################

# Step 2 - Create app layout

st.title("Retrieve RNASeq data from the DepMap portal (23Q4)")
st.markdown('<hr style="margin-top: +5px; margin-bottom: +5px;">', unsafe_allow_html=True)
col_1_row_1, col_2_row_1 = st.columns([2, 3], gap="medium")
st.markdown('<hr style="margin-top: +10px; margin-bottom: +15px;">', unsafe_allow_html=True)
col_1_row_2, col_2_row_2, col_3_row_2, col_4_row_2, col_5_row_2, col_6_row_2 = st.columns(6, gap="small")
st.markdown('<hr style="margin-top: +5px; margin-bottom: +10px;">', unsafe_allow_html=True)
col_1_row_3, col_2_row_3 = st.columns(2, gap="medium")

###################################################################################################

# Step 3 - Create the main widgets in column 1-row 1, and one more in the same row upon interaction

# The widgets on the first row are created immediately after loading the files
with col_1_row_1:
    
    # Buttons for the two types of cell line search available
    st.radio(key="search_by", label="Search cell lines by:", options=["Name", "Tissue type"])
    st.markdown('<hr style="margin-top: +10px; margin-bottom: +10px;">', unsafe_allow_html=True)

    # This responds to the radio button and displays a different widget depending on the type of search chosen
    if st.session_state["search_by"] == "Name":
        st.text_input(key="search_string", label="Type the name of the cell line or part of it", value="")

        # Generate the results df
        search_results = st.session_state["cell_menu"].copy()
        search_results["Keep cell line?"] = False
        search_results = search_results[search_results["Cell line"].str.contains(st.session_state["search_string"], case=False, na=False)]

    elif st.session_state["search_by"] == "Tissue type":
        st.selectbox(key="search_string", label="Select a tissue", options=st.session_state["cell_menu_tissues"], index=0)
        
        # Generate the results df
        search_results = st.session_state["cell_menu"].copy()
        search_results["Keep cell line?"] = False
        search_results = search_results[search_results["Tissue"] == st.session_state["search_string"]]
    
    st.markdown('<hr style="margin-top: +10px; margin-bottom: +10px;">', unsafe_allow_html=True)

# When the default option on Column 01 widgets is selected, just clear this column
if st.session_state["search_string"] == "":
    col_2_row_1.empty()
# When the string/name searched is not found in the dataset, show recommendations and a warning
elif search_results.empty:
    col_2_row_1.empty()
    with col_2_row_1:
        st.markdown('''
                    :red[No results matched the input entered] :confused:
                    
                    :bulb: Try using more/less characters of the cell line name, such as SH or SY if you are looking for SH-SY5Y :bulb:
                    
                    :warning: If this problem persists :warning: That cell line may not have been included in the DepMap project, yet :disappointed: :sob:
                    ''')
# Proceed to create widgets if a valid string is entered and a results df is obtained
else:      
    # The widget to select search results takes all col 2-row 2 because its big and resizes itself
    with col_2_row_1:
        search_results_interactive = st.data_editor(data=search_results, hide_index=True, use_container_width=True)
    
    # Checking or unchecking a box triggers the re-run of the app
    # Entering a new search string/term re-runs the app and shows a different df in the editor
    # Changing the search method and selecting a tissue type also re-runs the app
    # Because of that, we use 3 variables to keep track of changes through the editor with the same or different search term 

    # Reset the list of previous selections when a new string on the same widget or the other is entered/selected
    if st.session_state["search_string"] != st.session_state["search_string_temporal"]:
        st.session_state["keep_cells_previous"] = []
        st.session_state["search_string_temporal"] = st.session_state["search_string"]

    # Get any rows (cell lines) that have been checked through the data editor
    selected_cells = search_results_interactive.loc[search_results_interactive["Keep cell line?"], "Cell line"].tolist()
    
    # Add new values to the current selections or keep the ones that were selected before, to both state variables
    for name in selected_cells:
        if name not in st.session_state["keep_cells_previous"]:
            st.session_state["keep_cells_current"].append(name)
            st.session_state["keep_cells_previous"].append(name)
    
    # Unchecking a box makes selected_cells shorter so we remove the missing values from both state variables
    for name in st.session_state["keep_cells_previous"]:
        if name not in selected_cells:
            st.session_state["keep_cells_current"].remove(name)
            st.session_state["keep_cells_previous"].remove(name)

    # The cummulative selections + de-selections are kept and sorted
    st.session_state["keep_cells_current"] = sorted(set(st.session_state["keep_cells_current"]))

# A widget is displayed to visually track all user selections (loads empty immediately with other widgets in this col-row)
with col_1_row_1:
    multiselect_options = [""]+st.session_state["keep_cells_current"]
    st.multiselect(key="keep_cells_final", label="Your selections:", options=multiselect_options, placeholder="", 
                    default=st.session_state.get("keep_cells_current", []))

###################################################################################################

# Step 4 - Extract selected cell lines from the RNA dataset and prepare to preview and download when the user decides to

# Function to save the extracted dataframe to Excel
def save_to_excel(dataframe, filename='RNA_Results.xlsx'):

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        dataframe.to_excel(writer, index=True, sheet_name='Search_01')
    output.seek(0)

    return output

###################

# Button to trigger excel file preparation with the function above
with col_3_row_2:
    preview_button = st.button(label="Preview results", type="primary")

if preview_button and st.session_state["keep_cells_final"]:

    # Clean previous gene selections and plots
    col_2_row_3.empty()
    col_1_row_3.empty()

    # Find the current cummulative selections in the pre-processed RNA df
    st.session_state["extracted_RNA_data"] = st.session_state["RNA_expression"].loc[:, st.session_state["keep_cells_final"]]
    st.session_state["extracted_RNA_data"] = st.session_state["extracted_RNA_data"].reset_index(drop=False)

    # Prepare the data for preliminary plots
    st.session_state["gene_list"] = tuple(st.session_state["extracted_RNA_data"]["Gene"].tolist()) 
    st.session_state["df_to_plot"] = st.session_state["extracted_RNA_data"].copy()   
    st.session_state["df_to_plot"].insert(0, "Plot?", False)
    
    # Call the function to convert the results df to a xlsx file
    st.session_state["excel_data"] = save_to_excel(st.session_state["extracted_RNA_data"])

# Display a button to download the results when a file has been made 
if "excel_data" in st.session_state:
    with col_4_row_2:
        st.download_button(label="Download dataset", data=st.session_state["excel_data"], file_name='RNA_Results.xlsx', type="primary")

###################################################################################################

# Step 5 - Show a preview of the results df and a tool to plot gene expression

# Function to search through the genes for the preliminary plots
def search_genes(searchterm: str) -> List[tuple[str, str]]:
    
    # Assuming st.session_state["gene_list"] is a list of gene names
    suggestions = [gene for gene in st.session_state["gene_list"] if searchterm.lower() in gene.lower()]
    
    # Returning a list of tuples where each tuple contains a label and a value
    return [(gene, gene) for gene in suggestions]

###################

# Function to make plots based on genes selected by the searchbox and/or data editor 
def gene_plotter():
    
    # Get any genes currently selected in the data editor
    plot_genes = st.session_state["displayed_df_to_plot"].loc[st.session_state["displayed_df_to_plot"]["Plot?"], "Gene"].tolist()
    
    if plot_genes:
        # Plot the genes of interest and allow to swap the grouping type
        with col_2_row_3:
            st.radio(key="plot_type", label="Plot type", options=["Bar chart", "Heatmap"])
            st.toggle(key="group_by", label="Swap group by")
            st.markdown('<hr style="margin-top: +10px; margin-bottom: +10px;">', unsafe_allow_html=True)

            # Make one of two possible bar charts
            if st.session_state["plot_type"] == "Bar chart":
                if st.session_state["group_by"]:
                    fig = px.bar(st.session_state["extracted_RNA_data"][st.session_state["extracted_RNA_data"]['Gene'].isin(plot_genes)], 
                            x='Gene', y=st.session_state["extracted_RNA_data"].columns[1:], barmode='group',
                            color_discrete_sequence=px.colors.qualitative.Dark2)

                    # Customize the appearance of the bars
                    fig.update_traces(marker=dict(line=dict(color='black', width=0.5)), selector=dict(type='bar'))
                    fig.update_layout(xaxis_title="Gene", yaxis_title="log2(TPM+1)", legend_title="Cell Line", font=dict(size=24))
                else:
                    fig = px.bar(st.session_state["extracted_RNA_data"][st.session_state["extracted_RNA_data"]['Gene'].isin(plot_genes)].set_index('Gene').T, 
                                barmode='group', color_discrete_sequence=px.colors.qualitative.G10)

                    # Customize the appearance of the bars
                    fig.update_traces(marker=dict(line=dict(color='black', width=0.5)), selector=dict(type='bar'))
                    fig.update_layout(xaxis_title="Cell Line", yaxis_title="log2(TPM+1)", legend_title="Gene", font=dict(size=24))
            else:
                # Make a heatmap
                heatmap_data = st.session_state["extracted_RNA_data"][st.session_state["extracted_RNA_data"]['Gene'].isin(plot_genes)].set_index('Gene').T

                # Switch rows and columns based on the toggle state
                if st.session_state["group_by"]:
                    heatmap_data = heatmap_data.T
                
                # Customize the appearance of the heatmap
                fig = px.imshow(heatmap_data, color_continuous_scale='Cividis')
                fig.update_layout(xaxis_title="Cell Line" if st.session_state["group_by"] else "Gene", 
                                yaxis_title="Gene" if st.session_state["group_by"] else "Cell Line", 
                                font=dict(size=24))

            # Display plot
            fig.update_layout(height=400, width=600)
            st.plotly_chart(fig)
    else:
        # Clear plots if no genes are currently selected
        col_2_row_3.empty()

###################

# Proceed with results visualization only when the data has been extracted
if not st.session_state["df_to_plot"].empty:
    
    # Show a searchbox to quickly find genes as the df has thousands of rows (the user can scroll and check boxes too)
    with col_1_row_3:
        st_searchbox(key="selected_gene", search_function=search_genes, default=None, 
                    label="Type a gene name here or check/uncheck boxes below", clear_on_submit=True,)
        st.markdown('<hr style="margin-top: +10px; margin-bottom: +10px;">', unsafe_allow_html=True)
    
    # When the user selects a gene name, automatically check it to display it at the top of the df
    if st.session_state["selected_gene"].get("result"):
        selected_gene_result = st.session_state["selected_gene"].get("result")
        st.session_state["df_to_plot"].loc[st.session_state["df_to_plot"]["Gene"] == selected_gene_result, "Plot?"] = True
        
        # Reset the searchbox so we dont keep the previous result when the df changes
        st.session_state["selected_gene"] = {"result": None, "search": "", "options_js": []}

    # Show the results df
    st.session_state["sorted_df"] = st.session_state["df_to_plot"].sort_values(by=["Plot?", "Gene"], ascending=[False, True])
    with col_1_row_3:
        st.session_state["displayed_df_to_plot"] = st.data_editor(data=st.session_state["sorted_df"], use_container_width=True, hide_index=True)
    
    # Call the function to plot the selected genes (if any)
    gene_plotter()
    
###################################################################################################