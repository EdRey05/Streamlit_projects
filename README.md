
<h2 class="text-center"> 003 - Interactive Kaplan-Meier plotter </h2>

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
            <video width="750" height="550" autoplay loop muted>
                <source src="Images_GIFs_Videos/Preview_003.mp4" type="video/mp4">
                Your browser does not support the video tag.
            </video> 
        </div>
    </div>
    <p class="text-justify"><strong> Problem </strong></p>
    <p class="text-justify"> We needed to screen a total of 100 genes that we obtained from a different experimental technique as candidates
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
    <p class="text-justify"><strong> Solution </strong></p>
    <p class="text-justify"> I learned how to generate Kaplan-Meier plots using the <code>KaplanMeierFitter</code> module from the <code>lifelines</code>
                            python library. Then I retrieved the relevant datasets from CBioPortal and created a Jupyter Notebook to pre-process and 
                            filter the datasets. Once my notebook could do one KM plot, I hard-coded some iterable variables with all the names of the
                            genes to generate plots for. With this first tool, I produced basic but automated batches of 40-50 plots that allowed us to
                            quickly discard the gene pairs that did not shown the behaviour we were interested in. This first tool (see left GIF below), 
                            required only to change the list of names of genes of interest in a code block, and I did minor adjustments to adapt this to
                            run in Google Colab, allowing lab peers with no coding experience to use it too. 
                            Since I gained great interest for this type of analysis, I kept learning on my own for 1-2 years after the small projects 
                            finished. Then, I found an approach to generalize the data pre-processing and analysis and created a second tool that used                                         <code>ipywidgets</code> to interactively get user input to visualize and select the variables and ways to subdivide the dataset                                    before plotting the KM curves. This second tool (see right GIF below), was significantly more complex but allowed me to easily                                     explore different combinations of variables and subgroups to gain insights about this breast cancer study. Although the 2nd 
                            tool did not require the user to modify any code blocks, the proper rendering of the widget layout I used would not work in 
                            Google Colab and thus the user should know how to install and work in Jupyter lab. For that reason and some difficulties with 
                            widget behavior, I temporarily stopped that project (Version 04). 
                            Around a year later, I discovered Streamlit and tried to transform my notebook to a data app. It took me several weeks to adapt 
                            all my code to <code>streamlit</code> (which has its own widgets), and soon I realized the power of this library. Not only I 
                            was able to translate all the code of my latest version on Jupyter and make it look nicer, but also, I was able to improve the 
                            code, add plot interativity with <code>pyplot</code> and <code>altair</code> plots, add plot customization and add few more 
                            features.
                            Finally, the latest version of the third tool in Streamlit (see GIF above) is fully interactive and works locally or online 
                            through a button that directly builds a <strong>Github Codespace</strong> with everything needed to try it out without having 
                            any coding experience. This tool allowed me to explore different datasets, variables, and generate better plots with accompanying
                            data to do statistical analysis in my software of choice (even re-plot the curve+CIs).
    </p>
    <div class="two-columns">
        <div class="left-column-50">
            <p><strong> First tool for automation (dataset- and gene-specific) </strong></p>
            <img src="https://user-images.githubusercontent.com/62916582/204424020-bae3613c-bf10-4a3b-9d50-beaf50ca8eee.gif" alt="003_first_pre_tool" />
        </div>
        <div class="right-column-50">
            <p><strong> Second tool for automation (interactive subsetting options) </strong></p>
            <img src="Images_GIFs_Videos/Preview_003_Jupyter_version.gif" alt="003_second_pre_tool" />
        </div>
    </div>
    <p><strong> Read the instructions and watch another demo of the Streamlit app here: <a href="https://github.com/EdRey05/Streamlit_projects/tree/main/003_KM_plotter">Demo_KM_plotter</a></strong></p>
</details>

<hr>

<h2 class="text-center"> 002 - Automated Power Point generator</h2>

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
    <p class="text-justify"><strong> Problem </strong></p>
    <p class="text-justify"> Some description here </p>
    <p class="text-justify"><strong> Solution </strong></p>
    <p class="text-justify"> Some description here </p>
    <div class="two-columns">
        <div class="left-column-50">
            <p><strong> Sample cell images and figure </strong></p>
            <img src="Images_GIFs_Videos/Preview_002_figure1.jpg" alt="002_Sample_data_figure" />
        </div>
        <div class="right-column-50">
            <p><strong> First tool for automation </strong></p>
            <img src="https://user-images.githubusercontent.com/62916582/204415085-cc39bb7c-904e-487c-a16d-0d894c1e3249.gif" alt="002_first_pre_tool" />
        </div>
    </div>
    <p><strong> Read the instructions and watch another demo of the Streamlit app here: <a href="https://github.com/EdRey05/Streamlit_projects/tree/main/002_Automated_PPTX_PLA">Demo_PPTX_PLA</a></strong></p>
</details>

<hr>

<h2 class="text-center"> 001 - Extract RNA expression data from CCLE/DepMap </h2>

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
    <p class="text-justify"><strong> Problem </strong></p>
    <p class="text-justify"> Some description here </p>
    <p class="text-justify"><strong> Solution </strong></p>
    <p class="text-justify"> Some description here </p>
    <div class="two-columns">
        <div class="left-column-50">
            <p><strong> DepMap website showing the constant updates to the datasets </strong></p>
            <img src="Images_GIFs_Videos/Preview_001_DepMap_website.jpg" alt="001_DepMap_website" />
        </div>
        <div class="right-column-50">
            <p><strong> First tool for automation (used CCLE data from CBioPortals = DepMap 19Q1) </strong></p>
            <img src="https://user-images.githubusercontent.com/62916582/204422004-47fe5726-d92d-4193-bc6a-ea30b3a93cc1.gif" alt="001_first_pre_tool" />
        </div>
    </div>
    <p><strong> Read the instructions and watch another demo of the Streamlit app here: <a href="https://github.com/EdRey05/Streamlit_projects/tree/main/001_RNA_expression_DepMap">Demo_RNA_DepMap</a></strong></p>
</details>

<hr>

<h2 class="text-center"> Try out my apps with Github Codespaces! </h2>

<details><summary markdown="span"> Expand this to read more...</summary>
    <div class="two-columns">
        <div class="left-column-35">
            <p class="text-justify"> If you have a Github account you can create a Codespace with all the requirements to 
                run my apps. You only have to log into you account, click on the following button, create your Codespace (we 
                all have 60h of free usage per month!), and follow the instructions. </p>
            <a href="https://codespaces.new/EdRey05/Streamlit_projects?quickstart=1" target="_blank">
            <img src="https://github.com/codespaces/badge.svg" alt="Open in GitHub Codespaces">
            </a>
        </div>
        <div class="right-column-65">
            <video width="750" height="550" controls>
                <source src="Images_GIFs_Videos/Demo_Codespaces.mp4" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>
    </div>
</details>
