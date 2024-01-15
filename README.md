
<h2> 003 - Interactive Kaplan-Meier plotter </h2>

<details><summary markdown="span"> Expand this to read more...</summary>
    <div class="two-columns">
        <div class="left-column-35">
            <p><strong> Summary </strong></p>
            <p class="justify-text"> During my graduate studies, I helped two bachelor's students working in my research 
                group to analyze survival data from clinical trials to evaluate a possible association of increased 
                <strong>gene expression</strong> (RET) with bad <strong>clinical prognosis</strong>. For this purpose, we 
                retrieved data available in <strong>CBioPortal</strong>, and generated <strong>Kaplan-Meier survival 
                curves</strong>. We evaluated several datasets and I generated tools (Jupyter/Colab Notebooks and Streamlit 
                app) to automate the creation these plots using the <code>KaplanMeierFitter</code> library in <strong>Python</strong>.
            </p>
        </div>
        <div class="right-column-65">
            <video width="100%" height="auto" autoplay loop muted><source src="Images_GIFs_Videos/Preview_003.mp4" type="video/mp4"></video> 
        </div>
    </div>
    <p class="justify-text"><strong> Problem </strong></p>
    <p class="justify-text"> We needed to screen a total of 100 genes that we obtained from a different experimental technique as candidates
                            to show some interaction with the RET gene. Specifically, we needed to know if patients with low expression of RET 
                            and one of these 100 genes showed decreased survival probability than any other combination (high expression of both 
                            genes, high-low, low-high). We chose the largest dataset for beast cancer (METABRIC), which provides a clinical file
                            containing all patient IDs and survival information (time and status) with around 2,500 patient records and <30 
                            other variables measured. The gene expression information for those patients is provided as a separate file containing
                            around 20,000 genes. We needed to map the IDs between files and filter the dataset into 4 sub-dataset, one for each of 
                            the combinations of expression mentioned (low-low, low-high, high-low, high-high). Finally, we needed to generate 
                            <strong>Kaplan-Meier survival plots</strong> with confidence intervals for each of the RET-gene pairs (100) and keep 
                            the ones that show a significant increase in survival for the low-low curve, compared to the other 3 curves.
    </p>
    <div class="two-columns">
        <div class="left-column-50">
                <p><strong> Problem </strong></p>
                <ul>
                    <li class="justify-text">We needed to generate around <strong>100 Kaplan-Meier plots</strong> (pairs of <strong>RET-gene</strong>
                                            expression). </li>
                    <li class="justify-text">Each plot would require to divide the dataset into <strong>4 groups</strong> to generate <strong>4 survival 
                                            curves</strong> (expression: <strong>low-low, low-high, high-low, high-high</strong>). </li>
                    <li class="justify-text">The clinical data (survival times and status) was in a dataset, whereas the RNA Seq expression data was in
                                            another, so we needed to do some pre-processing to both so we could match the patient IDs. </li>
                    <li class="justify-text">We needed to screen all the plots generated but keep only the ones where the <strong>low-low curve</strong>
                                            was higher than the others, and retrieve relevant data such as CIs and time to 50% survival for analysis. </li>
                    <li class="justify-text">Since each clinical trial reports the data in a different way, we chose the biggest dataset for breast cancer
                                            first (<strong>METABRIC</strong>), but we needed to generalize as much as possible to reuse the tool for other                                                     clinical trials (breast or other cancer types). </li>
                </ul>
        </div>
        <div class="right-column-50">
            <p><strong> Solution </strong></p>
            <ul> 
                <li class="justify-text">I learned how to use the <strong>KaplanMeierFitter</strong> module from the <strong>lifelines</strong> python 
                                        library to generate KM plots. </li>
                <li class="justify-text">I first generated a <strong>Google Colab notebook</strong> that was dataset-specific to produce batches of 
                                        <strong>40-50</strong> plots but only subsetting the dataset in 4 groups based on 2 genes each, and required
                                        manual editing of the code to change the names of the genes of interest (<a href="https://user-images.githubusercontent.com/62916582/204424020-bae3613c-bf10-4a3b-9d50-beaf50ca8eee.gif" target="_blank">View GIF</a>). </li>
                <li class="justify-text">Then, I found a way to generalize some steps and created a <strong>Jupyter notebook</strong> that used
                                        <strong>ipywidgets</strong> to interactively get user inputs, allowing dynamically changing the columns
                                        used to subset the dataset and re-plotting curves (<a href="https://github.com/EdRey05/Resources_for_Mulligan_Lab/blob/de82796fe821b96c18ab0709018c02c3b02aba92/Tutorials/Preview_Interactive_KM.gif" target="_blank">View GIF</a>). </li>
                <li class="justify-text">Finally, I discovered <strong>Streamlit</strong> and adapted my interactive notebook to a data app (GIF above)
                                        that used a similar code approach but with more features to enhance interactivy and improve outputs. </li>
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
            <p class="justify-text"> During my graduate studies, I performed numerous microscopy experiments. These experiments required to acquire sufficient
                                    images (of cancer cells), process them and analyze them. When I was setting up a new technique in our research group
                                    called <strong>Proximity Ligation Assay - PLA</strong> to evaluate protein-protein interactions, I was able to use a 
                                    cell imager (EVOS M7000 - Thermo Fisher) that has automation capabilities. I automated the acquisition of hundreds of 
                                    fields of view (big images with many cells), and wrote scripts in <code>Jython</code> (Python wrapper for Java) to 
                                    automate the image pre-processing and analysis in <strong>ImageJ/Fiji</strong>. The final output of my series of scripts
                                    was a csv file with the quantification result for each image of individual cells (big images where cropped into many 
                                    smaller). Also, to validate the quantification results I designed a tool to merge all outputs into a summary Power Point
                                    presentation. I was able to automate the creation of slides, define the layout and the items to insert into each slide
                                    by using the <code>python-pptx</code> library. I created a tool in Jupyter/Colab notebook version and then a Streamilt 
                                    app that does the exact same thing but provides a better user interface and additional information. 
            </p>
        </div>
        <div class="right-column-65">
            <img src="Images_GIFs_Videos/Preview_002.gif" alt="Streamlit Projects 002 GIF" />
        </div>
    </div>
    <p class="justify-text"><strong> Problem </strong></p>
    <p class="justify-text"> Some description here </p>
    <p class="justify-text"><strong> Solution </strong></p>
    <p class="justify-text"> Some description here </p>
    <div class="two-columns">
        <div class="left-column-50">
            <p><strong> Sample cell images and figure </strong></p>
            <img src="Images_GIFs_Videos/Preview_002_figure1.jpg" alt="002_Sample_data_figure" />
        </div>
        <div class="right-column-50">
            <p><strong> First tool </strong></p>
            <img src="https://user-images.githubusercontent.com/62916582/204415085-cc39bb7c-904e-487c-a16d-0d894c1e3249.gif" alt="002_first_pre_tool" />
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
    <p class="justify-text"><strong> Problem </strong></p>
    <p class="justify-text"> Some description here </p>
    <p class="justify-text"><strong> Solution </strong></p>
    <p class="justify-text"> Some description here </p>
    <div class="two-columns">
        <div class="left-column-50">
            <p><strong> DepMap website showing the constant updates to the datasets </strong></p>
            <img src="Images_GIFs_Videos/Preview_001_DepMap_website.jpg" alt="001_DepMap_website" />
        </div>
        <div class="right-column-50">
            <p><strong> First tool (used CCLE data from CBioPortals = DepMap 19Q1) </strong></p>
            <img src="https://user-images.githubusercontent.com/62916582/204422004-47fe5726-d92d-4193-bc6a-ea30b3a93cc1.gif" alt="001_first_pre_tool" />
        </div>
    </div>
    <p><strong> Read the instructions and watch another demo of the Streamlit app here: <a href="https://github.com/EdRey05/Streamlit_projects/tree/main/001_RNA_expression_DepMap">Demo_RNA_DepMap</a></strong></p>
</details>

<hr>

<h2> Try out my apps with Github Codespaces! </h2>

<details><summary markdown="span"> Expand this to read more...</summary>
    <div class="two-columns">
        <div class="left-column-35">
            <p class="justify-text"> If you have a Github account you can create a Codespace with all the requirements to 
                run my apps. You only have to log into you account, click on the following button, create your Codespace (we 
                all have 60h of free usage per month!), and follow the instructions. </p>
            <a href="https://codespaces.new/EdRey05/Streamlit_projects?quickstart=1" target="_blank">
            <img src="https://github.com/codespaces/badge.svg" alt="Open in GitHub Codespaces">
            </a>
        </div>
        <div class="right-column-65">
            <video width="100%" height="auto" controls><source src="Images_GIFs_Videos/Demo_Codespaces.mp4" type="video/mp4"></video>
        </div>
    </div>
</details>
