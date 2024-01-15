
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
                information was used in combination with other data from different techniques (in-silico and wet-lab) to prioritize further 
                studies evaluating the effect of inhibtion of those genes in cancer cell models. </p>
        </div>
        <div class="right-column-65">
            <video width="100%" height="auto" autoplay loop muted><source src="Images_GIFs_Videos/Preview_003.mp4" type="video/mp4"></video> 
        </div>
    </div>
    </p>
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
                                        other gene (<a href="https://user-images.githubusercontent.com/62916582/204424020-bae3613c-bf10-4a3b-9d50-beaf50ca8eee.gif" target="_blank">View tool</a>). </li>
                <li class="justify-text">Then, I found a way to generalize some steps and created a <strong>Jupyter notebook</strong> that used
                                        <strong>ipywidgets</strong> to <strong>interactively get user inputs</strong>, allowing dynamic selection of 
                                        <strong>any measured variable</strong> to divide the dataset into <strong>2 or more groups</strong> and 
                                        re-plotting curves easily (<a href="https://github.com/EdRey05/Resources_for_Mulligan_Lab/blob/de82796fe821b96c18ab0709018c02c3b02aba92/Tutorials/Preview_Interactive_KM.gif" target="_blank">View tool</a>). </li>
                <li class="justify-text">Finally, I discovered <strong>Streamlit</strong> and adapted my interactive notebook to a <strong>data app</strong> 
                                        (GIF above) that used a similar approach but has <strong>more interactivy, improved outputs and better user                                                        experience</strong>. </li>
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
            <p class="justify-text"> During my graduate studies, I performed numerous <strong>fluorescence microscopy experiments</strong>. These 
                experiments required to acquire sufficient images of individual cancer cells, process them and analyze them. Typical analysis of my 
                experiments would involve <strong>co-localization</strong> between signals on different channels, or <strong>object/particle detection 
                and counting</strong>. <br><br>
                I carried out <strong>Proximity Ligation Assay (PLA)</strong> experiments to evaluate <strong>protein-protein interactions</strong> 
                using a cell imager (<strong>EVOS M7000 - Thermo Fisher</strong>) that has automated imaging features. I automated the acquisition of 
                hundreds of images, and wrote scripts in <strong>Jython</strong> (Python wrapper for Java) to automate the image pre-processing and 
                analysis in <strong>ImageJ/Fiji</strong>. The final output of my series of scripts was a <strong>csv file with the quantification 
                result for each individual cell</strong> and the <strong>cropped images with their object mask image</strong> (shows colored blobs 
                which are particles both detected and counted). <br><br>
                To <strong>validate the quantification results</strong> before proceeding to statistical analysis, I designed a tool to <strong>consolidate 
                all the outputs</strong> into a summary Power Point presentation. I automated the creation of slides with a <strong>customized layout
                </strong> and insertion of fluorescence + object mask <strong>image pairs with their names and quantification results</strong> using 
                the <strong>python-pptx</strong> library. <br><br>
                I created a tool first in the form of a <strong>Google Colab notebook</strong> and then as a <strong>Streamilt data app</strong> which
                helped me analyze outputs for <strong>almost 10,000 images</strong>. With this tool, I was able to easily <strong>compare two quantification 
                methods, test different pre-processing and object detection parameters, and fully optimize the whole workflow for each experiment</strong>.
            </p>
        </div>
        <div class="right-column-65">
            <img src="Images_GIFs_Videos/Preview_002.gif" alt="Streamlit Projects 002 GIF" />
        </div>
    </div>
    <div class="two-columns">
        <div class="left-column-50">
            <p class="justify-text"><strong> Problem </strong></p>
            <ul> 
                <li class="justify-text"> A. </li>
                <li class="justify-text"> B. </li>
                <li class="justify-text"> C. </li>
                <li class="justify-text"> D. </li>
                <li class="justify-text"> E. </li>
                <li class="justify-text"> F. </li>
            </ul>
        </div>
        <div class="right-column-50">
            <p class="justify-text"><strong> Solution </strong></p>
            <ul> 
                <li class="justify-text"> A. </li>
                <li class="justify-text"> B. </li>
                <li class="justify-text"> C. </li>
                <li class="justify-text"> D. </li>
                <li class="justify-text"> E. </li>
                <li class="justify-text"> F. </li>
            </ul>
        </div>
    </div>
    <p><strong> Read the instructions and watch another demo of the Streamlit app here: <a href="https://github.com/EdRey05/Streamlit_projects/tree/main/002_Automated_PPTX_PLA">Demo_PPTX_PLA</a></strong></p>
</details>

<hr>

<h2> 001 - Extract RNA expression data from CCLE/DepMap </h2>

<details><summary markdown="span"> Expand this to read more...</summary>
    <div class="two-columns">
        <div class="left-column-35">
            <p><strong> Summary </strong></p>
            <p class="justify-text"> Some summary here. 
            </p>
        </div>
        <div class="right-column-65">
            <img src="Images_GIFs_Videos/Preview_001.gif" alt="Streamlit Projects 001 GIF" />
        </div>
    </div>
    <div class="two-columns">
        <div class="left-column-50">
            <p class="justify-text"><strong> Problem </strong></p>
            <ul> 
                <li class="justify-text"> A. </li>
                <li class="justify-text"> B. </li>
                <li class="justify-text"> C. </li>
                <li class="justify-text"> D. </li>
                <li class="justify-text"> E. </li>
                <li class="justify-text"> F. </li>
            </ul>
        </div>
        <div class="right-column-50">
            <p class="justify-text"><strong> Solution </strong></p>
            <ul> 
                <li class="justify-text"> A. </li>
                <li class="justify-text"> B. </li>
                <li class="justify-text"> C. </li>
                <li class="justify-text"> D. </li>
                <li class="justify-text"> E. </li>
                <li class="justify-text"> F. </li>
            </ul>
        </div>
    </div>
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
                free usage per month!</strong>), and follow the instructions in this video-->.<br>
                *Note that due to size limits, I did everything quickly but added notes so pause, read and see where I clicked! <br><br></p>
            <div class="center-text">
                <a href="https://codespaces.new/EdRey05/Streamlit_projects?quickstart=1" target="_blank">
                    <img src="https://github.com/codespaces/badge.svg" alt="Open in GitHub Codespaces">
                </a>
            </div>
        </div>
        <div class="right-column-65">
            <br>
            <video width="100%" height="auto" controls><source src="Images_GIFs_Videos/Demo_Codespaces.mp4" type="video/mp4"></video>
        </div>
    </div>
</details>
