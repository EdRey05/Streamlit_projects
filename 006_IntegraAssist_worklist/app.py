'''
App made by:
    Eduardo Reyes Alvarez, Ph.D.
Contact:
    ed5reyes@outlook.com

App version: 
    V01 (Aug 18, 2024): First partial version of the app.
 
'''
###############################################################################

# Import the required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image, ImageDraw

# Streamlit App setup
st.set_page_config(
    page_title="Tool 006 - App by Eduardo",
    page_icon=":bar_chart:",
    layout="wide")
st.title("Create worklist for Integra liquid handler")
st.markdown('<hr style="margin-top: +5px; margin-bottom: +5px;">', unsafe_allow_html=True)

###############################################################################
########## OPTION A
st.subheader("Option A")

# Function to draw and save the culture plate as an image
def draw_culture_plate():
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Set up rectangle dimensions
    rect_width = 10
    rect_height = 6
    cut_corner_size = 0.5  # Make the diagonal cut smaller (closer to the corner)
    
    # Define the polygon's vertices (for the shape without the top-left corner)
    polygon_points = [
        (0, 0),  # Bottom-left corner
        (rect_width, 0),  # Bottom-right corner
        (rect_width, rect_height),  # Top-right corner
        (cut_corner_size, rect_height),  # Start of diagonal cut (moving left)
        (0, rect_height - cut_corner_size)  # End of diagonal cut (moving down)
    ]
    
    # Create the polygon with these points (no border on the diagonal)
    culture_plate_polygon = patches.Polygon(
        polygon_points, closed=True, color="#D3D3D3", edgecolor="black", linewidth=2
    )
    ax.add_patch(culture_plate_polygon)
    
    # Draw the 96 circles (8 rows and 12 columns)
    num_rows = 8
    num_cols = 12
    circle_radius = 0.3  # Radius of each circle
    padding = 0.1  # Padding between circles
    
    # Calculate space for labels (leave some margins around the edges)
    label_margin = 0.5  # Margin space for labels on all sides
    well_width = (rect_width - 2 * label_margin - (num_cols - 1) * padding) / num_cols
    well_height = (rect_height - 2 * label_margin - (num_rows - 1) * padding) / num_rows
    
    # Coordinates for the circles: we calculate the center of each circle
    for i in range(num_rows):
        for j in range(num_cols):
            # Center coordinates of each circle
            x = label_margin + j * (well_width + padding) + well_width / 2
            y = label_margin + i * (well_height + padding) + well_height / 2
            
            # Draw the circle
            circle = patches.Circle((x, y), circle_radius, color="white", ec="black", lw=1)
            ax.add_patch(circle)
            
            # Label the circle (e.g., A01, A02, ..., H12)
            row_label = chr(72 - i)  # Convert 0 -> "H", 1 -> "G", ..., 7 -> "A"
            col_label = str(j + 1)  # Column numbers: 1 to 12
            label = f"{row_label}{col_label}"
            
            # Place the label in the center of the circle
            ax.text(x, y, label, ha="center", va="center", fontsize=6)

    # Add Row Labels (A to H) on the left (vertical)
    row_labels = ["H", "G", "F", "E", "D", "C", "B", "A"]
    for i, label in enumerate(row_labels):
        # Row labels positioned just to the left of the first column, moved slightly up
        ax.text(-label_margin, label_margin + i * (well_height + padding) + 0.15, 
                label, ha="center", va="center", fontsize=10, fontweight="bold")
    
    # Add Column Labels (1 to 12) at the top (horizontal)
    col_labels = [str(i+1) for i in range(num_cols)]
    for i, label in enumerate(col_labels):
        # Column labels positioned just above the first row, moved slightly to the right
        ax.text(label_margin + i * (well_width + padding) + 0.3, rect_height + label_margin, 
                label, ha="center", va="center", fontsize=10, fontweight="bold")
    
    # Set the axis limits and remove axes
    ax.set_xlim(-1, rect_width + 1)
    ax.set_ylim(-1, rect_height + 1)
    ax.set_aspect("equal")
    ax.axis("off")  # Hide the axis

    # Save the figure twice as png and save its size
    fig.savefig("96well_plate.png", dpi=300, bbox_inches="tight")
    fig.savefig("clicked_fig.png", dpi=300, bbox_inches="tight")
    st.session_state["fig_size"] = fig.get_size_inches()
    plt.close(fig)

    # Save the path to the original figure in the session state
    st.session_state["original_fig"] = "96well_plate.png"
    st.session_state["clicked_fig"] = "clicked_fig.png"
    
