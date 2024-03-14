# Demo of the app 003_KM_plotter V11

How to use this app (see video below):
1. Open the app hosted in the <a href="https://edrey05-st-app-002.streamlit.app/">Streamlit Community Cloud</a>, running the script with an IDE such as Visual Studio Code or through Github Codespaces (an icon for that is the README of the repo Streamlit_projects). Wait for the app to load.
2. Rename the file containing the clinical data (or a cop of it) to 'clinical.txt', this is a mandatory file containing the times and events for the KM analysis.
3. Optionally, you can also upload a file containing RNA Seq data of the patients with a name 'RNA.txt'. Be sure a 'PATIENT_ID' column exists in both datasets and that these IDs are the same (not two sets of IDs).
4. Once the file(s) of interest is/are uploaded, click on 'Begin' and start selecting the parameters of interest.
5. You must select a column containing a time for an event, and the app will show you which columns were found in your clinical file (typically in the fromat 'x_MONTHS', where x could be OS/PFS/RFS, etc.).
6. You must select the event to observe (patient status) for the time column selected (usually comes in matching name pairs like OS_MONTHS, OS_STATUS).
7. Alternatively, some additional event columns may be shown (like VITAL_STATUS, or CAUSE_OF_DEATH), and these might be useful to remove patients who died from causes other than the associated to their cancer.
8. You must explicitely select the event from the column you selected in the additional widgets, where 0=No event observed, and 1=Event (died/dead/recurred/progressed,etc.).
9. You can decide and select in the last widget to make subgroups (Using variable(s)) or not (None). If you don't need, the whole dataset will be used to make a single curve (NaN's on time+event columns are filtered out).
10. You can click 'Generate/Update plot' now to get you plot and additional buttons to download it as an image and to download the data in an excel file (event table + survival curve + confidence intervals + median survival time).
11. Also, notice the plot customization tools that are shown in the sidebar, remember that you can change them but must press the button again ('Generate/Update plot').
12. Alternatively, you can divide the dataset to gain further insights by analyzing the survival curves of patients with different treatments, age, or gene expression. For that, select to make subgroups 'Using variable(s)'.
13. Choose the number of variables to make subrgoups by (1-5), and make sure you fill out all the widgets that appear, from left to right. First select the dataset, then the column, then the number of subgroups and their values/labels.
14. Notice that you can change the number of variables and groups per variable, but these will multiply the number of curves as there will be combinations (2 variables with 3 subgroups each will result in 9 curves, not 6, so keep that in mind).
15. To avoid errors, make sure no widget is left without selection. If you no longer need subgroups (1-5) or variables (1-5), decrease the corresponding slider to make them disappear.
16. Make sure the sliders do not have overlapping ranges (for fine tunning, you can drag the circle and then use the arrows in your keyboard to go higher/lower in small steps).
17. Once you have defined the variables and subgroups, generate or update your plot and customize it.
18. Notice most plots are partially interactive, so you can easily exlpore variables/columns, see NaN's, patients on each category, and the distribution of numeric values to choose appropriate ranges.
19. Finally, this app just automates KM plots using the KaplanMeierFitter module from the lifelines library. It is assumed the user knows how to select appropriate parameters and interpret the results of this type of survival analysis.
 
NOTES: 
* If you intend to use a big RNA Seq file (>200mb), it would be best if you download the app and the ".streamlit" folder to run it locally (seems that Codespaces is not obeying my config file). 
* The app will generate a log file 'MyLog.txt' every time it is used (with lots of information), but feel free to disregard/delete this file as it might be useful for debugging but the logging has not been fully optimized for Streamlit (the app was a Jupyter notebook before).

https://github.com/EdRey05/Streamlit_projects/assets/62916582/144aab3c-15e8-4894-acd9-6acd7d07894e
