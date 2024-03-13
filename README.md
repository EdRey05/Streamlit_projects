
<h2> 003 - Interactive Kaplan-Meier plotter </h2>

<details><summary markdown="span"> Expand this to read more...</summary>
    <div class="two-columns">
        <div class="left-column-35">
            <p><strong> Summary </strong></p>
            <p class="justify-text"> During my graduate studies, I helped two bachelor's students working in my research group to do a small 
                project analyzing survival data from a breast cancer clinical trial. The aim was to assess any <strong>potential correlation</strong> 
                between <strong>higher patient survival</strong> and <strong>low expression of two genes simultaneously</strong>. <br><br>
                For this purpose, we retrieved data publicly available in <strong><a href="https://www.cbioportal.org/">cBioPortal</a></strong>, 
                and generated <strong>Kaplan-Meier survival curves</strong>. We focused on the <strong>METABRIC</strong> dataset containing 
                information for over <strong>2,500 patients</strong> and I generated tools in <strong>Jupyter/Colab notebooks</strong> and a 
                <strong>Streamlit app (see GIF --></strong>) to automate the creation of these plots with <strong>Python</strong>. <br><br>
                At the end of the project, we were able to identify <strong>less than 10 gene pairs</strong> showing the behavior of interest. That 
                information was used in combination with other data from different techniques (<i>in silico</i> and <i>in vitro</i>) to prioritize 
                further studies evaluating the effect of inhibtion of those genes in cancer cell models. <br><br>
            </p>
        </div>
        <div class="right-column-65">
            <br><br>
            <video width="100%" height="auto" autoplay loop muted><source src="Images_GIFs_Videos/Preview_003.mp4" type="video/mp4"></video> 
            <p class="center-text">The app was deployed to the Streamlit Community Cloud, <strong><a href="https://edrey05-st-app-001.streamlit.app/">Click here to check it out!</a></strong></p>
        </div>
    </div>
    <div class="two-columns">
        <div class="left-column-50">
                <p><strong> Problem </strong></p>
                <ul>
                    <li class="justify-text">We needed to generate around <strong>100 Kaplan-Meier plots</strong> (pairs of <strong>RET-other gene
                                            </strong>). </li>
                    <li class="justify-text">Each plot required to divide the dataset into <strong>4 groups</strong> to generate <strong>4 survival 
                                            curves</strong> (expression: <strong>low-low, low-high, high-low, high-high</strong>). </li>
                    <li class="justify-text">The clinical data (<strong>survival times and status</strong>) and the <strong>RNA Seq expression</strong> 
                                            data were in different datasets that have different structure, so pre-processing to both of them was required 
                                            before we could map the patient IDs. </li>
                    <li class="justify-text">We needed to screen all the plots generated but keep only the ones where the <strong>low-low curve</strong>
                                            was higher than the others, and retrieve relevant data such as <strong>CIs and time to 50% survival</strong> 
                                            to complement our analysis. </li>
                    <li class="justify-text">Since each clinical trial reports the data in a different way and not all have RNA Seq data, we chose the 
                                            best possible option for breast cancer (<strong><a href="https://www.cbioportal.org/study/summary?id=brca_metabric">METABRIC</a></strong>). </li> 
                    <li class="justify-text">In order to reuse our code for other breast cancer datasets or even different cancer types, we <strong>needed 
                                            to generalize the workflow</strong> as much as possible and <strong>make tools for reproducibility and 
                                            automation</strong>. </li>
                </ul>
        </div>
        <div class="right-column-50">
            <p><strong> Solution </strong></p>
            <ul> 
                <li class="justify-text">I learned how to use the <strong>KaplanMeierFitter</strong> module from the <strong>lifelines</strong> python 
                                        library to generate KM plots. </li>
                <li class="justify-text">I first generated a <strong>Google Colab notebook</strong> that was dataset-specific to produce batches of 
                                        <strong>40-50</strong> plots. This <strong>exclusively makes 4 groups</strong> from the original dataset based 
                                        on the expression of RET and one other gene, which required to manually write in the code all 40-50 names of the
                                        other gene (<strong><a href="https://user-images.githubusercontent.com/62916582/204424020-bae3613c-bf10-4a3b-9d50-beaf50ca8eee.gif" target="_blank">View tool</a></strong>). </li>
                <li class="justify-text">Then, I found a way to generalize some steps and created a <strong>Jupyter notebook</strong> that used
                                        <strong>ipywidgets</strong> to <strong>interactively get user inputs</strong>, allowing dynamic selection of 
                                        <strong>any measured variable</strong> to divide the dataset into <strong>2 or more groups</strong> and 
                                        re-plotting curves easily (<strong><a href="https://github.com/EdRey05/Resources_for_Mulligan_Lab/blob/de82796fe821b96c18ab0709018c02c3b02aba92/Tutorials/Preview_Interactive_KM.gif" target="_blank">View tool</a></strong>). </li>
                <li class="justify-text">Finally, I discovered <strong>Streamlit</strong> and adapted my interactive notebook to a <strong>data app</strong> 
                                        (GIF above) that used a similar approach but has <strong>more interactivy, improved outputs and better user                                                                                                         experience</strong>. </li>
                <li class="justify-text">Although the app works well for several datasets, I noticed <strong>high variability in the formatting of clinical
                                        trial data</strong>, and try to improve my app to generalize it more!. </li>
            </ul>
        </div>
    </div>
    <p><strong> Read the instructions and watch another demo of the Streamlit app here: <a href="https://github.com/EdRey05/Streamlit_projects/tree/main/003_KM_plotter">Demo_KM_plotter</a></strong></p>
