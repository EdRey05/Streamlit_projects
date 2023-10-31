'''
App made by:
    Eduardo Reyes Alvarez, Ph.D.
Contact:
    eduardo_reyes09@hotmail.com

App version: 
    V02 (Oct 31, 2023): Few additional modifications were needed to make a functional version for 
                        Streamlit. Pending to customize buttons, add a progress/status widget, and 
                        fill in the text content for the info pages.

'''
###################################################################################################

# Import required libraries

import os
import glob
from zipfile import ZipFile
import urllib.request
import pandas as pd
import time
import streamlit as st
from streamlit_option_menu import option_menu

# Python-pptx specific modules

# To make the presentation
from pptx import Presentation
# To specify sizes of images and text (Other options like inches are available)
from pptx.util import Cm, Pt            
# To specify text alignment (the method is used on the text frame, not on the box or the actual text)
from pptx.enum.text import PP_ALIGN     
# To work with line and fill colours
from pptx.enum.dml import MSO_THEME_COLOR

###################################################################################################

# Function to process the input files
@st.cache_data
def process_files():

    # Extract all the folder structure and files of the zip file provided by the user
    with ZipFile(st.session_state["data_zipfile"], 'r') as zip:
        zip.extractall()

    # The unzipping takes several seconds, so we wait for the folder to appear
    while not "Data" in os.listdir():
        time.sleep(1)

    # Walk through the Data folder to find all csv files
    data_folder = os.path.join(st.session_state["current_directory"], "Data")
    extension_wanted = "*.csv"
    all_csv_files = [file
                    for path, subdir, files in os.walk(data_folder)
                    for file in glob.glob(os.path.join(path, extension_wanted))]

    # Make list with names and paths of the experimental conditions (according to the number of csv files found above)
    exp_conditions_info = []
    for csv_file in all_csv_files:
        csv_root_folder = csv_file.split("Data/")[1].split("/Quantification")[0]
        exp_conditions_info.append([csv_root_folder, csv_file])

    # We will store all the information of the images to insert to the ppt here
    all_info_for_slides = []

    # Iterate for each folder contained in the Data folder uploaded
    for condition_info in exp_conditions_info:
        
        # Read the csv file for the current experimental condition
        results_table = pd.read_csv(condition_info[1])

        # Make some edits for easier manipulation and sorting of the subtitles, folders and ROI names
        results_table["Image used"] = results_table["Image used"].str.replace("MAX_","")
        results_table["Image used"] = results_table["Image used"].str.replace(".tif","")
        results_table["Cell quantified"] = results_table["Cell quantified"].str.replace("_1.roi","")
        results_table["Cell quantified"] = results_table["Cell quantified"].apply(int)
        results_table["Particle count threshold"] = results_table["Particle count threshold"].apply(int)
        results_table["Particle count maxima"] = results_table["Particle count maxima"].apply(int)
        results_table = results_table.sort_values(by=["Image used", "Cell quantified"],ignore_index=True)

        # Iterate through the rows of the csv file (ROIs/cells quantified)
        for index, row in results_table.iterrows():
            
            # Retrieve all the relevant information for that row
            ROI_title = condition_info[0]
            ROI_subtitle = row["Image used"]
            ROI_name = str(row["Cell quantified"])
            ROI_Fluorescence_image = condition_info[1].replace("Quantification/Results.csv", "Cropped cells/Fluorescence/"+ROI_subtitle+"/"+ROI_name+"_2.jpg")
            ROI_Tcount_image = ROI_Fluorescence_image.replace("Fluorescence", "T_Particles").replace("_2.jpg", "_1.jpg")
            ROI_Tcount = row["Particle count threshold"]
            ROI_FMcount_image = ROI_Fluorescence_image.replace("Fluorescence", "FM_Particles").replace("_2.jpg", "_1.jpg")
            ROI_FMcount = row["Particle count maxima"]

            all_info_for_slides.append([ROI_title, ROI_subtitle, ROI_Fluorescence_image, ROI_name, ROI_Tcount_image, ROI_Tcount, ROI_FMcount_image, ROI_FMcount])

    # Prepare empty variables to store the grouped images for each slide
    all_slides_content = []
    temp_slide = []

    # Retrieve the title and subtitle of the very first image to feed the loop at i=0
    current_title = all_info_for_slides[0][0]
    current_subtitle = all_info_for_slides[0][1]

    # Iterate through all the information retrieve for each cell/ROI
    for info in all_info_for_slides:
        
        # Get the current title and subtitle to compare to the reference
        new_title = info[0]
        new_subtitle = info[1]

        # Check the 3 conditions described in text above
        if len(temp_slide)==20 or new_title!=current_title or new_subtitle!=current_subtitle:
            
            # If anything triggers the change of slide, dump the current, empty it and set titles as refs
            all_slides_content.append(temp_slide)
            temp_slide = []
            current_title = new_title
            current_subtitle = new_subtitle
        
        # Always attach the cell/ROI, could be at the same group/slide with others, or to a empty temp slide
        temp_slide.append(info)

    return all_slides_content

