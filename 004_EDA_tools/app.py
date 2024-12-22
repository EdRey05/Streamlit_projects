'''
App made by:
    Eduardo Reyes Alvarez, Ph.D.
Contact:
    eduardo_reyes09@hotmail.com

App version: 
    V02 (Dec 22, 2024): First working version with basic features. Need to improve the caching of
                        of the AI reports, layout and styling customization, etc.
'''
###################################################################################################

# General libraries
import numpy as np
import pandas as pd

# EDA libraries
from mitosheet.streamlit.v1 import spreadsheet as mitoss
import pygwalker as pyg

# AI EDA libraries
import ydata_profiling
import sweetviz

# Streamlit libraries
import streamlit as st
import hydralit_components as hc
from streamlit_option_menu import option_menu
from streamlit_ydata_profiling import st_profile_report
import streamlit.components.v1 as components

###################################################################################################

# App configuration and layout
st.set_page_config(
    page_title="Tool 004 - App by Eduardo",
    page_icon=":chart_with_uneven_scale:",
    layout="wide",
    initial_sidebar_state="expanded")   

# Make a pages menu on the siderbar
selected_page = option_menu("Data analysis tools", ["Load data", "Process data", "AI EDA"], 
                            icons=["filetype-pptx", "patch-question-fill", "columns-gap"], 
                            menu_icon="cast", default_index=0, orientation="horizontal")

st.markdown('<hr style="margin-top: +2px; margin-bottom: +2px; border-width: 5px;">', unsafe_allow_html=True)

# Load the selected app page (this function is called at the very end)
def change_pages():
    if selected_page == "Load data":
        load_first_page()
    elif selected_page == "Process data":
        load_second_page()
    else:
        load_third_page() 

###################################################################################################

# First page - show the uploaded data to verify it was imported correctly
def load_first_page():

    # Make columns for the widgets
    col1_row1, col2_row1 = st.columns([4, 1])
    
    # Add widgets to upload a file and a start button
    with col1_row1:
        uploaded_file = st.file_uploader("Upload a file", type=["csv", "txt"])
    with col2_row1:
        start_button = st.button(label="Start", type="primary")

    st.markdown('<hr style="margin-top: 1px; margin-bottom: 1px; border-width: 5px;">', unsafe_allow_html=True)
    # Save the df in the session state if the df is ready
    if start_button and "df" not in st.session_state:
        # Load the uploaded file
        if uploaded_file is not None:

            # Check the file extension to determine how to load it with pandas
            if uploaded_file.name.endswith(".txt"):
                df = pd.read_csv(uploaded_file, sep="\t", comment="#")
            else:
                df = pd.read_csv(uploaded_file)      
        else:
            st.error("Please upload a dataset first")
            st.stop()
        
        # Save the df in the session state
        st.session_state["df"] = df

    # Get the df from the session state
    df = st.session_state.get("df", None)
    if df is None:
        st.error("Please upload and confirm/update your dataframe first")
        st.stop()

    # Display the df
    st.success("Review your df, if it is correct and ready, click the button below and go to the other pages")
    save_df = st.button("Confirm df", type="primary")
    st.write("Shape of your df: ", df.shape) 
    st.dataframe(df)


###################################################################################################

# Second page - Data processing and analysis
def load_second_page():

    # Get the df from the session state
    current_df = st.session_state.get("df", None)
    if current_df is None:
        st.error("Please upload and confirm/update your dataframe first")
        st.stop()
    
    # Show a button to update the df
    st.success("Edit your df, once ready, update it so it can be used in the other pages")
    update_df = st.button("Update df", type="primary")
    if update_df:
        st.session_state["df"] = current_df

    # Menu options
    menu_data = [{'id':'st_de', 'label':"Streamlit Data Editor"},
                {'id':'mito', 'label':"Mitosheet"},
                {'id':'pyg', 'label':"Pygwalker"}]
    font_fmt = {'font-class':'h2','font-size':'150%'}

    over_theme =  {'txc_inactive': 'white','menu_background':'purple','txc_active':'yellow','option_active':'blue'}
    current_tab = hc.option_bar(option_definition=menu_data,
                                title='Choose a tool',
                                key='PrimaryOption',
                                override_theme=over_theme,
                                font_styling=font_fmt,
                                horizontal_orientation=True)

    if current_tab == "st_de":
        new_df = st.data_editor(current_df, key="de_df", num_rows="dynamic", use_container_width=True)
        st.session_state["df"] = new_df
    elif current_tab == "mito":
        new_dfs, code = mitoss(current_df, df_names=['df'])
        new_df = list(new_dfs.values())[0]
        st.session_state["df"] = new_df
        st.expander("Show code", expanded=False).code(code)
    elif current_tab == "pyg":
        pyg_html = pyg.to_html(current_df)
        components.html(pyg_html, height=950, scrolling=True)
    

###################################################################################################

# First page - Tools for AI-based EDA
def load_third_page():

    # Get the df from the session state
    current_df = st.session_state.get("df", None)
    if current_df is None:
        st.error("Please upload and confirm/update your dataframe first")
        st.stop()
    
    # Menu options
    menu_data = [{'id':'ydata_profiling', 'label':"ydata_profiling"},
                {'id':'sweetviz', 'label':"sweetviz"}]
    font_fmt = {'font-class':'h2','font-size':'150%'}
    
    over_theme = {'txc_inactive': 'white','menu_background':'purple','txc_active':'yellow','option_active':'blue'}
    current_tab = hc.option_bar(option_definition=menu_data,
                                title='Choose a tool',
                                key='PrimaryOption',
                                override_theme=over_theme,
                                font_styling=font_fmt,
                                horizontal_orientation=True)

    # Generate the reports
    ydata_report = ydata_profiling.ProfileReport(current_df)
    sweetviz_report = sweetviz.analyze([current_df, "sv_EDA"])

    # Display the selected tool
    if current_tab == "ydata_profiling":
        st_profile_report(ydata_report, navbar=True)
    elif current_tab == "sweetviz":
        sweetviz_report.show_html(filepath='sv_EDA.html', open_browser=False, layout='vertical', scale=1.0)
        with open('sv_EDA.html', 'r') as f:
            html_string = f.read()
        components.html(html_string, width=1050, height=1200, scrolling=True)
    
###################################################################################################
change_pages()
###################################################################################################