</details>

<hr>

<h2> 002 - Automated Power Point generator</h2>

<details><summary markdown="span"> Expand this to read more...</summary>
    <div class="two-columns">
        <div class="left-column-35">
            <p><strong> Summary </strong></p>
            <p class="justify-text"> During my graduate studies, I performed <strong>fluorescence microscopy experiments</strong>, acquiring images of 
                cancer cells <i>in vitro</i>. Typical analysis involved <strong>co-localization</strong> between signals produced by proteins, or 
                <strong>object/particle counting</strong>. <br><br>
                For <strong>Proximity Ligation Assay (PLA)</strong> experiments, which evaluate <strong>protein-protein interactions</strong>, I used 
                a <strong>EVOS M7000 </strong> cell imager to automate the acquisition of thousands of images. I wrote scripts in <strong>Jython</strong> 
                (Python wrapper for Java) to automate image processing and analysis in the <strong>ImageJ/Fiji</strong> software. The outputs are a 
                <strong>csv file with the object count for each individual cell</strong> and pairs of <strong>fluorescence + object mask images</strong> 
                (the latter shows particles as colored blobs if met the criteria to be counted). <br><br>
                I designed a tool to <strong>consolidate all the outputs</strong> for each experimental group into a summary Power Point presentation so 
                we could validate the parameters using during the workflow. I automated the creation of slides using the <strong>python-pptx</strong> 
                library, designing a <strong>custom layout</strong> and inserting relevant information. I created first a tool in the form of a 
                <strong>Google Colab notebook</strong> and then as a <strong>Streamilt app</strong>. This tool helped me visualize outputs for <strong>
                almost 10,000 images</strong>, easily <strong>compare two quantification methods, and fully optimize the whole workflow</strong>. <br><br>
            </p>
        </div>
        <div class="right-column-65">
            <br><br>
            <img src="Images_GIFs_Videos/Preview_002.gif" alt="Streamlit Projects 002 GIF" />
            <p class="center-text">The app was deployed to the Streamlit Community Cloud, <strong><a href="https://edrey05-st-app-002.streamlit.app/">Click here to check it out!</a></strong></p>
        </div>
    </div>
    <div class="two-columns">
        <div class="left-column-50">
            <p class="justify-text"><strong> Problem </strong></p>
            <ul> 
                <li class="justify-text">Manually inserting, resizing, arranging and labeling all the images is incredibly <strong>time consuming and 
                                        prone to errors</strong>. </li>
                <li class="justify-text"><strong>ImageJ/Fiji is not fully compatible with Python 3 code</strong>, so I could not integrate a feasible 
                                        solution into my other Jython scripts. </li>
                <li class="justify-text">Each experimental group may be <strong>quantified by both methods, one or the other</strong>. </li>
                <li class="justify-text">Depending on the quantification type, the output <strong>csv may contain less/additional columns</strong>. </li>
                <li class="justify-text">The real image labels are in the csv alongside their count numbers, however, the fluorescence images are in one
                                        subdirectory and adds a "_2" to their name, whereas the object mask image is in a different subdirectory and adds
                                        a "_1" to their name (may be one or two sets of object masks, one for each quantification method used). </li>
                <li class="justify-text">Due to the large number of images quantified per experimental group (<strong>100-500</strong>) we needed an 
                                        <strong>efficient layout</strong>, balancing image visibility and number of slides (<strong>fewer slides = faster 
                                        review</strong>). </li>
                <li class="justify-text">Since our research group was planning on doing several more PLA experiments, <strong>automation</strong> was 
                                        essential. </li>
            </ul>
        </div>
        <div class="right-column-50">
            <p class="justify-text"><strong> Solution </strong></p>
            <ul> 
                <li class="justify-text">I manually tested different arrangements of images + labels in rows and columns until <strong>I set one layout 
                                        that best worked for the type and amount of data I had</strong> (see app info page). </li>
                <li class="justify-text">I <strong>measured and defined each item's coordinates</strong> and dove in the documentation of python-pptx to 
                                        figure out how to make that very specific layout (see app info page). </li>
                <li class="justify-text">I generated the neccesary code to scan through a zip file in search for csv files, then read the content and go back 
                                        to the root directory for that experimental group to find the pairs of images to insert. </li>
                <li class="justify-text">A big iterable is generated with names, counts, and image locations which are analyzed to separate in groups of
                                        up to 20 for a single slide (see app info).  </li>
                <li class="justify-text">I implemented this approach first in a <strong>Google Colab notebook</strong> (<strong><a href="https://user-images.githubusercontent.com/62916582/204415085-cc39bb7c-904e-487c-a16d-0d894c1e3249.gif" target="_blank">View tool</a></strong>) and then created a <strong>Streamlit app</strong> (GIF above). The app has the <strong>same functionality 
                                        </strong> but <strong>better user experience</strong>, especially to read additional info on the input/output and the 
                                        design of the slides. </li>
                <li class="justify-text">The app allows <strong>quick and easy automation</strong>, as the user only needs to upload a <strong>zip file with as 
                                        many experimental group folders as desired</strong> (with the outputs of my quantification script), and indicate the 
                                        quantification method in the app. </li>
            </ul>
        </div>
    </div>
    <p><strong> Read the instructions and watch another demo of the Streamlit app here: <a href="https://github.com/EdRey05/Streamlit_projects/tree/main/002_Automated_PPTX_PLA">Demo_PPTX_PLA</a></strong></p>