###################################################################################################

# Function to generate the presentations and pass the slide maker the content it should insert 

def generate_pptxs(all_slides_content):

    # This will make two presentations, one for the Thresholding and one for the Find Maxima methods

    # Open the presentation uploaded by the user
    presentation_T = Presentation(st.session_state["template_pptx"])

    # Iterate through the image info grouped by slide
    for slide_content in all_slides_content:

        # Prepare the parameters we need to pass to the function that makes the slides
        current_slide_title = slide_content[0][0]
        current_slide_subtitle = slide_content[0][1]
        image_count_for_slide = len(slide_content)
        F_images_for_slide = [image[2] for image in slide_content]
        F_images_labels = [image[3] for image in slide_content]
        P_images_for_slide = [image[4] for image in slide_content]
        P_images_labels = [image[5] for image in slide_content]

        # Feed the function that makes the slide and inserts the corresponding images
        presentation_T = slide_maker(presentation_T, current_slide_title, current_slide_subtitle, image_count_for_slide, 
                                     F_images_for_slide, P_images_for_slide, F_images_labels, P_images_labels)

    # Finally, save this summary presentation after all slides have been created
    presentation_T.save(os.path.join(st.session_state["current_directory"], "Summary_results_T.pptx"))

    # Open the presentation uploaded by the user
    presentation_FM = Presentation(st.session_state["template_pptx"])

    # Iterate through the image info grouped by slide
    for slide_content in all_slides_content:

        # Prepare the parameters we need to pass to the function that makes the slides
        current_slide_title = slide_content[0][0]
        current_slide_subtitle = slide_content[0][1]
        image_count_for_slide = len(slide_content)
        F_images_for_slide = [image[2] for image in slide_content]
        F_images_labels = [image[3] for image in slide_content]
        P_images_for_slide = [image[6] for image in slide_content]
        P_images_labels = [image[7] for image in slide_content]
        
        # Feed the function
        presentation_FM = slide_maker(presentation_FM, current_slide_title, current_slide_subtitle, image_count_for_slide, 
                                      F_images_for_slide, P_images_for_slide, F_images_labels, P_images_labels)

    # Finally, save this summary presentation after all slides have been created
    presentation_FM.save(os.path.join(st.session_state["current_directory"], "Summary_results_FM.pptx"))

###################################################################################################

# Function to add slides to a pptx and inserts images+text 