# Function to calculate the center coordinates of each well
def calculate_well_centers():
    centers = []
    num_rows = 8
    num_cols = 12
    rect_width = 10
    rect_height = 6
    padding = 0.1
    label_margin = 0.5

    # Calculate space for each well
    well_width = (rect_width - 2 * label_margin - (num_cols - 1) * padding) / num_cols
    well_height = (rect_height - 2 * label_margin - (num_rows - 1) * padding) / num_rows

    # Calculate center coordinates for each well
    for i in range(num_rows):
        for j in range(num_cols):
            # Center coordinates of each circle
            x = label_margin + j * (well_width + padding) + well_width / 2
            y = label_margin + i * (well_height + padding) + well_height / 2
            row_label = chr(72 - i)  # Convert 0 -> "H", 1 -> "G", ..., 7 -> "A"
            col_label = str(j + 1)
            well_label = f"{row_label}{col_label}"
            
            centers.append((x, y, well_label))

    # Save the well centers to the session state
    st.session_state["well_centers"] = centers

# Function to find the closest well to the clicked coordinates
def find_clicked_well(coords, img_size):
    if coords is None:
        return None

    # Image dimensions in pixels
    img_width, img_height = img_size

    # Retrieve well centers
    well_centers = st.session_state["well_centers"]
    
    # Adjusted scaling factors for your image dimensions
    scale_x = 10 / img_width
    scale_y = 6 / img_height

    # Convert the clicked image coordinates to the figure's coordinate space
    x_fig = coords["x"] * scale_x
    y_fig = (img_height - coords["y"]) * scale_y  # Adjust or remove y-axis flip if needed

    # Define a tolerance around the center of each well
    circle_radius = 0.3  # This should match the radius used in draw_culture_plate
    tolerance = circle_radius * 1.5  # Adjust tolerance as needed

    # Check if the click falls within any well's bounding area
    for x_center, y_center, label in well_centers:
        if (x_fig >= x_center - tolerance and x_fig <= x_center + tolerance and
            y_fig >= y_center - tolerance and y_fig <= y_center + tolerance):

            # Save identified well label to the session state
            st.session_state["source_well1"] = label
            return (x_center, y_center, label)
    return None

# Make the initial plate image and calculate the centers
if "original_fig" not in st.session_state:
    draw_culture_plate()
    calculate_well_centers()

# Make column layout for required widgets
row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)
row2_col1, row2_col2 = st.columns(2)
row3_col1, row3_col2, row3_col3, row3_col4, row3_col5 = st.columns([4, 1, 1, 1, 1])

# Display widgets to enter sample information
with row1_col1:
    gene_ID1 = st.text_input("Gene ID", key="gene_ID1", placeholder="None")
with row1_col2:
    source_spot1 = st.selectbox("Source Spot", options=["A", "B", "C"], index=1, key="source_spot1")
with row1_col3:
    target_spot1 = st.selectbox("Target Spot", options=["A", "B", "C"], index=2, key="target_spot1")
with row1_col4:
    transfer_volume1 = st.slider("Transfer Volume", min_value=5, max_value=500, step=5, value=85, key="transfer_volume1")

# Display the plate image and duplicate image to get click coordinates
with row2_col1:
    clicked_coordinates = streamlit_image_coordinates(st.session_state["clicked_fig"], 
                                                    key="clicked_coordinates", use_column_width=True)

# Implement logic for coordinate detection
if clicked_coordinates:
    img_size = st.session_state["fig_size"]
    temp_image = Image.open(st.session_state["clicked_fig"])
    clicked_well = find_clicked_well(clicked_coordinates, img_size)
    st.warning(clicked_well)

    if clicked_well:
        x_center, y_center, well_label = clicked_well
        
        # Draw the aqua circle on the temp_image
        draw = ImageDraw.Draw(temp_image)
        img_width, img_height = img_size

        # Convert figure coordinates back to image coordinates
        x_img = int((x_center / 10) * img_width)
        y_img = int(((6 - y_center) / 6) * img_height)  

        # Draw a circle and white text for the well
        circle_radius = int((0.25 / 10) * img_width)  # Adjust radius to image scale
        draw.ellipse(
            [(x_img - circle_radius, y_img - circle_radius),
            (x_img + circle_radius, y_img + circle_radius)],
            outline="black", fill="darkblue"
        )
        draw.text((x_img, y_img), well_label, fill="white", anchor="mm")

        # Update the clicked image png
        temp_image.save(st.session_state["clicked_fig"], "PNG")
        st.rerun()