</details>

<hr>

<h2> 001 - Interactive extraction of RNA Seq data from CCLE/DepMap </h2>

<details><summary markdown="span"> Expand this to read more...</summary>
    <div class="two-columns">
        <div class="left-column-35">
            <p><strong> Summary </strong></p>
            <p class="justify-text"> During my graduate studies, I came across the <strong><a href="https://depmap.org/portal/ccle/">Cancer Cell Line 
                Encyclopedia</a></strong>, which is a project containing information on <strong>over 1,800 cell models</strong>, including <strong>RNA 
                Seq gene expression</strong> data (<strong>around 20,000 genes</strong>). <br><br>
                I created a basic tool as a <strong>Google Colab notebook</strong> (<strong><a href="https://user-images.githubusercontent.com/62916582/204422004-47fe5726-d92d-4193-bc6a-ea30b3a93cc1.gif">View tool</a></strong>) to search and retrieve only cell lines of interest (we usually only needed <10). However, years later I noticed that the dataset was 
                merged with the <strong>Achilles project</strong> to make the <strong><a href="https://depmap.org/portal/download/all/">DepMap project</a></strong>. 
                This added few more cell lines but several more datasets from diverse genomics, proteomics, and metabolomics assays. They also reshaped 
                datasets, reassigned IDs to make all datasets consistent, etc. I adapted my tool to work for the new version (<strong>at that time, 
                23Q2</strong>), and generated a similar notebook. <br><br>
                Finally, when I discovered <strong>Streamlit</strong> I built a data app to replicate my notebook tool. I realized how easy was to add 
                widgets and interactive plots that would allow not only to extract the data, but also to <strong>automate basic exploration and 
                visualization</strong> of the cell lines and gene expression in a very user-friendly manner. <br><br>
            </p>
        </div>
        <div class="right-column-65">
            <br><br>
            <img src="Images_GIFs_Videos/Preview_001.gif" alt="Streamlit Projects 001 GIF" />
            <p class="center-text">To see in full screen, right click on image and select "Open in new tab" </p>
        </div>
    </div>
    <div class="two-columns">
        <div class="left-column-50">
            <p class="justify-text"><strong> Problem </strong></p>
            <ul> 
                <li class="justify-text">The RNA Seq dataset is very large and it no longer has cell line names, as they were changed to Achilles IDs which are
                                        encoded in another file. </li>
                <li class="justify-text">We needed to pre-process both datasets before mapping the IDs, but asking the user to get the required files from the
                                        website was confusing and led to errors as the <strong>datasets change 2-4 times a year</strong>. </li>
                <li class="justify-text">The notebook tool required the user to have the required files already <strong>stored in a specific Google Drive folder 
                                        </strong> (or to have access to a Google account that had them). </li>
                <li class="justify-text">The notebook tool was <strong>only able to search based on cell line name</strong>, but sometimes we needed just to explore 
                                        what models are available for some tissues. </li>
                <li class="justify-text">The notebook tool only provided a <strong>simple view of the search results</strong> showing the cell line name followed 
                                        by tissue, no more information. </li>
                <li class="justify-text">While the notebook tool provided some degree of automation, it was not easy to de-select cell lines and <strong>only gave 
                                        the raw data for the user to plot or analyze</strong>. </li>
            </ul>
        </div>
        <div class="right-column-50">
            <p class="justify-text"><strong> Solution </strong></p>
            <ul> 
                <li class="justify-text">I set the Streamlit app to <strong>automatically download the required files</strong> for the current release at the time 
                                        (<strong>23Q2</strong>). It takes like a minute or two, but the user does not need any Google account, nor to upload anything
                                        to be able to use the app. </li>
                <li class="justify-text">The pre-processing is tailored to that specific data release and caches the prepared dataframe to improve efficiency. </li>
                <li class="justify-text">I <strong>added a second search mode</strong>, so the user can search names of cell lines (or parts of them), and also search
                                        by tissue type. </li>
                <li class="justify-text">The app displays more interactive search results, allowing to check boxes of cell lines to keep (instead of intering numbers)
                                        and I provide the <strong>Achilles ID, clean cell line name, tissue type and cancer type</strong>. </li>
                <li class="justify-text">The csv output is the same as the notebook tool, however, the app has several widgets to preview the selected data. </li>
                <li class="justify-text">Although it is not perfect, the preview area <strong>shows the generated dataset</strong> and lets the user easily <strong>type 
                                        in genes of interest to make a bar chart or a heatmap</strong>. These visualizations are interactive (plotly) and the user can 
                                        take snapshots if needed. </li>
            </ul>
        </div>
    </div>
    <p><strong> <u>NOTE:</u> I am not planning on deploying my app to a hosted server (for now), it runs locally or in Github Codespaces (see last section).</strong></p>
    <p><strong> Read the instructions and watch another demo of the Streamlit app here: <a href="https://github.com/EdRey05/Streamlit_projects/tree/main/001_RNA_expression_DepMap">Demo_RNA_DepMap</a></strong></p>