def slide_maker(presentation_input, current_slide_title, current_slide_subtitle, image_count_for_slide, 
                F_images_for_slide, P_images_for_slide, F_images_labels, P_images_labels):

    # All coordinates are stated always in the same order: From left first, from top second.

    # Title text box dimensions and coordinates (centimeters) 
    title_width = 17
    title_height = 1.5
    title_left_coordinate = 0
    title_top_coordinate = 0
    
    # Subtitle text box dimensions and coordinates (centimeters)
    subtitle_width = 17
    subtitle_height = 1.5
    subtitle_left_coordinate = 17
    subtitle_top_coordinate = 0
    
    # Size and coordinates for the 20 pairs of images (centimeters)
    image_width = 3.25
    image_height = 3
    image_coordinates = [
    (0.25, 2.1, 3.5, 2.1),   (7, 2.1, 10.25, 2.1),   (13.75 , 2.1, 17, 2.1),  (20.5, 2.1, 23.75, 2.1),    (27.25, 2.1, 30.5, 2.1),
    (0.25, 6.4, 3.5, 6.4),   (7, 6.4, 10.25, 6.4),   (13.75, 6.4, 17, 6.4),   (20.5, 6.4, 23.75, 6.4),    (27.25, 6.4, 30.5, 6.4),
    (0.25, 10.7, 3.5, 10.7), (7, 10.7, 10.25, 10.7), (13.75, 10.7, 17, 10.7), (20.5, 10.7, 23.75, 10.7),  (27.25, 10.7, 30.5, 10.7),
    (0.25, 15, 3.5, 15),     (7, 15, 10.25, 15),     (13.75, 15, 17, 15),     (20.5, 15, 23.75, 15),      (27.25, 15, 30.5, 15)
    ]
    
    # Size and coordinates for the 20 pairs of text labels (centimeters) (+3cm top coordinate of images)
    image_labels_width = 3.25
    image_labels_height = 1
    image_labels_coordinates = [
    (0.25, 5.1, 3.5, 5.1),   (7, 5.1, 10.25, 5.1),   (13.75 , 5.1, 17, 5.1),  (20.5, 5.1, 23.75, 5.1),    (27.25, 5.1, 30.5, 5.1),
    (0.25, 9.4, 3.5, 9.4),   (7, 9.4, 10.25, 9.4),   (13.75, 9.4, 17, 9.4),   (20.5, 9.4, 23.75, 9.4),    (27.25, 9.4, 30.5, 9.4),
    (0.25, 13.7, 3.5, 13.7), (7, 13.7, 10.25, 13.7), (13.75, 13.7, 17, 13.7), (20.5, 13.7, 23.75, 13.7),  (27.25, 13.7, 30.5, 13.7),
    (0.25, 18, 3.5, 18),     (7, 18, 10.25, 18),     (13.75, 18, 17, 18),     (20.5, 18, 23.75, 18),      (27.25, 18, 30.5, 18)
    ]
    
    # Create a new slide (layout Blank)
    blank_slide_layout = presentation_input.slide_layouts[6]
    slide = presentation_input.slides.add_slide(blank_slide_layout)
    
    # Make the title for this experimental condition
    left = Cm(title_left_coordinate)
    top = Cm(title_top_coordinate)
    width = Cm(title_width)
    height = Cm(title_height)
    title_textbox = slide.shapes.add_textbox(left, top, width, height)
    title_frame = title_textbox.text_frame
    title_text = title_frame.paragraphs[0]
    title_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    title_text.text = current_slide_title
    title_text.font.bold = True
    title_text.font.size = Pt(32)
    title_text.font.name = "Times New Roman"
    
    # Make the subtitle for the image where the ROI was cropped from
    left = Cm(subtitle_left_coordinate)
    top = Cm(subtitle_top_coordinate)
    width = Cm(subtitle_width)
    height = Cm(subtitle_height)
    subtitle_textbox = slide.shapes.add_textbox(left, top, width, height)
    subtitle_frame = subtitle_textbox.text_frame
    subtitle_text = subtitle_frame.paragraphs[0]
    subtitle_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    subtitle_text.text = current_slide_subtitle
    subtitle_text.font.size = Pt(32)
    subtitle_text.font.name = "Times New Roman"
    
    # Based on the number of images for the current slide, retrieve the neccesary images and coordinates
    for i in range(image_count_for_slide):
        
        # Find the images to insert
        fluorescence_image = F_images_for_slide[i]
        particle_image = P_images_for_slide[i]
        
        # Insert the cropped cell from the Fluorescence folder first
        left = Cm(image_coordinates[i][0])
        top = Cm(image_coordinates[i][1])
        width = Cm(image_width)
        height = Cm(image_height)
        inserting_image = slide.shapes.add_picture(fluorescence_image, left, top, width, height)
        
        # Insert the text label corresponding to the image just inserted above
        left = Cm(image_labels_coordinates[i][0])
        top = Cm(image_labels_coordinates[i][1])
        width = Cm(image_labels_width)
        height = Cm(image_labels_height)
        inserting_image_textbox = slide.shapes.add_textbox(left, top, width, height)
        inserting_image_frame = inserting_image_textbox.text_frame
        inserting_image_text = inserting_image_frame.paragraphs[0]
        inserting_image_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        inserting_image_text.text = F_images_labels[i]
        inserting_image_text.font.size = Pt(20)
        inserting_image_text.font.name = "Times New Roman"
        
        # Insert the cropped cell from the Particles folder second (FM or T particles)
        left = Cm(image_coordinates[i][2])
        top = Cm(image_coordinates[i][3])
        width = Cm(image_width)
        height = Cm(image_height)
        inserting_image2 = slide.shapes.add_picture(particle_image, left, top, width, height)
        inserting_image2.line.fill.solid()
        inserting_image2.line.width = Pt(0.5)
        inserting_image2.line.fill.fore_color.theme_color = MSO_THEME_COLOR.ACCENT_1
    
        # Insert the text label corresponding to the particle counts just inserted above
        left = Cm(image_labels_coordinates[i][2])
        top = Cm(image_labels_coordinates[i][3])
        width = Cm(image_labels_width)
        height = Cm(image_labels_height)
        inserting_image2_textbox = slide.shapes.add_textbox(left, top, width, height)
        inserting_image2_frame = inserting_image2_textbox.text_frame
        inserting_image2_text = inserting_image2_frame.paragraphs[0]
        inserting_image2_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        inserting_image2_text.text = "P="+str(P_images_labels[i])
        inserting_image2_text.font.size = Pt(20)
        inserting_image2_text.font.name = "Times New Roman"
    
    return presentation_input