# Show additional widgets to preview and add or clear the selection
with row3_col1:
    st.success(f"Transfer sample {st.session_state["gene_ID1"]} from {st.session_state.get('source_well1', 'None')} to ")
with row3_col2:
    add_to_worklist1 = st.button("Add sample", type="primary", key="add_to_worklist1")
with row3_col3:
    clear_selections = st.button("Clear Selections", type="primary")
with row3_col4:
    show_worklist1 = st.button("Show Worklist", type="primary", key="show_worklist1")

# Add current selection and sample info to worklist
if add_to_worklist1:
    df1 = st.session_state.get("df1", 
                            pd.DataFrame(columns=["Gene_ID", "Source_spot", "Source_well", 
                                    "Target_spot", "Target_well", "Transfer_volume"]))
    new_row = {"Gene_ID": gene_ID1, 
                "Source_spot": source_spot1, "Source_well": st.session_state["source_well1"], 
                "Target_spot": target_spot1,
                #"Target_well": st.session_state["target_well1"],
                "Transfer_volume": transfer_volume1}
    df1 = pd.concat([df1, pd.DataFrame([new_row])], ignore_index=True)
    st.session_state["df1"] = df1

# To clear selections, overwrite the original png to the clicked png
if clear_selections:
    reset_fig = Image.open(st.session_state["original_fig"])
    reset_fig.save(st.session_state["clicked_fig"], "PNG")
    st.rerun()

# Show worklist
if show_worklist1:
    st.dataframe(st.session_state["df1"])
    with row3_col5:
        download_worklist1 = st.download_button("Download Worklist", 
                                        data=st.session_state["df1"].to_csv(index=False), 
                                        file_name="worklist.csv", mime="text/csv", 
                                        type="primary", key="download_worklist1")

###############################################################################
########## OPTION B
st.markdown('<hr style="margin-top: +15px; margin-bottom: +15px;">', unsafe_allow_html=True)
st.subheader("Option B")

# Initialize a grid with 8 rows (A to H) and 12 columns (1 to 12)
rows = ["A", "B", "C", "D", "E", "F", "G", "H"]
columns_96 = range(1, 13)
row4_col1, row4_col2, row4_col3, row4_col4 = st.columns(4)
columns_48 = range(1, 7)
row5_col1, row5_col2, row5_col3 = st.columns([2.5, 0.25, 1.25])

# Display widgets to enter sample information
with row4_col1:
    gene_ID2 = st.text_input("Gene ID", key="gene_ID2", placeholder="None")
with row4_col2:
    source_spot2 = st.selectbox("Source Spot", options=["A", "B", "C"], index=1, key="source_spot2")
with row4_col3:
    target_spot2 = st.selectbox("Target Spot", options=["A", "B", "C"], index=2, key="target_spot2")
with row4_col4:
    transfer_volume2 = st.slider("Transfer Volume", min_value=5, max_value=500, step=5, value=85, key="transfer_volume2")

# Create buttons in a grid
for row in rows:
    # Generate the buttons for the 96-well plate
    with row5_col1:
        cols_1to12 = st.columns(12)

        for col_index, col in enumerate(columns_96):
            # Generate button label (e.g., A1, B2, etc.)
            button_label = f"{row}{col}"
            # Display button in the appropriate column ]
            with cols_1to12[col_index]:
                if st.button(button_label, key=button_label+"_96",):
                    # Update session state when a button is clicked
                    st.session_state["source_well2"] = button_label
    
    # Generate the buttons for the 48-well plate
    with row5_col3:
        cols_1to6 = st.columns(6)
        for col_index2, col2 in enumerate(columns_48):
            # Generate button label (e.g., A1, B2, etc.)
            button_label2 = f"{row}{col2}"
            # Display button in the appropriate column ]
            with cols_1to6[col_index2]:
                if st.button(button_label2, key=button_label2+"_48"):
                    # Update session state when a button is clicked
                    st.session_state["target_well2"] = button_label2