</details>

<hr>

<h2> Try out my apps with Github Codespaces! </h2>

<details><summary markdown="span"> Expand this to read more...</summary>
    <div class="two-columns">
        <div class="left-column-35">
            <br>
            <p class="justify-text"> If you have a Github account, you can create a <strong>Github Codespace</strong> with all the requirements to 
                run my apps. You only have to log into you account, click on the button below, create your Codespace (<strong>we all have 60h of 
                free usage per month!</strong>), and follow the instructions in this video→. <br><br>
                ***Due to size limits, I did everything in the video quickly but added notes so pause, read and see where I clicked! <br><br></p>
            <div class="center-text">
                <a href="https://codespaces.new/EdRey05/Streamlit_projects?quickstart=1" target="_blank">
                    <img src="https://github.com/codespaces/badge.svg" alt="Open in GitHub Codespaces">
                </a>
            </div>
            <br>
            <p class="justify-text"><strong>Download sample files to test the apps:</strong></p>
            <p class="justify-text">(button on the right side, by the pencil)</p>
            <ul>
                <li class="justify-text">App 001 - Does not require.</li>
                <li class="justify-text"><strong><a href="https://github.com/EdRey05/Streamlit_projects/blob/main/Test_units/Project%20002/Data_Both.zip">App 002</a></strong> - Rename to "data.zip" first.</li>
                <li class="justify-text"><strong><a href="https://github.com/EdRey05/Streamlit_projects/blob/main/Test_units/Project%20003/clinical_METABRIC.txt">App 003</a></strong> - Rename to "clinical.txt"                                             first.</li>
            </ul>
        </div>
        <div class="right-column-65">
            <br>
            <video width="100%" height="auto" controls><source src="Images_GIFs_Videos/Demo_Codespaces.mp4" type="video/mp4"></video>
        </div>
    </div>
</details>