###################################################################################################

# Function to load the first app page with instructions on how to use the app

def load_first_page():
    
    return

###################################################################################################

# Function to load the second app page which takes the input Data.zip file and producess the outputs

def load_second_page():
    
    # Show the user a widget to upload the compressed file
    uploaded_file = st.file_uploader("Upload compressed file", type=["zip"], accept_multiple_files=False)

    # Display a button so the user decides when to start (in case uploaded the incorrect file)
    start_button = st.button(label="Generate pptx", type="primary")
    if start_button and uploaded_file:
        
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getvalue())
        st.session_state["data_zipfile"] = os.path.join(os.path.dirname(os.path.abspath(uploaded_file.name)), "Data.zip")

        # Process the files to extract the information needed to import to the slide generator
        all_slides_content = process_files()
        generate_pptxs(all_slides_content)

        # Display download buttons for each of the two files produced
        threholding_file_path = os.path.join(st.session_state["current_directory"], "Summary_results_T.pptx")
        find_maxima_file_path = os.path.join(st.session_state["current_directory"], "Summary_results_FM.pptx")
        st.download_button(label="Download Threholding file", key="download_threholding", 
                           data=open(threholding_file_path, "rb").read(), file_name="Summary_results_T.pptx")
        st.download_button(label="Download Find Maxima file", key="download_find_maxima", 
                           data=open(find_maxima_file_path, "rb").read(), file_name="Summary_results_FM.pptx")

    return

###################################################################################################

# Function to load the second app page which describes the design and layout of the slides

def load_third_page():
    
    return

###################################################################################################

# App main layout and page loading

st.set_page_config(
    page_title="Tool 01 - App by Eduardo",
    page_icon=":newspaper:",
    layout="wide")

st.title("Pptx generator for PLA results")
st.write("---")

# Make a menu of pages on the siderbar, since the app is simple but requires lots of specific details
with st.sidebar:
    selected_page = option_menu("Main Menu", ["How to use the app", "Generate pptx", "Info on pptx design"], 
        icons=["patch-question-fill", "filetype-pptx", "columns-gap"], menu_icon="cast", default_index=1)
    
# Check the selected app page and call the corresponding function to display its content
if selected_page == "How to use the app":
    load_first_page()
elif selected_page == "Generate pptx":
    load_second_page()
else:
    load_third_page() 

# Get the working directory for all functions to write files to it, and download the blank pptx template
st.session_state["current_directory"] = os.path.dirname(os.path.realpath(__file__))
st.session_state["template_pptx"] = os.path.join(st.session_state["current_directory"], "Template.pptx")
if not os.path.exists(st.session_state["template_pptx"]):
    template_dir = "https://github.com/EdRey05/Resources_for_Mulligan_Lab/raw/c71427f2538cb20bac348ed0cc1a59d23053cc36/Tools%20for%20students/Eduardo%20Reyes/Template.pptx"
    urllib.request.urlretrieve(template_dir, st.session_state["template_pptx"])

###################################################################################################