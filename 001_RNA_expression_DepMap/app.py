'''
App made by:
    Eduardo Reyes Alvarez, Ph.D.
Contact:
    eduardo_reyes09@hotmail.com

DepMap release used: 
    23Q2

Files used: 
    OmicsExpressionProteinCodingGenesTPMLogp1.csv  (Downloaded as: DepMap_RNASeq_23Q2.csv)
    Model.csv  (Downloaded as: DepMap_CellInfo_23Q2.csv)

App version: 
    V01 (Oct 22, 2023): First working version. Not fully annotated.

'''
###################################################################################################

# Import the required libraries

import os
import urllib.request
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from io import BytesIO

###################################################################################################

# App two-column layout

st.set_page_config(
    page_title="Tool 01 - App by Eduardo",
    page_icon=":bar_chart:",
    layout="wide",
    menu_items={
        'Report a bug': 'mailto:eduardo_reyes09@hotmail.com',
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.title("Retrieve RNASeq data from DepMap")

column_01, column_02 = st.columns([2, 3], gap="medium")


###################################################################################################

# Cached function to download and/or read the required files 

@st.cache_data(show_spinner=False)
def get_files():

    # Show a status bar indicating when each step is completed
    with st.status("Loading...", expanded=False) as status:

        # Defined file names to be used in this script
        rna_file = "DepMap_RNASeq_23Q2.csv"
        cell_info_file = "DepMap_CellInfo_23Q2.csv"

        # Check if files exist in the working directory, otherwise download tem
        if not (os.path.isfile(rna_file) and os.path.isfile(cell_info_file)):
            
            status.update(label="Downloading files...")
            directory1 = "https://figshare.com/ndownloader/files/40449128"
            directory2 = "https://figshare.com/ndownloader/files/40448834"
            urllib.request.urlretrieve(directory1, rna_file)
            urllib.request.urlretrieve(directory2, cell_info_file)
            status.update(label="Files downloaded!")
        else:
            status.update(label="Files found!.")

        # Import the csv files into dataframes
        status.update(label="Importing files...")
        RNA_expression = pd.read_csv(rna_file)
        sample_IDs = pd.read_csv(cell_info_file)
        
        # Sort the IDs by cell line name and get the relevant columns to show the user in both search modes 
        status.update(label="Pre-processing files...")
        sample_IDs = sample_IDs.sort_values(by=["CellLineName"])
        sample_IDs = sample_IDs[sample_IDs["CellLineName"].notna()]
        sample_IDs = sample_IDs.reset_index(drop=True)
        cell_menu = sample_IDs[["ModelID", "CellLineName", "OncotreeLineage", "OncotreePrimaryDisease"]]
        cell_menu.columns = ["Achilles ID", "Cell line", "Tissue", "Disease"]
        cell_menu_tissues = [""] + list(cell_menu["Tissue"].unique())
        cell_menu_tissues.sort()

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

        status.update(label="Ready to begin search!", state="complete", expanded=False)

    return RNA_expression, cell_menu, cell_menu_tissues

###################################################################################################

# Call the function above when the app loads, and use cached variables for all re-runs

# Check if the data has already been loaded, otherwise download or get them
if "cell_menu" not in st.session_state or st.session_state["cell_menu"] is None:
    
    RNA_expression, cell_menu, cell_menu_tissues = get_files()

    # Save data relevant data on the first run
    st.session_state["RNA_expression"] = RNA_expression
    st.session_state["cell_menu"] = cell_menu
    st.session_state["cell_menu_tissues"] = cell_menu_tissues
    st.session_state["keep_cells_previous"] = []
    st.session_state["keep_cells_current"] = []
    st.session_state["search_string_temporal"] = ""
    st.session_state["search_results_interactive"] = pd.DataFrame()

#################################################

# Create the widgets for each column

with column_01:
    
    # Buttons for the two types of search available
    st.radio(key="search_by", label="Search cell lines by:", options=["Name", "Tissue type"])

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

# When the default option on Column 01 widgets is selected, just clear this column
if st.session_state["search_string"] == "":
    column_02.empty()
# When the string/name searched is not found in the dataset, show recommendations and a warning
elif search_results.empty:
    column_02.empty()
    with column_02:
        st.markdown('''
                    :red[No results matched the input entered] :confused:
                    
                    :bulb: Try using more/less characters of the cell line name, such as SH or SY if you are looking for SH-SY5Y :bulb:
                    
                    :warning: If this problem persists :warning: That cell line may not have been included in the DepMap project, yet :disappointed: :sob:
                    ''')
# Proceed to create widgets if a valid string and results are obtained
else:      
    # e
    with column_02:
        search_results_interactive = st.data_editor(data=search_results, hide_index=True)
    
    # a
    if st.session_state["search_string"] != st.session_state["search_string_temporal"]:
        st.session_state["keep_cells_previous"] = []
        st.session_state["search_string_temporal"] = st.session_state["search_string"]

    selected_cells = search_results_interactive.loc[search_results_interactive["Keep cell line?"], "Cell line"].tolist()
    for name in selected_cells:
        if name not in st.session_state["keep_cells_previous"]:
            st.session_state["keep_cells_current"].append(name)
            st.session_state["keep_cells_previous"].append(name)
    for name in st.session_state["keep_cells_previous"]:
        if name not in selected_cells:
            st.session_state["keep_cells_current"].remove(name)
            st.session_state["keep_cells_previous"].remove(name)

    st.session_state["keep_cells_current"] = sorted(set(st.session_state["keep_cells_current"]))

# Multiselect Widget
with column_01:
    multiselect_options = [""]+st.session_state["keep_cells_current"]
    st.multiselect(label="Your selections:", options=multiselect_options, placeholder="", default=st.session_state.get("keep_cells_current", []), key="keep_cells_final")

###################################################################################################

# Previewing and saving the results

# Create a function to save DataFrame to Excel
def save_to_excel(dataframe, filename='RNA_Results.xlsx'):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        dataframe.to_excel(writer, index=True, sheet_name='Search_01')
    output.seek(0)
    return output

with column_01:
    st.button(key="reset_button", label="Start over", type="primary")
if st.session_state["reset_button"]:
    column_02.empty()
    column_01.empty()
    st.session_state.clear()

# Save results
with column_01:
    save_button = st.button(label="Preview results", type="primary")
if save_button:
    extracted_RNA_data = st.session_state["RNA_expression"].loc[:, st.session_state["keep_cells_final"]]
    extracted_RNA_data = extracted_RNA_data.reset_index(drop=False)
    st.dataframe(extracted_RNA_data)

    excel_data = save_to_excel(extracted_RNA_data)
    column_01 = st.download_button(label="Download dataset", data=excel_data, file_name='RNA_Results.xlsx')
