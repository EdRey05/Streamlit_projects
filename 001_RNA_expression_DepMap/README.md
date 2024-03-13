
# Demo of the app 001_RNA_expression_DepMap V07 (V08 works the same but gets the newest files instead)

How to use this app:
1. Open the app hosted in the <a href="https://edrey05-st-app-001.streamlit.app/">Streamlit Community Cloud</a>, running the script with an IDE such as Visual Studio Code or through Github Codespaces (an icon for that is the README of the repo Streamlit_projects).
2. Wait for the app to load and get the files.
3. Search for cell lines of interest, either by name or explore options available for each tissue type (Tip: Try few characters, not the whole name, and avoid special characters).
4. When you see a cell line you want, check its box on the top-right widget. If you change your mind uncheck the box before searching more cell lines.
5. You can go back and fort between the two types of search to select more cell lines. There is no limit on how many/few you choose.
6. Once you finish searching for cell lines, click on the button to Preview results (Note: it may take a few seconds depending on how many cells you selected).
7. A button will appear to allow you to download the dataset (xlsx format, includes the index as the first column, gene names are rows and cell line names are columns).
8. Bonus - Below the two buttons, other widgets will appear in case you want to quickly examine expression of some genes.
9. Bonus -In the bottom-left widgets, you can search for genes of interest in the searchbox (also directly in the dataframe displayed below, but there are >10k rows so scrolling is less efficient).
10. Bonus - Select as many genes as you want through the searchbox, and try to use the dataframe below just to uncheck any (currently, there are interaction issues when going back and forth betweem selecting things in the searchbox and directly in the dataframe, so please do one or the other).
11. Bonus - You will see plots appearing in the bottom-right corner. You can choose between a bar chart or a heatmap, and exchange how the bars are grouped or what is in rows/cols in the heatmap.
12. Bonus - Although the gene expression plots are intended to be for exploratory purposes, you can maximize the dataframe and plot, and even snap pictures from the bar chart and heatmaps! (see demo below).

https://github.com/EdRey05/Streamlit_projects/assets/62916582/e0c16b14-6186-4dca-a4ce-59f275c47677
