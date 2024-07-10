###################################################################################################
###################################################################################################
'''
App made by:
    Eduardo Reyes Alvarez, Ph.D.
Contact:
    eduardo_reyes09@hotmail.com

App version: 
    V01 (July 09, 2024): First working version for basic merging of files or extracting pages.

'''
###################################################################################################
###################################################################################################

# Import required libraries
import os
import pandas as pd
import streamlit as st
from pypdf import PdfWriter, PdfReader

# App main layout and page loading
st.set_page_config(
    page_title="Tool 005 - App by Eduardo",
    page_icon=":books:",
    layout="wide",
    initial_sidebar_state="expanded")

st.title("PDF Tools")
st.markdown('<hr style="margin-top: +2px; margin-bottom: +2px; border-width: 5px;">', unsafe_allow_html=True)

# Sidebar - Initial widgets
with st.sidebar:
    uploaded_files = st.file_uploader(label="Upload PDF file(s)",
                                        type=["pdf"], 
                                        accept_multiple_files=True)
    st.markdown('<hr style="margin-top: 1px; margin-bottom: 1px; border-width: 5px;">', unsafe_allow_html=True)
    start_button = st.button(label="Begin", type="secondary")
    restart_button = st.button(label="Start over", type="secondary")

###################################################################################################

# Create the merger at the beginning and save to the session state
if start_button:
    st.session_state["files_uploaded"] = True

# Clear the session state if the user wants to start over and delete any output file
if restart_button:
    st.session_state.clear()
    if "output.pdf" in os.listdir():
        os.remove("output.pdf")

if "files_uploaded" in st.session_state:
    # Obtain the number of pages for each uploaded file
    page_counts = {}
    for i, file_content in enumerate(uploaded_files):
        pdf_reader = PdfReader(file_content)
        page_counts[f"File {i+1}"] = len(pdf_reader.pages)

    # Make a table with file names and page counts
    df = pd.DataFrame(columns=["Position", "File Name", "Number of Pages", "Add from here", "Add to here"])
    data = []
    for i, (filename, count) in enumerate(page_counts.items()):
        data.append({"Position": i+1, "File Name": filename, "Number of Pages": count, 
                    "Add from here": 1, "Add to here": count})
    
    # Add the data to the table
    df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)

    # Display the table with editable widgets to select pages to merge and file order
    st.write("Edit the following table to select pages to merge:")
    selected_pages = st.data_editor(df, use_container_width=True, hide_index=True)
    st.markdown('<hr style="margin-top: 1px; margin-bottom: 1px; border-width: 5px;">', unsafe_allow_html=True)

    # Create columns to display buttons
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        merge_now = st.button("Merge now", type="primary")
    st.session_state["merge_now"] = merge_now

# We show a button to let the user edit the other widget before merging the files
if "merge_now" in st.session_state and st.session_state["merge_now"]:
    # Merge the selected pages into a new PDF file
    output_file = PdfWriter()

    # Sort the selected_pages dataframe based on the "Position" column
    selected_pages = selected_pages.sort_values(by="Position")

    # Iterate through the sorted dataframe to obtain the file name and pages to add
    for index, row in selected_pages.iterrows():
        filename = row["File Name"]
        initial_page = row["Add from here"]
        final_page = row["Add to here"]

        # Process the file name, add_from_here, and add_to_here as needed
        pdf_reader = PdfReader(uploaded_files[index])
        for page_num in range(initial_page, final_page + 1):
            output_file.add_page(pdf_reader.pages[page_num - 1])

    # Save the merged PDF file
    with open("output.pdf", "wb") as file:
        output_file.write(file)

# Display a download button whenever there is an output file
if "output.pdf" in os.listdir():
    # Download the merged PDF file
    with col2:
        st.download_button(label="Download merged file", data=open("output.pdf", "rb").read(), 
                            file_name="output.pdf", type="primary")

    # Display a success message
    with col3:
        st.success("PDF files merged successfully!")

#################################################################################################