# Show additional widgets to preview and add or clear the selection
row6_col1, row6_col2 = st.columns([3, 1])
row7_col1, row7_col2 = st.columns([4, 1])
with row6_col1:
    st.success(f"Transfer sample {st.session_state["gene_ID2"]} from {st.session_state.get('source_well2', 'None')} to {st.session_state.get('target_well2', 'None')}")
with row6_col2:
    add_to_worklist2 = st.button("Add sample", type="primary", key="add_to_worklist2")

if "df2" in st.session_state:
    with row7_col1: 
        st.dataframe(st.session_state["df2"], use_container_width=True)
    
    final_worklist2 = st.session_state["df2"]["Automation_string"]
    final_worklist2 = final_worklist2.rename("SampleID;SourceDeckPosition;SourceWell;TargetDeckPosition;TargetWell;TransferVolume [µl]")
    
    with row7_col2: 
        worklist2_name = st.text_input("Save worklist as")
        download_worklist2 = st.download_button("Download Worklist", 
                                            data=final_worklist2.to_csv(index=False), 
                                            file_name=f"{worklist2_name}.csv", mime="text/csv", 
                                            type="primary", key="download_worklist2")
    
# Add current selection and sample info to worklist
if add_to_worklist2:
    df2 = st.session_state.get("df2", 
                            pd.DataFrame(columns=["Gene_ID", 
                                                "Source_spot", "Source_well", 
                                                "Target_spot", "Target_well", 
                                                "Transfer_volume",
                                                "Automation_string"]))
    new_row2 = {"Gene_ID": gene_ID2, 
                "Source_spot": source_spot2, "Source_well": st.session_state["source_well2"], 
                "Target_spot": target_spot2, "Target_well": st.session_state["target_well2"],
                "Transfer_volume": transfer_volume2,
                "Automation_string": f"{gene_ID2};{source_spot2};{st.session_state['source_well2']};{target_spot2};{st.session_state['target_well2']};{transfer_volume2}"}
    df2 = pd.concat([df2, pd.DataFrame([new_row2])], ignore_index=True)
    st.session_state["df2"] = df2
    st.rerun()

###############################################################################
########## BULK MODE

# Create column layout for required widgets
st.markdown('<hr style="margin-top: +15px; margin-bottom: +15px;">', unsafe_allow_html=True)
st.subheader("Bulk Mode")
df3 = pd.DataFrame(columns=["Gene_name", "Vplate", "Seq_well"], index=range(96))
row8_col1, row8_col2 = st.columns([4, 1])
row9_col1, row9_col2 = st.columns([4, 1])

with row8_col1:
    temp_df = st.data_editor(df3, use_container_width=True, key="temp_df")

with row8_col2:
    source_spot3 = st.selectbox("Source Well", options=["A", "B", "C"], index=1)
    target_spot3 = st.selectbox("Target Well", options=["A", "B", "C"], index=2)
    transfer_volume3 = st.slider("Transfer Volume", min_value=5, max_value=500, step=5, value=85)
    convert = st.button("Convert to worklist", type="primary")

if convert or "df3" in st.session_state:
    converted_df = temp_df.copy()
    converted_df["Source_well"] = converted_df["Vplate"].str.slice(7)
    converted_df["Target_well"] = converted_df["Seq_well"].str.replace(r"[#\(\)]", "", regex=True)
    converted_df["Source_spot"] = source_spot3
    converted_df["Target_spot"] = target_spot3
    converted_df["Transfer_volume"] = transfer_volume3
    converted_df["Automation_string"] = converted_df.apply(lambda row: f"{row["Gene_name"]};{row["Source_spot"]};{row["Source_well"]};{row["Target_spot"]};{row["Target_well"]};{row["Transfer_volume"]}", axis=1)
    st.session_state["df3"] = converted_df
    with row9_col1:
        row3_col1.empty()
        st.dataframe(st.session_state["df3"], use_container_width=True)

    with row9_col2:
        final_worklist3 = st.session_state["df3"].dropna()
        final_worklist3 = final_worklist3["Automation_string"]
        final_worklist3 = final_worklist3.rename("SampleID;SourceDeckPosition;SourceWell;TargetDeckPosition;TargetWell;TransferVolume [µl]")
        worklist3_name = st.text_input("Worklist Name", key="worklist3_name")
        download_worklist3 = st.download_button("Download Worklist", 
                                            data=final_worklist3.to_csv(index=False), 
                                            file_name=f"{worklist3_name}.csv", mime="text/csv", 
                                            type="primary", key="download_worklist3")
