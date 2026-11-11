---
reference_id: url:https://commonfund.nih.gov/sites/commonfund/files/Complement-ARIE-Landscape-Analysis-29-Feb-2024-508.pdf
extractor_version: 1
url_source_version: 2
title: "Landscape Analysis Report 2024: New Approach Methodologies in Biomedical Research"
content_type: full_text_pdf
full_text_url: "https://commonfund.nih.gov/sites/commonfund/files/Complement-ARIE-Landscape-Analysis-29-Feb-2024-508.pdf"
---

# Landscape Analysis Report 2024: New Approach Methodologies in Biomedical Research

## Content

 
A-1 
Complement-ARIE 
Landscape Analysis 
 
  
Complement Animal Research In 
Experimentation (Complement-ARIE)  
 
Landscape Analysis Report 2024: New 
Approach Methodologies in Biomedical 
Research 


 
A-2 
Complement-ARIE 
Landscape Analysis 
 
This project was funded in part by the National Institute of Environmental Health Sciences  
(N I E H S ), National Institutes of Health (NIH) under Contract No. HHSN273201500010C to  
I L S /Inotiv and under consulting agreement No. 15-199 to ICF in support of the National 
Toxicology Program Interagency Center for the Evaluation of Alternative Toxicological Methods 
(NICEATM) and The N IH Common Fund Complement Animal Research In Experimentation 
(Complement-ARIE) Program.  
 
 
 
C
ontr
ibuting members from NIH Complement-ARIE:  
Nicole Kleinstreuer, Danilo Tagle, Daniel Shaughnessy, Margaret Ochocinska, Tony Kirilusha, 
Chariz Johnstone, Kris Sunderic, Nikeya Macioce, Christine Happel, Katelynn Milora, and 
members of the NIH inter-IC Complement-ARIE workgroup 
Contr
ibuting members from Integrated Laboratory Systems, an Inotiv company:  
Dave Allen, Emily Reinke, Todd Auman, Anna Kreutz, Jon Hamm, Bridgett Hill, Getachew Tedla 
Contributing members from ICF International:  
Scientific input and analysis: Sadegh Fa ramarzi, Tom Feiler, Kevin Hobbie, Courtney Lemeris, 
Elizabeth Martin, Noelle Sinski, Vidhi Verma, Nicole Vetter, Janielle Vidal, Jessica A Wignall 
Screening, extraction, and reference retrieval: Rachel Col eman, Julia Finver, Samantha 
Goodman, Shahreen Hussain, Michele Justice, Abby Kokkinakis, Jaycee Mayer, Rachel McGill, 
Lisa Prince, Sheerin Shirajan, Swati Sriram 
 
 
 
 
  

A-3 
Complement-ARIE 
Landscape Analysis 
Complement-ARIE Landscape Analysis 
Project Background ................................................................................................................................... A-4  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
Project Methods ......................................................................................................................................... A-6
Initial Search Strategy .......................................................................................................................... A-6
Identification of Seeds ......................................................................................................................... A-7
Broad Scale Search Strategy .............................................................................................................. A-9
Prioritization of Results ...................................................................................................................... A-10
Screening of Studies ............................................................................................................................ A-11
Extraction of Relevant Information and Summary ........................................................................ A-11
FAIR Database Review ........................................................................................................................ A-13
Project Results ......................................................................................................................................... 1A-14
Literature Landscape Results .......................................................................................................... A-14
FAIR Database Results ...................................................................................................................... A-23
Gap Analysis and Overall Recommendations .................................................................................. A-26
Appendix A. Initial Search Strategy ................................................................ . A-341
A
ppendix
 B. Title/Abstract Screening and Extraction .......................................... B -1
Appendix
 C. Broad Search Strategy .................................................................... C-1
Appendix D. Reference List ................................................................... .............. D-
1
Appendix E. Keyword List ................................................................... .............. E-12
Appendix
 F. Prompts Used in Generative AI Approach .......................................  F-
1
Appendix G. Biomedical database with FAIR score per question ........................ G-1
Appendix H. FAIR rubric questions ..................................................................... H-1
Supplemental Materials ....................................................................................... H -26

A-4 
Complement-ARIE 
Landscape Analysis 
Project Background 
The NIH Complement-ARIE (Complement Animal Research In Experimentation) 
program will catalyze the development, standardization, validation, and use of human-
based new approach methodologies (NAMs) that will transform the way we do basic, 
trans
lational, and clinical science.  The goals of the program include developing 
improved alternatives to traditional models for understanding human health and disease 
outcomes across diverse populations; developing NAMs that provide insight into 
specific biological processes or diseases states; validating/qualifying mature NAMs to 
support regulatory use and standardization; and complementing or replacing traditional 
models, making biomedical research more efficient and effective. To ensure that the 
Complement-ARIE program is focused on the areas of science with the greatest need, 
and which present the best opportunities for human-based model development, a 
landscape analysis was required to collect information on ongoing efforts in the NAMs 
space. The following landscape analysis is intended to provide a foundation on which to 
better define the scope of Complement-ARIE and inform upon coordination with existing 
programs. It includes a survey of in vitro, in chemico, and in silico approaches that have 
the potential to improve understanding of human health and disease mechanisms, 
reduce reliance on animal models, and make the use of animals more efficient. To 
ensure a rapid and comprehensive approach, we leveraged generative artificial 
intelligence (GenAI) and other computational methods, supplemented with subject 
matter expertise. In addition, a survey is presented of the requirements for data 
associated with and generated by NAMs to make the data Findable, Accessible, 
Interoperable, and Reusable (FAIR) and AI-ready. This survey includes considerations 
for a suitable data ecosystem and analysis of currently available infrastructure, including 
existing data centers and repositories, that can be leveraged. 
Ac
cor
dingly, this analysis focused on describing existing efforts, and highlighting gaps, 
challenges, and opportunities in the following primary areas of developing human-based 
models of health and disease: 
• In vitro models (e.g., cell lines and organoids)
• In silico models (e.g., multiscale models and digital twins)
• In chemico cell-free models (e.g., biocomputers and high-throughput receptor-
ligand screens)
• FAIRness of data needed to train, interpret, and use NAMs (FAIR = findable,
acc
essible, interoperable, reusable) (e.g., findability/accessibility of datasets,
data annotation and interoperability, artificial intelligence (AI)-readiness of
training data, data ecosystem infrastructure requirements)
In th
ese areas, the following questions are addressed: 

 
A-5 
Complement-ARIE 
Landscape Analysis 
• Current and past systematic efforts (e.g., Multiscale Modeling Consortium and 
Tissue Chip program) to develop and refine NAMs, including both success 
s
tories, scientific and technical challenges, and roadblocks to wider adoption.  
This includes, e.g., current efforts by the Food and Drug Administration 
(Regulatory Science Tools program) and the National Science Foundation 
(Reproducible Cells and Organoids initiative), as well as other federal agencies 
and non-federally supported initiatives (as relevant). 
• O
pportunities to validate mature NAMs to support their regulatory use and 
m
arket adoption. This includes thinking beyond the NAM itself to see how it can 
be meaningfully leveraged in research and/or industrial settings.  
• R
equirements for data associated with and generated by NAMs to make the data 
F
indable, Accessible, Interoperable, and Reusable (FAIR) and AI-ready.  This 
includes considerations for a suitable ecosystem, as well as analysis of currently 
available infrastructure that can be leveraged without building new data centers 
or dedicated data repositories. 
• T
he likely impact of NAMs on complementing and streamlining animal research, 
i
ncluding methods to evaluate potential economic benefits. 

A-6 
Complement-ARIE 
Landscape Analysis 
Project Methods 
The overall project methods are summarized
 in Figure 1 and further described 
in subsequent sections. 
Figure 1. Overall Project Methods 
Initial Search Strategy
Identification
of Seeds
Broad Scale Search Strategy
Prioritization of Results
Screening Studies
Extraction of Relevant 
Information & Summary
Landscape Analysis
31,239 results from search strategy 
16,171 prioritized using topic extraction
1,252 randomly selected from 16,171 
177 Seeds identified as relevant to project
67,718 results from search strategy
10,607 references prioritized for review
6,569 references reviewed to reach 75% 
relevant threshold
2,938 relevant references 
2,848 with PDFs 
2,735 with summary data extracted
In
itial Search Strategy 
We developed an initial search strategy to identify likely-to-be rel evant review  papers. 
We developed t
his strategy by creating a list of keywords for specific topics and then 
co
nvertin
g them to literature database syntax (specifically for the National  Library of 
Medicine’s Pu
bMed database). Our initial sear ch strategy with broad terms returned 
millions of
 hits, and so w e tested the inclusion and exclusion of specific ter ms on the 
number of hits to identify
 the final list of terms. We also limited the scope of the years 
(2018 to Present) and to reviews (as indexe
d by PubMed) only. See Table 1 for a 
snapshot
 of this strategy and Appendix A for full details.  
Table 1. Sn
apshot of Initial Search Str ategy Methods 
Sets of Terms Syntax Other Methods 
Set 1: Alternative methods 
terms 
Set 1 
AND  
(Set 2 OR Set 3 OR 
Set 4) 
Limited to 2018 – 
Present 
Reviews only (PubMed 
filter) 
Set 2: In vitro terms 
Set 3: In silico terms 
Set 4: In chemico terms 
Total: 31,237 hits  
(Ran on Oct 10, 2023) 

A-7 
Complement-ARIE 
Landscape Analysis 
Identification of Seeds 
Topic Extraction 
We applied the approach of “topic extraction” to prioritize the 31k references retrieved 
in the previous step. As shown in Figure 2, this method includes clustering references 
using t
heir
 titles and abstracts so li ke references are grouped with like (and each 
r
eference only appears in a single cluster). The method also  provides the most common 
topic
 keywords for eac h cluster, allowing us to quickl y identify clusters likely to contain 
relevant information. We utilized ICF’s Lits tream® to perform this analysi s. 
Figure 
2. Illustration of Topic Extraction Methodology 
Cluster References 
Based on Text 
Similarities
Further review clusters 
with most relevant 
keywords.
Method for scoping in 
the absence of any 
training data.
Results
Provides cluster size 
and 20 most common 
keywords in each cluster 
We derived 10 clusters, shown in Table 2, with associated keywords. Using the results 
of topic ex
traction, we included 16,171 references from clusters 4, 8, 9, and 10 from 
Table 2
 in subsequent screening and review steps.  
Table 2.
 Topic Extraction R esults 
Cluster # of 
Studies 
Keywords/Topic Signature 
1 6542 biomarkers, patients, clinical, disease, treatment, risk, 
diagnosis, studies, diagnostic, management, early, patient, 
based, therapy, current, outcomes, biomarker, results, new, 
methods 
2 846 95, ci, meta, meta analysis, 95 ci, analysis, review meta, 
review meta analysis, systematic, systematic review meta, 
pooled, systematic review, studies, included, patients, 
results, hr, ratio, embase, value 

A-8 
Complement-ARIE 
Landscape Analysis 
Cluster # of 
Studies 
Keywords/Topic Signature 
3 1901 cancer, patients, tumor, immunotherapy, checkpoint, 
immune, inhibitors, treatment, biomarkers, immune 
checkpoint, clinical, pd, response, therapy, predictive, 
checkpoint inhibitors, lung cancer, pd l1, l1, lung 
4 2077 learning, machine, machine learning, ai, intelligence, 
artificial, artificial intelligence, data, ml, deep, deep learning, 
models, prediction, methods, algorithms, based, predictive, 
applications, intelligence ai, artificial intelligence ai 
5 713 covid, covid 19, 19, cov, sars, sars cov, coronavirus, 
pandemic, respiratory, acute respiratory, severe, respiratory 
syndrome, 2019, severe acute respiratory, severe acute, 
infection, acute respiratory syndrome, 19 pandemic, covid 
19 pandemic, syndrome 
6 2501 gene, arna, expression, gene expression, r n a s , coding, 
sequencing, genes, non coding, regulation, genome, cell, 
epigenetic, single, dna, non, mechanisms, throughput, 
genetic, coding r n a s  
7 2563 cancer, tumor, cells, cell, therapeutic, treatment, therapy, 
resistance, microenvironment, drug, tumors, progression, 
metastasis, cancer cells, cancers, models, clinical, targeting, 
development, potential 
8 2480 stem, cells, stem cells, cell, stem cell, pluripotent, tissue, 
pluripotent stem, regenerative, derived, regeneration, 
human, mesenchymal, mscs, therapy, pluripotent stem cells, 
mesenchymal stem, induced pluripotent, induced pluripotent 
stem, disease 
9 7202 based, methods, high, applications, approaches, systems, 
development, throughput, new, data, research, high 
throughput, recent, technologies, used, drug, techniques, 
analysis, advances, tools 
10 4412 vitro, models, drug, studies, vivo, effects, disease, diseases, 
therapeutic, development, mechanisms, drugs, human, 
potential, treatment, inflammatory, anti, activity, compounds, 
clinical 
Title/Abstract Screening and Extraction 
We created random subsets of the 16,171 references for expert staff to review 
according to the methods outlined in Appendix B. Specifically, staff reviewed 1252 
references (~
8% of titles/abstracts randomly selected from the 16,171) for relevance to 
the project. Each reference was reviewed by a primary reviewer and a QA reviewer 
confirmed the accuracy of the primary review. References could be categorized as 

A-9 
Complement-ARIE 
Landscape Analysis 
Include, Supplemental, or Exclude as shown in Table 3 below, and high-level 
study details were extracted as shown in Appendix B. 
Table 3. Categories for Classification of References According to Title and 
Abstract 
Relevance Categories Definition 
Include In vitro 
In silico 
In chemico 
General Methods 
Method has the potential to complement or 
replace the use of animals in biomedical 
research 
Supplemental FAIR Relevant to findable, accessible, interoperable, 
and reusable concepts, including discussion of 
data availability or databases or other 
repositories 
Animal-based 
NAM 
NAM but animal-based (using animal tissue – 
whole organisms are excluded) 
Potential 
application in 
biomedical 
research 
Catch-all bin for when the paper has the potential 
for being relevant to a biomedical context and 
replacing animal tests, but the authors do not 
necessarily make that point explicitly 
Exclude n/a The study does not describe an alternative test 
method/model that meets the requirements 
above, where the context is related to 
recapitulating a relevant human physiological 
process or increasing our understanding of a 
biological process 
Broad Scale Search Strategy 
We then developed a broader search strategy to complement the initial strategy. 
Specifically, we expanded to additional databases (Web of Science and Scopus) and 
did n
ot limit to reviews only, but we looked at only the most recently published papers 
(2023 – 2024 references published early). This resulted in 67,718 potentially rel evant 
references after deduplicating across databases. Expanding to 2018 – Present would 
have resulted in about 450k references, which was deemed beyond the project's scope 
given the focus on obtaining the most current perspective of NAMs in the scient
ific 
literature. Take
n together, we assumed that  the reviews identifie d during the initial 
search strategy and the most  recent papers fr om this broad search strategy represent 
the landscape of
 the most cutting-edge developments able to be ev aluated within the 
project’s time constraints. See Table 
4 for a snapshot
 of this strategy and  Appendix C 
for full details.  

A-10 
Complement-ARIE 
Landscape Analysis 
Table 4. Snapshot of Broad Search Strategy Methods 
Sets of Terms Syntax Other Methods 
Set 1: Alternative methods 
terms 
Set 1 
AND  
(Set 2 OR Set 3 OR 
Set 4) 
Limited to 2023 – 
Present 
Set 2: In vitro terms 
Set 3: In silico terms 
Set 4: In chemico terms 
PubMed: 53,846 hits 
Scopus: 25,470 hits 
Web of Science:33,434 hits 
Total: 67,718 hits  
(Removing duplicates across PubMed, Web of Science, and Scopus; ran on Oct 
23, 2023) 
Prioritization of Results 
To increase the likelihood of i
dentifying key papers in the field, a modular prioritization 
method was applied. Specifically, supervised ensemble clustering was performed using 
seed
 studies identified as relevant in Step 2.2. An ensemble of six clustering 
approaches using two clustering algorithms (
K-means and non-negative matrix 
factorization) and three bin sizes (10, 20, and 30) were applied and each study was 
assigned a score based the number of times the study was found in a selected cluster 
containing a high proportion of seeds. Studies with an  ensemble cluster score  of greater 
than or equal to 4 (n=10,607, see Table 5) were prioritized for human screening based 
on a prior study that
 demonstrated the validity of the scoring method (Cawley et al., 2020) 
Table 5. Ensemble Clustering Results 
Seed 
# of Refs 
6 5 4 3 2 1 0 
Grand 
Total 
Unclassified 3720 2645 3637 5887 8824 10412 32593 67718 
Seeds tagged as 
“exclude” 223 146 84 58 37 45 66 659 
Seeds tagged as 
“include” 93 38 21 11 2 5 7 177 
Grand 
Total 4036 2829 3742 5956 8863 10462 32666 68554 

A-11 
Complement-ARIE 
Landscape Analysis 
Screening of Studies 
To expedite the process of title/abstract screening, the Active Machine Learning (AML) 
component of Litstream was employed to accelerate review of the 10,607 studies 
identified as being of potential interest. AML requires a user to annotate an initial set of 
references as relevant or not relevant to first train the model. Litstream provides 
additional references for the user to annotate, then iterates the model to optimize on 
recall. Using additional screening data from every 50 studies screened, a support vector 
machine algorithm builds a predictive model to re-rank not-yet-screened s tudies in 
terms of their likely relevance, based on natural language patterns to identify the most 
likely to be relevant studies
 (see Figure 3).  
Figure 3. Illustr
ation of Active Machine Learning Methodology 
This
 ranking process sifts the unreviewed references and prioritizes those predicted to 
be relevant for human review. This allowed for the screening of 6,569 titles and 
abstracts and the identification of 2,938 relevant studies, which was estimated to be 
more than 75% of the total relevant studies. In discussion with the Complement-ARIE 
leadership, this threshold was decided to be enough relevant studies to proceed to 
analysis in order to meet the expedited timeline. 
Extraction of Relevant Information and Summary 
PDF Retrieval and Generation of Text Files 
For references deemed relevant in previous steps, we retrieved PDFs from NIH Library 
and ot
her web sources. Of the 3,091 studies to enter the pipeline (2,938 identified 
during AML + 261 seed studies, with 108 duplicates removed), we successfully 

A-12 
Complement-ARIE 
Landscape Analysis 
retrieved 2,848 (243 were not available without inter-library loans or purchasing or were 
not in
 English). See Appendix D for a reference list. 
Availabl
e PDFs were converted to text files using Azure AI Document Intelligence for 
use in future steps of the project (see below). 
Keyword Analysis 
We developed a list of keywords
 to categorize relevant references. The Keyword 
Analysis Tool (KAT) searched for the occurrence of o ne or more keywords within either 
a title 
or abstract of a 
bibliographic reference. The tool generated a CSV file with a 
frequency array by keyword for each reference, which we used to understand the scope 
of the relevant literature. We developed the keyword list
 used in this step (Appendix E) 
in collaboration with Complement-ARIE leadership. 
Generative Artificia
l Intelligence (AI) 
For extraction of
 relevant information, generative AI technology was leveraged. 
Anthropic’s Claude V2 Foundation Model LLM was chos en for this analysis as it  was a 
secure technology designed for summarization with a high enough token limit to read a 
full PDF and return a satisfactory answer
. T
o deploy this across all possible studies, we 
developed a Claude workspace in the AWS Bedrock envir
onment. This allowed for 
compiling of responses across multiple papers and uploads of multiple PDFs in a 
systematic and streamlined way.  
Two methods were proposed and piloted.
 The f
irst was to feed a corpus of studies to an 
AI and then ask specific questions related to the overall state of the field/topic area. The 
second was to summarize studies individually and then aggregate the data across the 
bolus of literature based on individual level
 summaries. After piloting, it was determined 
that the first approach was
 not feasible as the generative AI tended to “hallucinate” 
information beyond that which was provided,
 and it would be difficult to do this approach 
in a systematic way. We therefore decided the best approach would be to summarize 
studies on a study-by-study basis and then aggregate the data afterwards .  
For the generative AI, we 
developed questions in conjunction with Complement-A RIE 
leadership with the aim of (1) understanding the currently
 existing landscape of 
literature, (2) making funding decisions to move the state 
of the science forward and (3) 
thinking ahead to understand the current ethical, w orkforce,
 economic and social issues 
that may surround the use of N
AMs. These questions were then converted into pr ompts 
that prevented the AI interface from making up answers (
aka “hallucinating”), and quotes 
had to be given to justify the response
 generated by the AI for validation purposes. The 
full list of questions and 
prompts can be found in Appendix F.  

A-13 
Complement-ARIE 
Landscape Analysis 
Of the 2,848 studies, 47 were non-responsive in Claude and 66 PDFs were longer than 
40 p
ages (exceeding the token lim it). This resulted in a total of 2, 735 successful outputs 
that were summarized by generative AI.  
Post-P
rocessing of Generative AI Outputs 
After collecting the responses from the Claude outputs, we applied post-processing of 
the text to convert statements noting a lack of data to a standardized response (e.g., 
changing “I don’t see…” or “The authors did not…” to “No”). Additionally, for a subset of 
questions, we re-entered the responses into Claude and asked it to extract the “named 
entities” of each statement so that the information could be returned in the format of a 
categorical list, to use f or further classification of the studies and response data. These 
prompts can also be found in Appendix F. 
FAIR
 Database Review 
Twenty-eight out of 260 identified biomedical databases were evaluated for Findability, 
Accessibility, Interoperability and Reuse (FAIR) using a modified rubric originally 
developed by the U.S. Geological Survey (Hutchison et al., 2023; Wilkinson et al., 
2016). This rubric consisted of 29 questions (Appendix H) aimed to assess 
computational readiness and was applied to each databas e by two evaluators: one 
initial screen/scoring and one review of assessment. If the evaluator was able to find the 
information for a given question, the question received a score of “1” and if the 
information was not identifiable, the question received a score of “0”. These scores were 
summed and each evaluated database and FAIR question was given a composite 
score. Databases were also categorized using keyword lists (Appendix E) to determine 
NAM representation.  

 
A-14 
Complement-ARIE 
Landscape Analysis 
Project Results 
 
 
 
Literature Landscape Results  
Overall breakdown of representation    
Following assessment of the comprehensive literature review by generative AI, we 
summarized and mapped the relevant references into interactive visuals according to 
the results of AI, answers to relevant questions and categorical assignments, and 
reference characteristics using Tableau data visualization software (Seattle, WA) (see 
Complement-ARIE Landscape Analysis). Individual dashboards focus on different 
aspects of the data, with questions and categories featuring prominently. Interactive 
features include: 
• Filtering by variables of interest 
• Hoveri
ng over data elements for additional information and links to references 
• Search for specific keywords of interest 
The Tableau comprises three tabs:   
• Explore Questions: Generative AI responses to questions for each reference, 
organized by question.  
 
• Explore Categories: All references organized by keyword.  
 
• Reference List: All references including bibliographic details.  
As shown in Figure 4, data within Tableau can be sorted and filtered to identify, for 
example, the volume of studies associated with a specific type of NAM, identify papers 
that include multiple types of NAMs for potentially evaluating combinatorial approaches, 
or
 note trends associated with generative AI responses (see also Fig 5 and 
supplementary material). 
 
 

 
A-15 
Complement-ARIE 
Landscape Analysis 
 
 
 
 
 
 
 
Figure 4a. T
ableau screenshot demonstrating how to explore categories by organizing 
references organized by keyword.  
Fi
gure 4b. Tableau screenshot demonstrating how to explore generative AI responses 
to questions for each reference.  
The res
ults demonstrate that NAMs work has mainly focused on in vitro (n=1284) and in 
si
lico (n=1300) studies with fewer in chemico (n=657) studies or general methods 
development such as high throughput screening (n=750). Within the in vitro category, 
stem cell (n=556) and 3D cell culture (n=487) are the best represented categories. In 
chemico analyses have focused on biochemical assays (n=273) or structure/identity 
analysis methods (n=262). In silico studies are generally focused on the development of 
AI/machine learning models (n=676) and molecular simulation (n=483). Review of the 
topical breakdowns following generative AI did note that the assignment of categories 
was not always completely accurate. It is likely that some manuscripts were overlooked 
within certain subject areas (or incorrectly included based on keyword analysis). 

 
A-16 
Complement-ARIE 
Landscape Analysis 
However, the overall outlook of the current state of NAMs in biomedical research is still 
appr
opriately reflected in this assessment based on the wide range of input received 
relating to the literature review approach implemented, and the alignment of observed 
trends with comprehensive NAMs review papers.  
 
Whi
le there were differences in the amount of NAM publications gathered for each focal 
area, similar trends were noted in all (Figure 5, Supplemental Materials). The topics with 
the highest representation examined both cell and tissue types, human physiology 
considerations and method information including detailed description of new or 
improved technologies, and technological challenges. Diseases, metabolic capabilities, 
and method limitations were also addressed, but to a lesser extent. Areas that were 
seldom reported or addressed in these publications included regulatory application, 
workforce or ethical considerations, population diversity and variability, and economic 
considerations. However, it should be noted that publications often included related 
aspects such as future endeavors and ethical considerations regarding multiple cell 
culture techniques including biobanking, community engagement and informed patient 
consent. An assessment of these gaps is found in the Gap Analysis section. A common 
future direction noted in publications included the need for standardization and 
validation of NAMs.    

 
A-17 
Complement-ARIE 
Landscape Analysis 
Figure 5. Number of Publications Gathered per General Topic Using Generative AI 
Approach. 
 
In vitro biomedical NAMs 
Acr
oss the literature on in vitro models, 2D and 3D cell cultures were highly 
represented, including models based on both induced pluripotent and embryonic stem 
cells (Supplemental Materials). Many of these publications are focused on the use of 
cardiomyocyte, neuronal and endothelial cell types and liver, bone, breast, lung, and 
skin tissues. Cancer (e.g., liver, ovarian, breast and pancreatic), diabetes, Alzheimer’s 
and Parkinson’s diseases were a particular focus. In vitro methodologies were the 
largest proportion of literature hits compared to in silico and in chemico approaches. 


 
A-18 
Complement-ARIE 
Landscape Analysis 
Within the in vitro space, bioprinting and microphysiological based systems were often 
used in conjunction with 2D and 3D cell cultures to better recapitulate organ and tissue 
human physiology for disease research, supporting the high representation of 2D and 
3D methods. Examples include patient derived cells to create organoids for ovarian 
cancer and development of prostate organoids for preclinical cancer research (Buskin et 
al., 2023; Chan et al., 2023). Technological advances continue to foster the 
development and use of these more complex models, but challenges still remain to 
represent complex tumor microenvironments and metastasis processes. Other non-
cancer related NAMs include stem cell cardiomyocyte “heart-on- a-chip” and hepatocyte 
microfluidic “lab-on-a-chip” platforms in addition to ocular organoids for drug 
development and diseases (Bai and Wang, 2020; Criscione et al., 2023; Di, 2023).  
Keywor
d analysis revealed gaps in knowledge including lack of donor derived high 
throughput culture panels, co-culture and explant in vitro NAMs. Developmental 
neur
ological disorders including ADHD and autism spectrum disorders, asthma, and 
immune and inflammatory diseases were also seldomly represented. Multiple aspects of 
methods were reported including method limitations and challenges such as high cost 
with limited resolution of bioprinting along with the potential toxic waste materials 
generated through these processes and inclusion of multiple different cell types to help 
identify roles of genetic variants. While many of these approaches were not specifically 
noted for regulatory purposes, there were a few review papers highlighting the potential 
for alternative approaches (e.g., specialized cell lines and organ-on-chips) in the food 
safety and endocrine disruption space (Audouze et al., 2020; Reddy et al., 2023). 
Various ethical considerations were highlighted in two main areas: those related to the 
origin of human embryonic stem cells and the study of psychiatric disorders, which 
commonly combine both in vitro and in vivo techniques such as complex human brain 
organoid and mammalian behavioral observations, both of which may have some level 
of consciousness (Cota-Coronado et al., 2019; Dixon and Muotri, 2023). Workforce 
considerations are a noted gap for all biomedical NAMs, which takes into consideration 
aspects of an approach, such as training that would be needed in order to implement it. 
There was one instance of rapid bioprinting for medical supplies development (e.g., 
human tissues and bioactive bandages) for military use in austere locations and the 
need for training in both use and advancement of these technologies (Barnhill et al., 
2023).  Ongoing research of these bioprinting technologies can lead to the development 
of civilian/consumer level accessibility in medicine, providing a potentially biocompatible 
option for burns and traumatic injury, treatment of dermal diseases, etc. Lastly, areas 
that were not considered but mentioned as future directions include translation for 
clinical relevance, and lack of incorporation of immune and microvascular components, 
and drug development for rare diseases including precision medicine.  
 

 
A-19 
Complement-ARIE 
Landscape Analysis 
In silico biomedical NAMs 
The main focal areas of in silico approaches were AI and machine learning; molecular 
simulation; and predictive models for absorption, distribution, metabolism, and excretion 
(see Supplemental Materials). Within these the largest percentage of NAMs focused on 
AI and machine learning. Areas with the least representation within the biomedical 
space include digital twins and read across approaches which may have been 
influenced by the focus of this review since the latter approach is more commonly 
utilized in toxicology fields, and the former is an emerging topic in precision medicine.  
Due to the vast amount of literature within the AI/ML category, it was necessary to 
explore the “detailed answers,” i.e., 5,351 records for this category, produced by the 
generative AI. To do so, we have generated bar plots to indicate the frequency of 
phrases within the “detailed answer” records, with the assumption that word frequency 
distributions would indicate areas that are less or more explored.  
As disease-treatme nt and drug-development are two broad areas within biomedical 
research, the phrase frequency distributions focus on these two topics. Cancer is the 
most highly explored disease type, with mental health, cardiovascular diseases and 
diabetes following closely. Figure 6 indicates the distribution of the different types of 
cancer and cancer therapies that were most highly represented within the literature. 
Removing the term "cancer” to look more specifically at cancer type shows that lung, 
breast, colorectal, prostate, glioma and glioblastoma are the most represented, in line 
with cancer rates and research funding (Figure 7).  Regarding drug development, 
docking, molecular dynamic simulations, and virtual screening are among the frequently 
used methods (Figure 8). This analysis indicates that there is a lack of effort in utilizing 
or developing read across, pharmacophore, and homology methods for drug 
development.  
 
 
 
 
 
 
 
 
 
 

 
A-20 
Complement-ARIE 
Landscape Analysis 
Figure 6. Frequency Distributions of Cancer and Therapy Types 
 
 
 
Figure 7. Frequency Distribution of Cancer Types 


 
A-21 
Complement-ARIE 
Landscape Analysis 
 
Figure 8. Frequency Distribution of Drug Development Computational Methods 
In g
eneral, large language models (LLM) is one of the least studied AI/ML categories 
where only one relevant paper was identified (Zagirova et al., 2023). The model was 
developed on a large corpus of biomedical literature and generates targets predictions. 
The authors have shown its application on aging and age-related disease targets.  
However, as the practical availability of LLMs has exploded in  the past year, it is 
expected that their use in biomedical research will grow significantly in the near future. 
In chem
ico biomedical NAMs 
 The two larges
t aspects of in chemico NAMs were biochemical assays and 
struc
ture/identity analysis (Supplemental Materials). Many of the “in chemico” articles 
should have been categorized as “in silico” upon further assessment. Cell free and 
ligand-receptor binding assays were included as part of the keyword categorization but 
were rarely noted in these publications. Of the correctly categorized publications, these 
mainly included enzymatic assays and mass spectrometry and chromatography with a 
focus on brain and liver tissues. Similar to in vitro NAMs, cancer (parti cularly breast 
cancer), along with diabetes and Alzheimer’s disease, were some of the most common 
disease research topics. One of the most promising areas for application of in chemico 
biomedical NAMs will be in the identification of novel biomarkers. For instance, 
proteomics has helped to identify prognostic, predictive, and therapeutic biomarkers for 
various sarcoma subtypes (Connolly et al., 2023). Many screening approaches have 

 
A-22 
Complement-ARIE 
Landscape Analysis 
also been facilitated by in chemico NAMs, including a v ariety of reporter assays to 
assess endocrine disruption. For instance, the AR2 assay uses a luciferase enzyme 
fused to the human androgen receptor to assess androgen receptor homodimerization 
and allows for incorporation of enzymatic metabolism (Brown et al., 2023). The assay 
showed a high Z’-factor and balanced accuracy, and an interlaboratory investigation is 
now being conducted. Supramolecular chemistry (the chemistry of noncovalent bonding 
between molecules) is another exciting field opening up for screening. A supramolecular 
tandem assay in conjunction with a reporter assay for intracellular imaging of HDAC1 to 
identify HDAC1 inhibitors was recently developed (Li et al., 2023). This approach is 10X 
more sensitive than prior HDAC1 assays and has already identified one novel HDAC1 
down-regulator. The primary challenge noted for in chemico biomedical NAMs is 
translation to in vivo models and then later into human clinical medicine. Additional 
challenges include single cell mass spectrometry, enabling real time analysis, and full 
automation. For example, the identification of metabolite biomarkers still faces a variety 
of challenges. These include the high variability of such data, which can be influenced 
by diet, exercise, environment and experimental handling; generally low sensitivity and 
specificity; and a lack of standardized protocols for statistical analysis. In sum, in 
chemico biomedical NAMs are poised to play an important role in biomarker 
identification and screening (Anwardeen et al., 2023). 
 
 
  
Com
binatorial NAM strategies 
While this landscape analysis has provided information on the individual NAM groups 
highlighted above, it has also shed light on combinatorial approaches across the 
targeted NAM spaces. Main topics include cancer, drug discovery and digital pathology 
with most of the approaches focusing on molecular docking and spectral imaging. 
However, only roughly 1% of the gathered publications spanned all four targeted NAM 
categories (i.e., in vitro, in silico, in chemico and general methods) with the majority of 
these not integrating these approaches but instead reviewing their respective potential 
utility (see Figure 9).  

 
A-23 
Complement-ARIE 
Landscape Analysis 
Figure 9. Overlap of NAMs Categories in Literature Reviewed  
 
 
 
 
 
Li
ter
ature landscape challenges and limitations 
Approaches were utilized to help identify key areas and gaps in knowledge by applying 
specific keywords or questions to the gathered publications. Review of publications 
revealed that there were some challenges with the algorithm in which topics or 
keywords were mentioned in publications (e.g. in the background or introduction 
sections) but weren’t relevant to the particular study. While this is a noted challenge, 
this aided in identifying future applications for these NAMs in biomedical research as 
many of
 these instances were included as future directions or current limitations. 
FAIR
 Database Results  
FAIR assessment of the 28 databases reviewed differed with only 9 databases including 
at least 70% or more of the information needed to answer rubric questions. Only one 
database, the Human BioMolecular Atlas Program (HuBMAP), included all information 
targeted 
by our review. Other databases that included 93% and 86% of FAIR 
information were the Library of Integrated Network-Based Cellular Signatures (LINCS) 
and NIH Genetic Testing Registry (GTR) and Genome-wide Association Studies  
(G WAS) Catalog, respectively. The categories of reviewed databases also varied with 
most falling within General Methods (e.g., high throughput screening, sequencing 
technology, and omics approaches), suggesting that databases are centered more on 
the technological aspects of the assays as opposed to NAM space (e.g., cell culture 
type, microphysiological systems, AI, and machine learning).  

 
A-24 
Complement-ARIE 
Landscape Analysis 
Focusing on the four main principles of FAIR, there was not a single rubric question for 
which all databases provided information. The highest response ranges were for 
Accessible (12 – 27 databases, median of 19) and Findable (4 – 25 databases, median 
of 23) indicating the ability to identify and retrieve unique labeled data/metadata, 
through human and automated actions, is not a limiting factor among the evaluated 
biomedical databases. Areas that had the lowest reporting tended to fall within the 
Interoperable (7 – 27 databases, median of 15) and Reusable (8 – 22 databases, 
median of 13) domains which address integrating, replicating or combing data for 
processing, analyzing and storage applications. Information pertaining to seven out of 
the 29 questions were not able to be identified for more than half of the databases 
(Figure 10). The question with the lowest response addressed detailed author 
information (ORCID identifier),  which was likely too specific for this exercise. There was 
also an additional question pertaining to citations for input datasets that was likely not 
relevant for those that did not include these and therefore this information could not be 
identified. Other questions that were less FAIR included metadata documentation such 
as information on data consistency/precision/accuracy and including suggestions for 
data reuse both in terms of data constraints and user groups that could reuse data. 
 
 
 
 
 
  
Fur
ther review of documentation provided by databases revealed that while most 
encourage detailed reporting of metadata, sole reliance on the data originator or 
submitter for the level of detail resulted in a lower FAIR score. Additional aspects that 
led to less FAIR databases include limited access to data/metadata (e.g. required 
account credentials) or obtained data, without metadata, from existing databases and 
utilized internal data processing pipelines. For this reason, some of the above-
mentioned areas that scored the lowest were related to method details including 
information about technological aspects of assay or data quality practices. Conversely, 
databases that incorporated curation/harmonization steps, detailed reporting criteria or 
forms tended to be more FAIR, indicating that establishment of metadata reporting 
guidelines or standardization will enable more FAIR resources. 

 
A-25 
Complement-ARIE 
Landscape Analysis 
Figure 10. FAIR Principle Ranking per Database1.
1 N H C  D R : N I N D S  Hum an  Cell and Data Repository; BioSystics-AP: BioSystics Analytics Platform; CCDI MTP: Molecular Targets 
Platform; CMAP: Connectivity Map;  IDC: Imaging Data Commons; TCGA: The Cancer Genome Atlas; N DEx: The Network 
Data Exc
hange; HuBMAP: The Human BioMolecular Atlas Program; IDC: Imaging Data Commons; BioGRID: Biological 
Genera
l Rep
ository for Interaction Datasets; C D S : Cancer Data Service; DABI: Data Archive for the BRAIN Initiative; GDC: 
Genomic Data Commons; G  E  A  :  Genomic Expression Archive; G TEx: Genotype-Tissue  Expression; G  WAS: Genome-wide 
Association Studies Catalog; G  WAS Central; LINCS: Library of Integrated Network-Based Cellular Signatures; NCBI dbVar: 
Structural Variation Database; N  H  G  R  I  -EBI G  WAS Catalog; The N  H  G  R  I   Genomic AnVIL: Data Science Analysis, Visualization, 
and Informatics Lab-space; PDC: Proteomic Data Commons; PRIDE: Proteomics Identifications Database; NIH GTR: 
Genetic Testing Registry 
 Warmer colors indicate a higher 
FAI
R score while cooler colors indicate a lower FAIR score. Databases with the 
overall highest FAIR score are highlighted. Detailed view of each FAIR principle 
can be viewed in Appendix G and FAIR questions are listed in Appendix H. 
 
 


 
A-26 
Complement-ARIE 
Landscape Analysis 
Gap Analysis and Overall Recommendations 
 
 
 
 
While this landscape analysis provides a general overview of the current status of 
biomedical NAMs, there are several areas to refine and explore in this space. Indeed, 
t
his report focuses on a snapshot in time of biomedical NAMs and recent NAM 
applications; evaluating these spaces over a broader range of time will enable our 
understanding of how certain NAM use has changed over time or how certain areas 
have evolved over the period being analyzed. The citations provided are by no means 
an exhaustive list of relevant studies, and the papers discussed below are simply 
examples of the observed trends. Additional post processing of generative AI including 
quality control of AI outputs, in depth review of AI summaries of assay group limitations 
and biological coverage of each technology type, and review of documents that failed 
generative AI are future directions to explore. Various other literature approaches can 
be applied to further assess the biomedical NAM space. Some of these include review 
of titles/abstracts that were not screened using keyword/computational approaches, 
evaluation of number of citations for references/methods to understand replicability, and 
review of other sources of information outside of peer-review.  
Wit
h those caveats, the results suggest that cardiomyocytes, neuronal and endothelial 
cell types and liver, bone, breast, lung, and skin tissues are extensively represented 
among the in vitro NAMs identified, a nd thus perhaps other cell types/tissues should be 
prioritized for further development. Likewise, cancer, diabetes, Alzheimer’s and 
Parkinson’s diseases have all been a particular focus of recent efforts, although very 
few (or no) articles included the application of NAMs in translation for clinical relevance, 
and there was a general lack of incorporation of immune and microvascular 
components. Such issues could be the subject of targeted future efforts. 
Regar
ding in chemico methods, there is modest representation across all four of the 
principal categories defined for this analysis, with biochemical and structure/identity 
analysis methods most highly represented among those studies. We did find that many 
in chemico studies were misclassified, suggesting further refinement of the search and 
interpretation algorithms is necessary. However, overall, such methods have the 
capacity to efficiently screen compounds of interest with exquisite sensitivity and thus 
could be considered in future efforts to design combinatorial approaches in 
conjunction with other types of NAMs to address a wide range of research questions. 
Given the rapid growth of computational approaches, it is not surprising that AI and 
machine learning represent the majority of silico NAMs that were identified. There is 
l
ittle debate of the power of such approaches in biomedical research, limited only by the 
quality and quantity of input data with which they are initially developed and trained. 
Future efforts should harness the data generated by NAMs and therefore an essential 

 
A-27 
Complement-ARIE 
Landscape Analysis 
future effort is the development of a readily accessible data repository. Considering the 
observation that databases incorporating curation/harmonization steps, detailed 
reporting criteria or forms tended to be more FAIR, establishment of metadata 
reporting guidelines or standardization to enable more FAIR resources should be a 
priority. 
 
 
 
Regardless of the category of method considered (i.e., in vitro, in chemico, in silico, or 
general method), economic and workforce considerations, ethical considerations, 
regulatory use, and population diversity and variability were consistently 
underrepresented, highlighting key areas where additional research efforts should be 
directed (Figure 11 and S2, S4, S6, S8). Given their potential throughput, human 
relevance, and opportunity for representative heterogeneity, it would seem prudent to 
more extensively evaluate the utility of NAMs for addressing these research questions.  
Figure 11. Identification of Topical Areas Least Identified by Generative A.I. 
This
 analysis also indicates that future efforts need to be focused on using 
combinatorial or multidisciplinary NAMs to investigate and address human health 
sc
ience.  Only 1% of the reviewed literature described research encompassing in vitro, 
in silico, in chemico and high dimensionality research methods.  Research programs 

 
A-28 
Complement-ARIE 
Landscape Analysis 
centered on specific aspects of human health or disease states could be used to 
develop concerted, multidisciplinary efforts that complement each other to provide 
insight and advances that would be impossible to achieve using single NAM modalities. 
Review of Population Diversity and Variability Incorporated Findings 
Forty-eight manuscripts were identified as having potential information on population 
diversity and variability incorporated. Not surprisingly, the greatest number of hits (14) 
were found in stem cell studies, followed by 12 on AI/machine learning within in 
chemico approaches, and 10 each for high-throughput screening and sequencing 
technology within general methods. Screening the identified manuscripts, it appears 
most make only a cursory mention of donor-related diversity. For example, X. Gao et al.  
published a manuscript entitled Toxicological applications of human induced pluripotent 
stem cell-derived hepatocyte-like cells: an updated review (Gao et al., 2023). The 
manuscript presents data on hepatocyte-like cells (HLCs) derived from human induced 
pl
uripotent stem cells (i P S C s ) as in vitro hepatotoxicity models and makes mention of 
t
he fact that H
LCs maintain their original donor genotype and allow for donor diversity to 
be studied.  
Wit
hin the references on AI, Y. Gao et al.  published a manuscript entitled Addressing 
the Challenge of Biomedical Data Inequality: An AI Perspective” (Y. Gao et al., 2023) 
which focus on issues of population diversity. Central to their manuscript, Gao et al. 
state “existing biomedical data, which are a vital resource and foundation for developing 
medical AI models, do not reflect the diversity of the human population. The low 
representation in biomedical data has become a significant health risk for non-European 
populations…”. 
A small number of additional manuscripts, including Pike et al. (2023) and Hnatiuk et al. 
(2021), discuss donor diversity and its influence on test results in more detail (Hnatiuk et 
al., 2021; Pike et al., 2023). Pike et al. published a manuscript entitled Characterization 
and optimization of variability in a human colonic epithelium culture model. This 
manuscript analyzes donor-specific differences and presents the influence of these on 
test results. Hnatiuk et al. (2021) published a manuscript entitled Human i P S C  modeling 
of heart disease for drug development.  Hnatiuk et al. state “h i P S C s r etain the genetic 
makeup of their human donor, so they have the potential to recapitulate essential 
aspects of genetic diseases or mimic drug responses in vitro”. Based on this, Hnatiuk et 
al. suggest several points, including the fact that large numbers of patient-derived  
h i P S C  lines might be needed to infer the effect of a rare variant on a clinical phenotype 
or drug response, that studies using h i P S C  lines may experience confounding effects 
caused by the donors' genetics, and the use of h i P S C ’s offers the advantage that there 
is no limit on the number of different “people” that can be tested. An important take 
home point from Hnatiuk et al. is that to date, all published large-scale drug screens 

 
A-29 
Complement-ARIE 
Landscape Analysis 
have used h i P S C s from a small number of healthy donors and future studies should look 
t
o include stem cells from patients with mutations relevant to the disease being studied. 
 
 
 
 
Review
 of Workforce Considerations Findings 
Eleven manuscripts were identified as having potential information on workforce 
considerations with five of these covering in silico approaches under AI/machine 
learning. A brief review of abstracts and a subset of the manuscripts revealed limited 
relevant information and suggests the search strategy to identify references with 
information on workforce considerations may require revision. While not focused on 
workforce considerations for NAMs, Miller et al. 2023 published a manuscript entitled 
Machine Learn
ing in Clinical Trials: A Primer with Applications to Neurology (Miller et 
al., 2023). The authors present ways in which AI and machine learning can be used to 
facilitate successful clinical trials and discuss technical and regulatory challenges. 
Manual In
ternet Search on Population Diversity and Workforce Considerations 
Given the limited material identified using the automated search we conducted a 
cursory, manual internet search for material on both population diversity or workforce 
considerations. This search reveals manuscripts that discuss considerations for NAM 
application (Petersen et al., 2022; Stucki et al., 2022); however, these manuscripts 
generally appear to have little information on workforce considerations. While an 
automated search with revised search terms may be helpful, it’s possible there is simply 
a lack of information on workforce considerations with NAMs. 
In terms of specific material on population diversity, this quick search did reveal the 
2023 SACATM report entitled Using New Approach Methodologies to Address 
Variability and Susceptibility Across Populations – Report from the October 2022 
Symposium/Workshop (Hogberg, 2023) which included a c all for relevant papers that 
would be expected to provide useful material on population diversity. 
In Depth Explora
tion of Specific Areas of Interest 
Using this landscape analysis as a starting point, there is ample opportunity to retrieve 
and review current research activity on specific areas of interest. For example, EPA 
expressed a strong interest in NAMs for breast and prostate cancer during the 
C
omplement-ARIE strategic planning process. As an example, we looked for breast 
cancer manuscripts within the retrieved literature. To accomplish this, the retrieved 
manuscripts were filtered for the term “breast cancer” within the tag for “disease”. This 
text search produced 112 manuscripts, including 39 manuscripts identified as using AI. 
A quick manual screen of this subset of manuscripts revealed materials that may be of 
interest including a recent review by Orsini et al (2023 entitled Omics Technologies 

 
A-30 
Complement-ARIE 
Landscape Analysis 
Improving Breast Cancer Research and Diagnostics ((Orsini et al., 2023). To prepare 
their review, Orsini et al screened PubMed and Medline for manuscripts discussing 
omics research for breast cancer evolution and progression published between the 
years 2010 and 2023. The authors summarize their findings as follows “This review 
focuses on the findings of recent multi-omics-based research that has been applied to 
BC research, with an introduction to every omics technique and their applications for the 
different BC phenotypes, biomarkers, target therapies, diagnosis, treatment and 
prognosis, to provide a comprehensive overview of the possibilities of BC research.” A 
thorough review of retrieved literature would likely identify other manuscripts of interest 
that could be used, in this case, to review the state of the science for breast cancer 
research but could be applied to numerous other areas of interest. 
 
 
For on-going or future efforts, the following recommendations/action items are proposed 
to provide further insight into the current landscape of NAMs for biomedical use and 
proposal
s for future programmatic efforts to develop the biomedical NAMs field beyond 
its current capacity. As described previously, several areas lack robust efforts, 
particularly with respects to individual variability, workplace effects, etc. Efforts directed 
toward these areas would be highly recommended. 
Potent
ial Future Directions and Opportunities for Additional Analyses 
• Conduct more extensive post-processing and curation of the generative AI 
outputs to confirm quality and establish additional trends in the available data for 
further investigation. 
• Conduct additional in-depth review of generative AI outputs, such as: 
o Summarize common limitations by assay group 
o Summarize most commonly used methods 
o Review coverage of each cell and tissue type within each technology type 
• Conduct supplemental literature searches focused on population variability  
• Conduct supplemental literature searches focused on the workforces needed for 
implementation of NAMs.  
• Review the full range of studies retrieved to evaluate trends indicative of NAMs 
inc
reasing (or declining) in the extent to which they are being used in biomedical 
research.  
• D ev
elop an action plan for the implementation of FAIR data practices 
• Implement research programs to develop and utilize combinatorial NAM 
approaches 
• Conduct reviews to understand epigenetic reprogramming in i P S C  and i P S C-
derived organoid models and determine how reflective the epigenetic profile is of 
a mature in vivo cell. 
 

 
A-31 
Complement-ARIE 
Landscape Analysis 
Reference List 
 
Anwardeen, N.R., Diboun, I., Mokrab, Y., Althani, A.A., Elrayess, M.A., 2023. Statistical 
methods and resources for biomarker discovery using metabolomics. BMC 
Bioinformatics 24, 250. https://doi.org/10.1186/s12859-023-05383-0 
Audouze, K., Sarigiannis, D., Alonso-Magdalena, P., Brochot, C., Casas, M., Vrijheid, 
M., Babin, P.J., Karakitsios, S., Coumoul, X., Barouki, R., 2020. Integrative 
Strategy of Testing Systems for Identification of Endocrine Disruptors Inducing 
Metabolic Disorders—An Introduction to the OBERON Project. International 
Journal of Molecular Sciences 21, 2988. https://doi.org/10.3390/ijms21082988 
Bai, J., Wang, C., 2020. Organoids and Microphysiological Systems: New Tools for 
Ophthalmic Drug Discovery. Frontiers in Pharmacology 11. 
Barnhill, J., Gaston, J.D., Deffenbaugh, P.I., Wagner, L., Liacouras, P.C., Ho, V.B., 
2023. Additive Manufacturing for Fabrication of Point-of-Care Therapies in 
Austere Environments. Military Medicine 188, e1847–e1853. 
https://doi.org/10.1093/milmed/usad007 
Brown, E.C., Hallinger, D.R., Simmons, S.O., 2023. High-throughput AR dimerization 
assay identifies androgen disrupting chemicals and metabolites. Frontiers in 
Toxicology 5. 
Buskin, A., Scott, E., Nelson, R., Gaughan, L., Robson, C.N., Heer, R., Hepburn, A.C., 
2023. Engineering prostate cancer in vitro: what does it take? Oncogene 42, 
2417–2427. https://doi.org/10.1038/s41388-023-02776-6 
Cawley, M., Beardslee, R., Beverly, B., Hotchkiss, A., Kirrane, E., Sams, R., Varghese, 
A., Wignall, J., Cowden, J., 2020. Novel text analytics approach to identify 
relevant literature for human health risk assessments: A pilot study with health 
effects of in utero exposures. Environ Int 134, 105228. 
https://doi.org/10.1016/j.envint.2019.105228 
Chan, W.S., Mo, X., Ip, P.P.C., Tse, K.Y., 2023. Patient-derived organoid culture in 
epithelial ovarian cancers—Techniques, applications, and future perspectives. 
Cancer Medicine 12, 19714–19731. https://doi.org/10.1002/cam4.6521 
Connolly, E.A., Grimison, P.S., Horvath, L.G., Robinson, P.J., Reddel, R.R., 2023. 
Quantitative proteomic studies addressing unmet clinical needs in sarcoma. 
Frontiers in Oncology 13. 
Cota-Coronado, A., Ramírez-Rodríguez, P.B., Padilla-Camberos, E., Díaz,  éNstor F., 
Flores-Fernández, J.M., Ávila-Gónzalez, D., Diaz-Martinez, N.E., 2019. 
Implications of human induced pluripotent stem cells in metabolic disorders: from 
drug discovery toward precision medicine. Drug Discovery Today 24, 334–341. 
https://doi.org/10.1016/j.drudis.2018.10.001 
Criscione, J., Rezaei, Z., Hernandez Cantu, C.M., Murphy, S., Shin, S.R., Kim, D.-H., 
2023. Heart-on-a-chip platforms and biosensor integration for disease modeling 
and phenotypic drug screening. Biosens Bioelectron 220, 114840. 
https://doi.org/10.1016/j.bios.2022.114840 
Di, L., 2023. Recent advances in measurement of metabolic clearance, metabolite 
profile and reaction phenotyping of low clearance compounds. Expert Opinion on 
Drug Discovery 18, 1209–1219. https://doi.org/10.1080/17460441.2023.2238606 

 
A-32 
Complement-ARIE 
Landscape Analysis 
Dixon, T.A., Muotri, A.R., 2023. Advancing preclinical models of psychiatric disorders 
with human brain organoid cultures. Mol Psychiatry 28, 83–95. 
https://doi.org/10.1038/s41380-022-01708-2 
Gao, X., Yourick, J.J., Sprando, R.L., 2023. Toxicological applications of human 
induced pluripotent stem cell-derived hepatocyte-like cells: an updated review. 
The Journal of Toxicological Sciences 48, 441–456. 
https://doi.org/10.2131/jts.48_441 
Hnatiuk, A.P., Briganti, F., Staudt, D.W., Mercola, M., 2021. Human i P S C modeling of 
heart disease for drug development. Cell Chemical Biology 28, 271–282. 
https://doi.org/10.1016/j.chembiol.2021.02.016 
Hogberg, H., 2023. Using New Approach Methodologies to Address Variability and 
Susceptibility Across Populations – Report from the October 2022 
Symposium/Workshop. 
Hutchison, V.B., Zolly, L., Norkin, T., Hsu, L., Hou, C.-Y., 2023. US GS State of the Data 
Project: Rubric and Assessment Data. https://doi.org/10.5066/P97V4XA4 
Li, M., Yu, H., Li, Y., Li, X., Huang, S., Liu, X., Weng, G., Xu, L., Hou, T., Guo, D.-S., 
Wang, Y., 2023. Rational design of supramolecular self-assembly sensor for 
living cell imaging of HDAC1 and its application in high-throughput screening. 
Biosensors and Bioelectronics 242, 115716. 
https://doi.org/10.1016/j.bios.2023.115716  
Miller, M.I., Shih, L.C., Kolachalama, V.B., 2023. Machine Learning in Clinical Trials: A 
Primer with Applications to Neurology. Neurotherapeutics 20, 1066–1080. 
https://doi.org/10.1007/s13311-023-01384 -2 
Orsini, A., Diquigiovanni, C., Bonora, E., 2023. Omics Technologies Improving Breast 
Cancer Research and Diagnostics. International Journal of Molecular Sciences 
24, 12690. https://doi.org/10.3390/ijms241612690 
Petersen, E.J., Ceger, P., Allen, D.G., Coyle, J., Derk, R., Garcia-Reyero, N., Gordon, 
J., Kleinstreuer, N.C., Matheson, J., McShan, D., Nelson, B.C., Patri, A.K., Rice, 
P., Rojanasakul, L., Sasidharan, A., Scarano, L., Chang, X., 2022. U.S. federal 
agency interests and key considerations for new approach methodologies for 
nanomaterials. ALTEX - Alternatives to animal experimentation 39, 183–206. 
https://doi.org/10.14573/altex.2105041 
Pike, C.M., Zwarycz, B., McQueen, B.E., Castillo, M., Barron, C., Morowitz, J.M., Levi, 
J.A., Phadke, D., Balik-Meisner, M., Mav, D., Shah, R., Glasspoole, D.L.C., 
Laetham, R., Thelin, W., Bunger, M.K., Boazak, E.M., 2023. Characterization and 
optimization of variability in a human colonic epithelium culture model. 
https://doi.org/10.1101/2023.09.22.559007 
Reddy, N., Lynch, B., Gujral, J., Karnik, K., 2023. Alternatives to animal testing in 
toxicity testing: Current status and future perspectives in food safety 
assessments. Food and Chemical Toxicology 179, 113944. 
https://doi.org/10.1016/j.fct.2023.113944 
Stucki, A.O., Barton-Maclaren, T.S., Bhuller, Y., Henriquez, J.E., Henry, T.R., Hirn, C., 
Miller-Holt, J., Nagy, E.G., Perron, M.M., Ratzlaff, D.E., Stedeford, T.J., 
Clippinger, A.J., 2022. Use of new approach methodologies (NAMs) to meet 
regulatory r
equirements for the assessment of industrial chemicals and 
pesticides for effects on human health. Frontiers in Toxicology 4. 

 
A-33 
Complement-ARIE 
Landscape Analysis 
Wilkinson, M.D., Dumontier, M., Aalbersberg, Ij.J., Appleton, G., Axton, M., Baak, A., 
Blomberg, N., Boiten, J.-W., da Silva Santos, L.B., Bourne, P.E., Bouwman, J., 
Brookes, A.J., Clark, T., Crosas, M., Dillo, I., Dumon, O., Edmunds, S., Evelo, 
C.T., Finkers, R., Gonzalez-Beltran, A., Gray, A.J.G., Groth, P., Goble, C., 
Grethe, J.S., Heringa, J., ’t Hoen, P.A.C., Hooft, R., Kuhn, T., Kok, R., Kok, J., 
Lusher, S.J., Martone, M.E., Mons, A., Packer, A.L., Persson, B., Rocca-Serra, 
P., Roos, M., van Schaik, R., Sansone, S.-A., Schultes, E., Sengstag, T., Slater, 
T., Strawn, G., Swertz, M.A., Thompson, M., van der Lei, J., van Mulligen, E., 
Velterop, J., Waagmeester, A., Wittenburg, P., Wolstencroft, K., Zhao, J., Mons, 
B., 2016. The FAIR Guiding Principles for scientific data management and 
stewardship. Sci Data 3, 160018. https://doi.org/10.1038/sdata.2016.18 
Zagirova, D., Pushkov, S., Leung, G.H.D., Liu, B.H.M., Urban, A., Sidorenko, D., 
Kalashnikov, A., Kozlova, E., Naumov, V., Pun, F.W., Ozerov, I.V., Aliper, A., 
Zhavoronkov, A., 2023. Biomedical generative pre-trained based transformer 
language model for age-related disease target discovery. Aging (Albany NY) 15, 
9293–9309. https://doi.org/10.18632/aging.205055 
  

 
A-34 
Complement-ARIE 
Landscape Analysis 
Appendix A. Initial Search Strategy 
 
Table 6. Search Strategy for PubMed* 
Set Topic Search Strategy for PubMed Initial 
Results 
(No Limits) 
1 NAMs "Animal Testing Alternative"[t i a b ] OR "Animal Testing 
Alternatives"[t i a b ] OR "Animal Use Alternative"[t i a b ] OR 
"Animal Use Alternatives"[t i a b ] OR "computational 
toxicology"[t i a b ] OR "high content"[t i a b ] OR "high 
throughput"[t i a b ] OR "high-throughput"[t i a b ] OR  
"HTS"[t i a b ] OR "HTTr"[t i a b ] OR "integrated testing 
strategies"[t i a b ] OR "integrated testing strategy"[t i a b ] OR 
"NAMs"[t i a b ] OR 3R[t  i a b ] OR 3Rs[t i a b ] OR “Animal 
alternative*”[t i a b ] OR "assessment batteries"[t i a b ] OR 
"assessment battery"[t i a b ] OR "test batteries"[t i a b ] OR 
"test battery"[t i a b ] OR “Test system*”[t i a b ] OR 
((“alternative*”[t i a b ] OR “predictive”[t i a b ] OR “non- 
animal”[t i a b ] OR “new approach*”[t i a b ] OR novel[t i a b ]) 
AND (method*[t i a b ] OR approach*[t i a b ] OR model*[t i a b ] 
OR test*[t i a b ] OR assay*[t i a b ])) 
1,988,623 
2 In vitro 
models 
(("3D tissue model"[t i a b ] OR "3D tissue models"[t i a b ] OR 
"biomarker"[t i a b ] OR "biomarkers"[t i a b ] OR "embryonic 
stem cell"[t i a b ] OR "embryonic stem cells"[t i a b ] OR 
"Engineered organoid"[t i a b ] OR "Engineered  
organoids"[t i a b ] OR "Functionally integrate"[t i a b ] OR 
"Functionally integrated"[t i a b ] OR "gene expression"[t i a b ] 
OR genomic*[t i a b ] OR "h E S C "[t i a b ] OR "human  
embryonic stem cell"[t i a b ] OR "human embryonic stem 
cells"[t i a b ] OR "in vitro"[t i a b ] OR "induced pluripotent"[t i a b ] 
OR "micromass"[t i a b ] OR "Microfabrication"[t i a b ] OR 
Microfluidic*[t i a b ] OR "Microphysiological Systems"[t i a b ] 
OR "Microphysiological System"[t i a b ] OR  
microdevice*[t i a b ] OR "Organ chip"[t i a b ] OR "Organ 
chips"[t i a b ] OR "organ-on-a-chip"[t i a b ] OR organoid*[t i a b ] 
OR "pharmacokinetic"[t i a b ] OR "Phenotype 
disappearance"[t i a b ] OR "Physiological relevance"[t i a b ] 
OR "Pluripotent Stem Cell"[t i a b ] OR "pluripotent stem 
3,049,541 

 
A-35 
Complement-ARIE 
Landscape Analysis 
Set Topic Search Strategy for PubMed Initial 
Results 
(No Limits) 
cells"[t i a b ] OR "Quantitative systems pharmacology"[t i a b ] 
OR "Reporter gene"[t i a b ] OR "Reporter genes"[t i a b ] OR 
"Single cell analysis"[t i a b ] OR "Stem Cell"[t i a b ] OR "Stem 
Cells"[t i a b ] OR "Tissue-engineered organ construct"[t i a b ] 
OR "Tissue-engineered organ constructs"[t i a b ] OR 
"Tissue-on-chip"[t i a b ] OR "Tissue-on-a-chip"[t i a b ]  OR 
"Tissue chip"[t i a b ]  OR "toxicogenomic"[t i a b ] OR 
"toxicogenomics"[t i a b ] OR "toxicokinetic"[t i a b ] OR 
"toxicokinetics"[t i a b ] OR "transcriptome"[t i a b ] OR 
"transcriptomics"[t i a b ] OR "Vascularization"[t i a b ]) OR 
(“Test side effects”[t i a b ] AND “non-target tissues”[t i a b ]) OR 
spheroid*[t i a b ] OR coculture[t i a b ] OR “co-culture”[t i a b ] OR 
“cell culture”[t i a b ] OR “primary culture”[t i a b ])  
3 In 
silico 
models  
(Algorithm*[t i a b ] OR bioinformat*[t i a b ] OR "Chemical 
space"[t i a b ] OR "Chemical space"[t i a b ] OR "Chemical 
spaces"[t i a b ] OR "Chemical structure"[t i a b ] OR "Chemical 
structures"[t i a b ] OR cheminformat*[t i a b ] OR 
"Chemogenomic"[t i a b ] OR "Chemogenomics"[t i a b ] OR 
"Computational model"[t i a b ] OR "Computational  
models"[t i a b ] OR "computational study"[t i a b ] OR 
"computational analysis"[t i a b ] OR “computer model”[t i a b ] 
OR "mathematical models"[t i a b ] OR "mathematical 
model"[t i a b ]  OR Simulation*[t i a b ] OR "Deep learning"[t i a b ] 
OR "Disease database"[t i a b ] OR "Disease databases"[t i a b ] 
OR "Docking software"[t i a b ] OR "Drug database"[t i a b ] OR 
"Drug databases"[t i a b ] OR "in silico"[t i a b ] OR "In vitro to in 
vivo extrapolation"[t i a b ] OR "informatics"[t i a b ] OR  
"I V I V E "[t i a b ] OR "Machine learning"[t i a b ] OR “artificial 
intelligence”[t i a b ] OR "Molecular Docking"[t i a b ] OR 
"Molecular Dynamics"[t i a b ] OR "PBPK"[t i a b ] OR 
"Pharmacokinetic"[t i a b ] OR "Pharmacodynamic"[t i a b ] OR 
"toxicokinetic"[t i a b ] OR "toxicodynamic"[t i a b ] OR 
"Pharmacology database"[t i a b ] OR "Pharmacology 
databases"[t i a b ] OR "Protein space"[t i a b ] OR "Q SAR"[t i a b ] 
OR "quantitative structure activity relationship"[t i a b ] OR 
"Read-across"[t i a b ] OR "Small molecule database"[t i a b ] 
1,326,522 

 
A-36 
Complement-ARIE 
Landscape Analysis 
Set Topic Search Strategy for PubMed Initial 
Results 
(No Limits) 
OR "Small molecule databases"[t i a b ] OR "Structural 
database"[t i a b ] OR "Structural databases"[t i a b ] OR 
"structure activity relationship"[t i a b ] OR “Digital Twins”[t i a b ] 
OR “multiscale models”[t i a b ]) 
4 In 
chemico 
models  
("In chemico"[t i a b ] OR "Virtual tissue model"[t i a b ] OR 
"Virtual tissue models"[t i a b ] OR "Exposure model"[t i a b ] OR 
"Exposure models"[t i a b ]  OR "Cell-free assays"[t i a b ] OR 
"Cell-free assay"[t i a b ] OR "Synthetic biochemistry"[t i a b ] 
OR "Receptor binding"[t i a b ] OR  "Synthetic biology"[t i a b ] 
OR  "Ligand binding"[t i a b ] OR “biochemical assay”[t i a b ]) 
98,383 
 Other 
limits 
Reviews: ((english[Filter] AND 2018:2024[pdat] AND 
hasabstract AND (Review[pt] OR Systematic Review[pt])) 
 
*Ran on October 10, 2023 using https://pubmed.ncbi.nlm.nih.gov/ 
 

 
B-1 
Complement-ARIE 
Landscape Analysis 
Appendix B. Title/Abstract Screening and Extraction 
Overall Methods 
Each reference was reviewed and screened for relevance by a primary staff person who 
noted high level information about each reference (see instructions, below). A study was 
considered relevant if it met the inclusion criteria outlined below. Each reference was 
also reviewed by a second person for QA purposes, to confirm the original 
categorization and extraction was accurate. 
Inclusion Criteria – if any of the following criteria were met, it was considered 
relevant 
• Contains information related to the development or application of a NAM for a 
human-relevant endpoint or biological process 
• Could putatively be a replacement for an in vivo animal test  
• NAM must not rely solely on animal tissue or data  
o For in vitro and in chemico studies, should be exclusively human 
o For in silico models, it is relevant if it was built using animal data if it is 
predicting a human relevant outcome  
• Data are collected from a relevant model system/using a relevant technology 
Exclusion Criteria 
• The study does not describe an alternative test method/model that meets the 
requirements above, where the context is related to recapitulating a relevant 
human physiological process or increasing our understanding of a biological 
process  
• Model or approach could not be used in a biomedical context  
• Model or approach makes use of whole organisms (including mice, humans, 
whole embryos)  
• Model is designed for application in an ecological context (making decisions 
about health of organisms in the environment, not humans)  
• Diagnostic method related to diagnosing outcomes in humans  
• Replacing a method that already does not use animals (e.g., micromass culture 
derived from a chick embryo, mouse cell culture lines) 
• Biomedical devices 
• Data collected for the purpose of studying plants, pathogenic bacteria, 
microorganisms  
• Other exclusion criteria: 
o Secondary literature (letters to the editor, notes, meeting abstract, etc.)  
o Not in English  
o Retracted publication 

 
B-2 
Complement-ARIE 
Landscape Analysis 
Supplemental Categories 
FAIR: Discussion of data availability, any FAIR concept, database or other 
repository  
Animal-based NAM: NAM but animal-based (using animal tissue – whole 
organisms are excluded) 
Potential application in biomedical research: Catch-all bin for when the paper 
has the potential for being relevant to a biomedical context and replacing animal 
tests, but the authors do not necessarily make that point explicitly  

 
B-3 
Complement-ARIE 
Landscape Analysis 
Instructions for Litstream® form 
 
 
 


 
4 
 
Complement-ARIE 
Landscape Analysis 
Appendix C. Broad Search Strategy 
Table 7. Search Strategy for PubMed* 
Set Topic Search Strategy for PubMed Initial 
Results 
(No Limits) 
1 NAMs "Animal Testing Alternative"[t i a b ] OR "Animal Testing 
Alternatives"[t i a b ] OR "Animal Use Alternative"[t i a b ] OR 
"Animal Use Alternatives"[t i a b ] OR "computational 
toxicology"[t i a b ] OR "high content"[t i a b ] OR "high 
throughput"[t i a b ] OR "high-throughput"[t i a b ] OR  
"HTS"[t i a b ] OR "HTTr"[t i a b ] OR "integrated testing 
strategies"[t i a b ] OR "integrated testing strategy"[t i a b ] OR 
"NAMs"[t i a b ]  OR 3R[ t i a b ] OR 3Rs[t i a b ] OR “Animal 
alternative*”[t i a b ] OR "assessment batteries"[t i a b ] OR 
"assessment battery"[t i a b ] OR "test batteries"[t i a b ] OR 
"test battery"[t i a b ] OR “Test system*”[t i a b ] OR 
((“alternative*”[t i a b ] OR “predictive”[t i a b ] OR “non- 
animal”[t i a b ] OR “new approach*”[t i a b ] OR novel[t i a b ]) 
AND (method*[t i a b ] OR approach*[t i a b ] OR model*[t i a b ] 
OR test*[t i a b ] OR assay*[t i a b ])) 
1,988,623 
2 In vitro 
models 
(("3D tissue model"[t i a b ] OR "3D tissue models"[t i a b ] OR 
"biomarker"[t i a b ] OR "biomarkers"[t i a b ] OR "embryonic 
stem cell"[t i a b ] OR "embryonic stem cells"[t i a b ] OR 
"Engineered organoid"[t i a b ] OR "Engineered  
organoids"[t i a b ] OR "Functionally integrate"[t i a b ] OR 
"Functionally integrated"[t i a b ] OR "gene expression"[t i a b ] 
OR genomic*[t i a b ] OR "h E S C "[t i a b ] OR "human 
embryonic stem cell"[t i a b ] OR "human embryonic stem 
cells"[t i a b ] OR "in vitro"[t i a b ] OR "induced pluripotent"[t i a b ] 
OR "micromass"[t i a b ] OR "Microfabrication"[t i a b ] OR 
Microfluidic*[t i a b ] OR "Microphysiological Systems"[t i a b ] 
OR "Microphysiological System"[t i a b ] OR  
microdevice*[t i a b ] OR "Organ chip"[t i a b ] OR "Organ 
chips"[t i a b ] OR "organ-on-a-chip"[t i a b ] OR organoid*[t i a b ] 
OR "pharmacokinetic"[t i a b ] OR "Phenotype 
disappearance"[t i a b ] OR "Physiological relevance"[t i a b ] 
OR "Pluripotent Stem Cell"[t i a b ] OR "pluripotent stem 
cells"[t i a b ] OR "Quantitative systems pharmacology"[t i a b ] 
OR "Reporter gene"[t i a b ] OR "Reporter genes"[t i a b ] OR 
3,049,541 

 
5 
 
Complement-ARIE 
Landscape Analysis 
Set Topic Search Strategy for PubMed Initial 
Results 
(No Limits) 
"Single cell analysis"[t i a b ] OR "Stem Cell"[t i a b ] OR "Stem 
Cells"[t i a b ] OR "Tissue-engineered organ construct"[t i a b ] 
OR "Tissue-engineered organ constructs"[t i a b ] OR 
"Tissue-on-chip"[t i a b ] OR "Tissue-on-a-chip"[t i a b ]  OR 
"Tissue chip"[t i a b ]  OR "toxicogenomic"[t i a b ] OR 
"toxicogenomics"[t i a b ] OR "toxicokinetic"[t i a b ] OR 
"toxicokinetics"[t i a b ] OR "transcriptome"[t i a b ] OR 
"transcriptomics"[t i a b ] OR "Vascularization"[t i a b ]) OR 
(“Test side effects”[t i a b ] AND “non-target tissues”[t i a b ]) OR 
spheroid*[t i a b ] OR coculture[t i a b ] OR “co-culture”[t i a b ] OR 
“cell culture”[t i a b ] OR “primary culture”[t i a b ])  
3 In silico 
models  
(Algorithm*[t i a b ] OR bioinformat*[t i a b ] OR "Chemical 
space"[t i a b ] OR "Chemical space"[t i a b ] OR "Chemical 
spaces"[t i a b ] OR "Chemical structure"[t i a b ] OR "Chemical 
structures"[t i a b ] OR cheminformat*[t i a b ] OR 
"Chemogenomic"[t i a b ] OR "Chemogenomics"[t i a b ] OR 
"Computational model"[t i a b ] OR "Computational  
models"[t i a b ] OR "computational study"[t i a b ] OR 
"computational analysis"[t i a b ] OR “computer model”[t i a b ] 
OR "mathematical models"[t i a b ] OR "mathematical 
model"[t i a b ]  OR Simulation*[t i a b ] OR "Deep learning"[t i a b ] 
OR "Disease database"[t i a b ] OR "Disease  
databases"[t i a b ] OR "Docking software"[t i a b ] OR "Drug 
database"[t i a b ] OR "Drug databases"[t i a b ] OR "in  
silico"[t i a b ] OR "In vitro to in vivo extrapolation"[t i a b ] OR 
"informatics"[t i a b ] OR "I V I V E "[t i a b ] OR "Machine 
learning"[t i a b ] OR “artificial intelligence”[t i a b ] OR 
"Molecular Docking"[t i a b ] OR "Molecular Dynamics"[t i a b ] 
OR "PBPK"[t i a b ] OR "Pharmacokinetic"[t i a b ] OR 
"Pharmacodynamic"[t i a b ] OR "toxicokinetic"[t i a b ] OR 
"toxicodynamic"[t i a b ] OR "Pharmacology database"[t i a b ] 
OR "Pharmacology databases"[t i a b ] OR "Protein  
space"[t i a b ] OR "Q SAR"[t i a b ] OR "quantitative structure 
activity relationship"[t i a b ] OR "Read-across"[t i a b ] OR 
"Small molecule database"[t i a b ] OR "Small molecule 
databases"[t i a b ] OR "Structural database"[t i a b ] OR 
1,326,522 

 
6 
 
Complement-ARIE 
Landscape Analysis 
Set Topic Search Strategy for PubMed Initial 
Results 
(No Limits) 
"Structural databases"[t i a b ] OR "structure activity 
relationship"[t i a b ] OR “Digital Twins”[t i a b ] OR “multiscale 
models”[t i a b ]) 
4 In 
chemico 
models  
("In chemico"[t i a b ] OR "Virtual tissue model"[t i a b ] OR 
"Virtual tissue models"[t i a b ] OR "Exposure model"[t i a b ] OR 
"Exposure models"[t i a b ]  OR "Cell-free assays"[t i a b ] OR 
"Cell-free assay"[t i a b ] OR "Synthetic biochemistry"[t i a b ] 
OR "Receptor binding"[t i a b ] OR  "Synthetic biology"[t i a b ] 
OR  "Ligand binding"[t i a b ] OR “biochemical assay”[t i a b ]) 
98,383 
 Other 
limits 
Reviews: ((english[Filter] AND 2023:2024[pdat] AND 
hasabstract AND (Review[pt] OR Systematic Review[pt])) 
 
*Ran on October 23, 2023 using https://pubmed.ncbi.nlm.nih.gov/ 
 
Table 8. Search Strategy for Web of Science* 
Set Topic Search Strategy for Web of Science Initial 
Results 
(No Limits) 
1 NAMs "Animal Testing Alternative" OR "Animal Testing 
Alternatives" OR "Animal Use Alternative" OR "Animal Use 
Alternatives" OR "computational toxicology" OR "high 
content" OR "high throughput" OR "high-throughput" OR 
"HTS" OR "HTTr" OR "integrated testing strategies" OR 
"integrated testing strategy" OR "NAMs" OR 3R OR 3Rs 
OR “
Animal alternative*” OR "assessment batteries" OR 
"assessment battery" OR "test batteries" OR "test battery" 
OR “Test system*” OR ((“alternative*” OR “predictive” OR 
“non-animal” OR “new approach*” OR novel) AND 
(method* OR approach* OR model* OR test* OR assay*)) 
3,972,818 
2 In vitro 
models 
(("3D tissue model" OR "3D tissue models" OR 
"biomarker" OR "biomarkers" OR "embryonic stem cell" 
OR "embryonic stem cells" OR "Engineered organoid" OR 
"Engineered organoids" OR "Functionally integrate" OR 
"Functionally integrated" OR "gene expression" OR 
genomic* OR "h E S C " OR "human embryonic stem cell" 
4,161,732 

 
7 
 
Complement-ARIE 
Landscape Analysis 
Set Topic Search Strategy for Web of Science Initial 
Results 
(No Limits) 
OR "human embryonic stem cells" OR "in vitro" OR 
"induced pluripotent" OR "micromass" OR 
"Microfabrication" OR Microfluidic* OR "Microphysiological 
Systems" OR "Microphysiological System" OR 
microdevice* OR "Organ chip" OR "Organ chips" OR 
"organ-on-a-chip" OR organoid* OR "pharmacokinetic" OR 
"Phenotype disappearance" OR "Physiological relevance" 
OR "Pluripotent Stem Cell" OR "pluripotent stem cells" OR 
"Quantitative systems pharmacology" OR "Reporter gene" 
OR "Reporter genes" OR "Single cell analysis" OR "Stem 
Cell" OR "Stem Cells" OR "Tissue-engineered organ 
construct" OR "Tissue-engineered organ constructs" OR 
"Tissue-on-chip" OR "Tissue-on-a-chip"  OR "Tissue chip"  
OR "toxicogenomic" OR "toxicogenomics" OR 
"toxicokinetic" OR "toxicokinetics" OR "transcriptome" OR 
"transcriptomics" OR "Vascularization") OR (“Test side 
effects” AND “non-target tissues”) OR spheroid* OR 
coculture OR “co-culture” OR “cell culture” OR “primary 
culture”)  
3 In 
silico 
models  
(Algorithm* OR bioinformat* OR "Chemical space" OR 
"Chemical spaces" OR "Chemical structure" OR "Chemical 
structures" OR cheminformat* OR "Chemogenomic" OR 
"Chemogenomics" OR "Computational model" OR 
"Computational models" OR "computational study" OR 
"computational analysis" OR “computer model” OR 
"mathematical models" OR "mathematical model"  OR 
Simulation* OR "Deep learning" OR "Disease database" 
OR "Disease databases" OR "Docking software" OR "Drug 
database" OR "Drug databases" OR "in silico" OR "In vitro 
to in vivo extrapolation" OR "informatics" OR "I V I V E " OR 
"Machine learning" OR “artificial intelligence” OR 
"Molecular Docking" OR "Molecular Dynamics" OR "PBPK" 
OR "Pharmacokinetic" OR "Pharmacodynamic" OR 
"toxicokinetic" OR "toxicodynamic" OR "Pharmacology 
database" OR "Pharmacology databases" OR "Protein 
Aspace" OR "Q SAR" OR "quantitative structure activity 
6,710,316 

 
8 
 
Complement-ARIE 
Landscape Analysis 
Set Topic Search Strategy for Web of Science Initial 
Results 
(No Limits) 
relationship" OR "Read-across" OR "Small molecule 
database" OR "Small molecule databases" OR "Structural 
database" OR "Structural databases" OR "structure activity 
relationship" OR “Digital Twins”) 
4 In 
chemico 
models  
("In chemico" OR "Virtual tissue model" OR "Virtual tissue 
models" OR "Exposure model" OR "Exposure models" OR 
"Cell-free assays" OR "Cell-free assay" OR "Synthetic 
biochemistry" OR "Receptor binding" OR "Synthetic 
biology" OR "Ligand binding" OR “biochemical assay”) 
128,827 
 Other 
limits 
2023 or 2024 (Publication Years) and Article or Review 
Article (Document Types) and English (Languages) and 
Biochemistry Molecular Biology or Materials Science 
Multidisciplinary or Oncology or Pharmacology Pharmacy 
or Medicine Research Experimental or Genetics Heredity 
or Cell Biology or Neurosciences or Mathematical 
Computational Biology or Biochemical Research Methods 
or Biology or Materials Science Biomaterials or Toxicology 
or Respiratory System or Cell Tissue Engineering or 
Reproductive Biology or Materials Science Composites or 
Developmental Biology (Web of Science Categories) 
 
*Ran on October 23, 2023 using https://www.webofscience.com/wos  
 
Table 9. Search Strategy for Scopus* 
Set Topic Search Strategy for Scopus Initial 
Results 
(No Limits) 
1 NAMs TITLE-ABS ( "Animal Testing Alternative" OR "Animal 
Testing Alternatives" OR "Animal Use Alternative" OR 
"Animal Use Alternatives" OR "computational toxicology" 
OR "high content" OR "high throughput" OR "high-
throughput" OR "HTS" OR "HTTr" OR "integrated testing 
strategies" OR "integrated testing strategy" OR "NAMs" 
OR 3r OR
 3rs OR "Animal alternative*" OR "assessment 
batteries" OR "assessment battery" OR "test batteries" OR 
4,753,857 
 
 
 
 
 

 
9 
 
Complement-ARIE 
Landscape Analysis 
Set Topic Search Strategy for Scopus Initial 
Results 
(No Limits) 
"test battery" OR "Test system*" OR ( ( "alternative*" OR 
"predictive" OR "non-animal" OR "new approach*" OR 
novel ) AND ( method* OR approach* OR model* OR test* 
OR assay* ) ) ) 
2 In vitro 
models 
TITLE-ABS ( "3D tissue model" OR "3D tissue models" OR 
"biomarker" OR "biomarkers" OR "embryonic stem cell" 
OR "embryonic stem cells" OR "Engineered organoid" OR 
"Engineered organoids" OR "Functionally integrate" OR 
"Functionally integrated" OR "gene expression" OR 
genomic* OR "h E S C " OR "human embryonic stem cell" 
OR "human embryonic stem cells" OR "in vitro" OR 
"induced pluripotent" OR "micromass" OR 
"Microfabrication" OR microfluidic* OR "Microphysiological 
Systems" OR "Microphysiological System" OR 
microdevice* OR "Organ chip" OR "Organ chips" OR 
"organ-on-a-chip" OR organoid* OR "pharmacokinetic" OR 
"Phenotype disappearance" OR "Physiological relevance" 
OR "Pluripotent Stem Cell" OR "pluripotent stem cells" OR 
"Quantitative systems pharmacology" OR "Reporter gene" 
OR "Reporter genes" OR "Single cell analysis" OR "Stem 
Cell" OR "Stem Cells" OR "Tissue-engineered organ 
construct" OR "Tissue-engineered organ constructs" OR 
"Tissue-on-chip" OR "Tissue-on-a-chip" OR "Tissue chip" 
OR "toxicogenomic" OR "toxicogenomics" OR 
"toxicokinetic" OR "toxicokinetics" OR "transcriptome" OR 
"transcriptomics" OR "Vascularization" ) OR ( "Test side 
effects" AND "non-target tissues" ) OR spheroid* OR 
coculture OR "co-culture" OR "cell culture" OR "primary 
culture" 
4,955,213 
3 In 
silico 
models  
TITLE-ABS ( algorithm* OR bioinformat* OR "Chemical 
space" OR "Chemical space" OR "Chemical spaces" OR 
"Chemical structure" OR "Chemical structures" OR 
cheminformat* OR "Chemogenomic" OR 
"Chemogenomics" OR "Computational model" OR 
"Computational models" OR "computational study" OR 
"computational analysis" OR "computer model" OR 
8,434,230 

 
10 
 
Complement-ARIE 
Landscape Analysis 
Set Topic Search Strategy for Scopus Initial 
Results 
(No Limits) 
"mathematical models" OR "mathematical model" OR 
simulation* OR "Deep learning" OR "Disease database" 
OR "Disease databases" OR "Docking software" OR "Drug 
database" OR "Drug databases" OR "in silico" OR "In vitro 
to in vivo extrapolation" OR "informatics" OR "I V I V E " OR 
"Machine learning" OR "artificial intelligence" OR 
"Molecular Docking" OR "Molecular Dynamics" OR "PBPK" 
OR "Pharmacokinetic" OR "Pharmacodynamic" OR 
"toxicokinetic" OR "toxicodynamic" OR "Pharmacology 
database" OR "Pharmacology databases" OR "Protein 
space" OR "Q SAR" OR "quantitative structure activity 
relationship" OR "Read-across" OR "Small molecule 
database" OR "Small molecule databases" OR "Structural 
database" OR "Structural databases" OR "structure activity 
relationship" OR "Digital Twins" ) 
4 In 
chemico 
models  
TITLE-ABS ( "In chemico" OR "Virtual tissue model" OR 
"Virtual tissue models" OR "Exposure model" OR 
"Exposure models" OR "Cell-free assays" OR "Cell-free 
assay" OR "Synthetic biochemistry" OR "Receptor binding" 
OR "Synthetic biology" OR "Ligand binding" OR 
"biochemical assay" ) 
119,284 
 Other 
limits 
Subject areas: Pharmacology, Toxicology and 
Pharmaceutics; Biochemistry, Genetics and Molecular 
Biology 22,365 and Multidisciplinary 2,740, Immunology and 
Microbiology 5,294 
 
PUBYEAR  >  2022  AND  PUBYEAR  <  2025   AND  ( 
LIMIT-TO ( LANGUAGE ,  "English" ) ) 
 
*Ran on October 23, 2023 using https://www.scopus.com/home.uri  

 
11 
 
Complement-ARIE 
Landscape Analysis 
Appendix D. Reference List 
Note: The reference list is provided separately for this project. (See third tab of Tableau 
dashboard “Reference List”: Complement-ARIE Landscape Analysis). 
 
 

 
12 
 
Complement-ARIE 
Landscape Analysis 
Appendix E. Keyword List 
Table 10. Keyword List 
Model Type Category Keyword 
0_in vitro 2D cell culture 2D 
0_in vitro 2D cell culture 2D cell culture 
0_in vitro 2D cell culture 2D in vitro cell culture 
0_in vitro 2D cell culture 2D traditional cell cultures 
0_in vitro 2D cell culture cell culture 
0_in vitro 2D cell culture cell cultures 
0_in vitro 2D cell culture cell line 
0_in vitro 2D cell culture cell lines 
0_in vitro 2D cell culture immortalized cell line 
0_in vitro 2D cell culture immortalized cell lines 
0_in vitro 3D cell culture 3D 
0_in vitro 3D cell culture 3D cell culture 
0_in vitro 3D cell culture 3D cell cultures 
0_in vitro 3D cell culture colonoid 
0_in vitro 3D cell culture embryo body 
0_in vitro 3D cell culture embryoid 
0_in vitro 3D cell culture organoid 
0_in vitro 3D cell culture Organoids 
0_in vitro 3D cell culture spheroid 
0_in vitro 3D cell culture Spheroids 
0_in vitro Bioprinting biofabrication 
0_in vitro Bioprinting bioink 
0_in vitro Bioprinting bioprint 
0_in vitro Bioprinting Bioprinting 
0_in vitro Bioprinting tissue engineering 
0_in vitro Bioprinting tissue scaffold 
0_in vitro Co-culture coculture 
0_in vitro Co-culture Co-culture 
0_in vitro Co-culture cocultures 
0_in vitro Co-culture co-cultures 
0_in vitro Donor-derived high throughput 
culture panels 
Donor Derived Cell Panels 
0_in vitro Donor-derived high throughput 
culture panels 
Donor derived high throughput 
cultures 
0_in vitro Donor-derived high throughput 
culture panels 
Donor derived panel 

 
13 
 
Complement-ARIE 
Landscape Analysis 
Model Type Category Keyword 
0_in vitro Donor-derived high throughput 
culture panels 
donor panel 
0_in vitro Donor-derived high throughput 
culture panels 
donor-derived 
0_in vitro Explant ex vivo 
0_in vitro Explant explant 
0_in vitro Explant explants 
0_in vitro Explant Tissue slice 
0_in vitro Microphysiological systems chip 
0_in vitro Microphysiological systems microfluidic 
0_in vitro Microphysiological systems microfluidics 
0_in vitro Microphysiological systems microphysiologic 
0_in vitro Microphysiological systems microphysiologic system 
0_in vitro Microphysiological systems microphysiologic systems 
0_in vitro Microphysiological systems Microphysiological 
0_in vitro Microphysiological systems Microphysiological system 
0_in vitro Microphysiological systems Microphysiological systems 
0_in vitro Microphysiological systems on a chip 
0_in vitro Microphysiological systems on chip 
0_in vitro Microphysiological systems organ chip 
0_in vitro Microphysiological systems organ on a chip 
0_in vitro Microphysiological systems tissue chip 
0_in vitro Microphysiological systems tissue on a chip 
0_in vitro stem cell adult stem cell 
0_in vitro stem cell adult stem cells 
0_in vitro stem cell differentiation 
0_in vitro stem cell embryonic stem cells 
0_in vitro stem cell h i p s c s  
0_in vitro stem cell human induced pluripotent stem 
cell 
0_in vitro stem cell human induced pluripotent stem 
cells 
0_in vitro stem cell human pluripotent stem cell 
0_in vitro stem cell human pluripotent stem cells 
0_in vitro stem cell induced pluripotent stem cell 
0_in vitro stem cell induced pluripotent stem cells 
0_in vitro stem cell i p s c 
0_in vitro stem cell i p s c s 
0_in vitro Stem Cell mixed culture 

 
14 
 
Complement-ARIE 
Landscape Analysis 
Model Type Category Keyword 
0_in vitro stem cell pluripotent 
0_in vitro stem cell Stem Cell 
0_in vitro stem cell Stem Cells 
1_In chemico Biochemical Assays biochemical 
1_In chemico Biochemical Assays biochemical assay 
1_In chemico Biochemical Assays Biochemical Assays 
1_In chemico Biochemical Assays enzyme 
1_In chemico Biochemical Assays G protein-coupled receptors 
1_In chemico Biochemical Assays G P C R 
1_In chemico Biochemical Assays Ion Channels 
1_In chemico Biochemical Assays lipid bilayer 
1_In chemico Cell-free assay area under curve 
1_In chemico Cell-free assay area under the curve 
1_In chemico Cell-free assay A U C  
1_In chemico Cell-free assay cell free 
1_In chemico Cell-free assay cell membrane 
1_In chemico Cell-free assay Cell-free assay 
1_In chemico Cell-free assay conformation 
1_In chemico Cell-free assay membrane protein 
1_In chemico Cell-free assay micelle 
1_In chemico Cell-free assay microsome 
1_In chemico Cell-free assay transport assay 
1_In chemico Ligand-receptor binding assay ligand binding 
1_In chemico Ligand-receptor binding assay ligand binding assay 
1_In chemico Ligand-receptor binding assay ligand binding assays 
1_In chemico Ligand-receptor binding assay Ligand receptor binding assay 
1_In chemico Ligand-receptor binding assay receptor binding 
1_In chemico Ligand-receptor binding assay receptor binding assay 
1_In chemico Ligand-receptor binding assay receptor binding assays 
1_In chemico structure/identity analysis chromatography 
1_In chemico structure/identity analysis CryoEM 
1_In chemico structure/identity analysis crystal structure 
1_In chemico structure/identity analysis Fourier transform infrared 
1_In chemico structure/identity analysis ft _ ir 
1_In chemico structure/identity analysis Gas Chromatography Mass 
Spectrometry 
1_In chemico structure/identity analysis GC MS 

 
15 
 
Complement-ARIE 
Landscape Analysis 
Model Type Category Keyword 
1_In chemico structure/identity analysis high performance liquid 
chromatography 
1_In chemico structure/identity analysis H P L C  
1_In chemico structure/identity analysis infrared spectroscopy 
1_In chemico structure/identity analysis LC MS 
1_In chemico structure/identity analysis Liquid Chromatography Mass 
Spectrometry 
1_In chemico structure/identity analysis Mass Spectrometry 
1_In chemico structure/identity analysis NMR 
1_In chemico structure/identity analysis NMR structure 
1_In chemico structure/identity analysis Nuclear magnetic resonance 
1_In chemico structure/identity analysis Raman 
1_In chemico structure/identity analysis Spectroscopies 
1_In chemico structure/identity analysis Spectroscopy 
1_In chemico structure/identity analysis S P R 
1_In chemico structure/identity analysis Surface Plasmon Resonance 
1_In chemico structure/identity analysis x ray crystallography 
1_In chemico structure/identity analysis X ray structure 
1_In chemico Synthetic organelles/cells synesthetic cell 
1_In chemico Synthetic organelles/cells synesthetic membranes 
1_In chemico Synthetic organelles/cells synthetic cell membrane 
1_In chemico Synthetic organelles/cells synthetic membrane 
1_In chemico Synthetic organelles/cells synthetic mitochondria 
1_In chemico Synthetic organelles/cells synthetic mitochondrias 
1_In chemico Synthetic organelles/cells synthetic nucleus 
1_In chemico Synthetic organelles/cells synthetic organelle 
1_In chemico Synthetic organelles/cells synthetic organelles / cells 
2_In silico AD ME Absorption 
2_In silico AD ME AD ME 
2_In silico AD ME Distribution 
2_In silico AD ME Excretion 
2_In silico AD ME kinetics 
2_In silico AD ME Metabolism 
2_In silico Artificial Intelligence/Machine 
Learning 
algorithm 
2_In silico Artificial Intelligence/Machine 
Learning 
artificial intelligence 
2_In silico Artificial Intelligence/Machine 
Learning 
computational 

 
16 
 
Complement-ARIE 
Landscape Analysis 
Model Type Category Keyword 
2_In silico Artificial Intelligence/Machine 
Learning 
deep learning 
2_In silico Artificial Intelligence/Machine 
Learning 
GAN  
2_In silico Artificial Intelligence/Machine 
Learning 
Generative adversarial networks 
2_In silico Artificial Intelligence/Machine 
Learning 
Generative AI  
2_In silico Artificial Intelligence/Machine 
Learning 
high performance computation 
2_In silico Artificial Intelligence/Machine 
Learning 
Large language model 
2_In silico Artificial Intelligence/Machine 
Learning 
LLM 
2_In silico Artificial Intelligence/Machine 
Learning 
machine learning 
2_In silico Artificial Intelligence/Machine 
Learning 
Neural networks 
2_In silico Bayesian Statistics advanced sampling 
2_In silico Bayesian Statistics Bayesian 
2_In silico Bayesian Statistics Bayesian Statistics 
2_In silico Bayesian Statistics metadynamics 
2_In silico Bayesian Statistics umbrella sampling 
2_In silico Bioinformatic processing bioinformatic 
2_In silico Bioinformatic processing Bioinformatic processing 
2_In silico Bioinformatic processing bioinformatics 
2_In silico Bioinformatic processing force field  
2_In silico Cheminformatics cheminformatic 
2_In silico Cheminformatics Cheminformatics 
2_In silico Cheminformatics chemogenomic 
2_In silico Cheminformatics Chemogenomics 
2_In silico Digital Twin Digital Twin 
2_In silico Molecular simulation binding affinity 
2_In silico Molecular simulation Coarse grained simulation 
2_In silico Molecular simulation free energy perturbation 
2_In silico Molecular simulation GROMACS 
2_In silico Molecular simulation molecular docking 
2_In silico Molecular simulation molecular dynamic simulations 
2_In silico Molecular simulation molecular dynamics 
2_In silico Molecular simulation Molecular simulation 

 
17 
 
Complement-ARIE 
Landscape Analysis 
Model Type Category Keyword 
2_In silico Molecular simulation N A M D 
2_In silico Molecular simulation optimized structure 
2_In silico Molecular simulation quantum mechanical calculation 
2_In silico Molecular simulation RMSD 
2_In silico Molecular simulation scalable molecular dynamics 
2_In silico Molecular simulation virtual screening 
2_In silico Molecular simulation visual molecular dynamics 
2_In silico Molecular simulation VMD 
2_In silico Pathways analysis Adverse Outcome Pathway 
2_In silico Pathways analysis A O P 
2_In silico Pathways analysis Connectivity Map 
2_In silico Pathways analysis Dynamic modeling 
2_In silico Pathways analysis I A T A 
2_In silico Pathways analysis integrated approaches to testing 
and assessment 
2_In silico Pathways analysis Kinetic modeling 
2_In silico Pathways analysis Pathways analysis 
2_In silico Pathways analysis Systems biology 
2_In silico Pharmacokinetic/Pharmacodynamic 
modeling 
In vitro to in vivo extrapolation 
2_In silico Pharmacokinetic/Pharmacodynamic 
modeling 
i v i v e  
2_In silico Pharmacokinetic/Pharmacodynamic 
modeling 
PB / PK 
2_In silico Pharmacokinetic/Pharmacodynamic 
modeling 
PBPK 
2_In silico Pharmacokinetic/Pharmacodynamic 
modeling 
PBPK model 
2_In silico Pharmacokinetic/Pharmacodynamic 
modeling 
pharmacodynamic 
2_In silico Pharmacokinetic/Pharmacodynamic 
modeling 
pharmacokinetic 
2_In silico Pharmacokinetic/Pharmacodynamic 
modeling 
physiologically based 
2_In silico Q SAR Chemical structure 
2_In silico Q SAR Q SAR 
2_In silico Q SAR quantitative structure activity 
relationship 
2_In silico Q SAR structure activity relationship 
2_In silico Read Across Read Across 

 
18 
 
Complement-ARIE 
Landscape Analysis 
Model Type Category Keyword 
3_General 
Methods 
Biochemical Assays Förster resonance energy transfer 
3_General 
Methods 
Biochemical Assays FRET 
3_General 
Methods 
CRISPR Clustered Regularly Interspaced 
Short Palindromic Repeats 
3_General 
Methods 
CRISPR CRISPR 
3_General 
Methods 
Droplet-based assays droplet based assay 
3_General 
Methods 
Droplet-based assays Droplet based assays 
3_General 
Methods 
Epigenomics epigenome 
3_General 
Methods 
Epigenomics epigenomic 
3_General 
Methods 
Epigenomics epigenomics 
3_General 
Methods 
High-throughput screening cell painting 
3_General 
Methods 
High-throughput screening High throughput screening 
3_General 
Methods 
High-throughput screening multi omics 
3_General 
Methods 
High-throughput screening omics 
3_General 
Methods 
Imaging image based 
3_General 
Methods 
Imaging imaging 
3_General 
Methods 
Imaging Live cell imaging 
3_General 
Methods 
Metabolomics metabolome 
3_General 
Methods 
Metabolomics metabolomic 
3_General 
Methods 
Metabolomics Metabolomics 
3_General 
Methods 
Microbiome microbiome 
3_General 
Methods 
Proteomics proteome 

 
19 
 
Complement-ARIE 
Landscape Analysis 
Model Type Category Keyword 
3_General 
Methods 
Proteomics proteomic 
3_General 
Methods 
Proteomics Proteomics 
3_General 
Methods 
Sequencing Technology DNA Seq 
3_General 
Methods 
Sequencing Technology genomic 
3_General 
Methods 
Sequencing Technology genomics 
3_General 
Methods 
Sequencing Technology miRNA Seq 
3_General 
Methods 
Sequencing Technology Next Generation Sequencing 
3_General 
Methods 
Sequencing Technology NGS 
3_General 
Methods 
Sequencing Technology oxford nanopore 
3_General 
Methods 
Sequencing Technology RNA Seq 
3_General 
Methods 
Sequencing Technology second generation sequencing 
3_General 
Methods 
Sequencing Technology Sequencing Technology 
3_General 
Methods 
Sequencing Technology third generation sequencing 
3_General 
Methods 
Single Cell Assays single cell assay 
3_General 
Methods 
Single Cell Assays Single Cell Assays 
3_General 
Methods 
Single Cell Assays single cell imaging 
3_General 
Methods 
Single Cell Assays single cell sequencing 
3_General 
Methods 
Single Cell Assays single cell sorting 
3_General 
Methods 
Transcriptomics transcriptome 
3_General 
Methods 
Transcriptomics transcriptomic 
3_General 
Methods 
Transcriptomics Transcriptomics 

 
20 
 
Complement-ARIE 
Landscape Analysis 
Appendix F. Prompts Used in Generative AI Approach 
Generative AI Summary Questions 
The following is text from an article: <json here> 
Please act as a biomedical researcher exploring alternatives to animal testing. Wrap 
each response in an XML tag based on the prefix 'response' concatenated with the 
question number. Replace '&' characters with '&amp;' in your responses. Replace '<' 
characters with '&lt;' in your responses. Replace '>' characters with '&gt;' in your 
responses. 
1. What is the title of this paper? 
1. Give a brief response to the question 'What are the details on the funding of this 
research, including any grants or sponsors?'. Justify your answer with direct 
quotes. If you can't tell, say 'I don't know' 
2. Give a brief response to the question 'Provide details on the method described.'. 
Justify your answer with direct quotes. If you can't tell, say 'I don't know' 
3. Give a brief response to the question 'Is the method novel (new technology) or is 
it an improvement on an existing approach (refinement)?'. Justify your answer 
with direct quotes. If you can't tell, say 'I don't know' 
4. Give a brief response to the question 'What were the main technical challenges 
described in the paper that this method was trying to overcome?'. Justify your 
answer with direct quotes. If you can't tell, say 'I don't know' 
5. Give a brief response to the question 'Did the authors discuss the method in 
terms of a regulatory use? If so, what did the authors say?'. Justify your answer 
with direct quotes. If you can't tell, say 'I don't know' 
6. Give a brief response to the question 'Did the authors discuss ethical 
considerations? If so, what did they say?'. Justify your answer with direct quotes. 
If you can't tell, say 'I don't know' 
7. Give a brief response to the question 'Did the authors discuss workforce 
considerations? If so, what did they say?'. Justify your answer with direct quotes. 
If you can't tell, say 'I don't know' 
8. Give a brief response to the question 'Did the authors discuss economic 
considerations? If so, what did they say?'. Justify your answer with direct quotes. 
If you can't tell, say 'I don't know' 
9. Give a brief response to the question 'Did the authors incorporate considerations 
of population diversity or interindividual variability into the technology? If so, 
how?'. Justify your answer with direct quotes. If you can't tell, say 'I don't know' 
10. Give a brief response to the question 'Did this paper model outcomes in a 
specific population? If so, what population?'. Justify your answer with direct 
quotes. If you can't tell, say 'I don't know' 

 
21 
 
Complement-ARIE 
Landscape Analysis 
11. Give a brief response to the question 'What tissue types does this paper 
examine?'. Justify your answer with direct quotes. If you can't tell, say 'I don't 
know' 
12. Give a brief response to the question 'What cell types does this paper examine?'. 
Justify your answer with direct quotes. If you can't tell, say 'I don't know' 
13. Give a brief response to the question 'What elements of human physiology does 
this paper consider?'. Justify your answer with direct quotes. If you can't tell, say 
'I don't know' 
14. Give a brief response to the question 'Is a disease examined in this paper? If so 
what disease?'. Justify your answer with direct quotes. If you can't tell, say 'I don't 
know' 
15. Give a brief response to the question 'Are cellular endpoints being measured in 
this paper? If so, what are the endpoints?'. Justify your answer with direct quotes. 
If you can't tell, say 'I don't know' 
16. Give a brief response to the question 'Did this model seek to address metabolic 
capacity of the tissue? If so, in what way?'. Justify your answer with direct 
quotes. If you can't tell, say 'I don't know' 
17. Give a brief response to the question 'Did the authors describe the validation 
methods, such as the use of controls, taken for this method? If so, what are 
they?'. Justify your answer with direct quotes. If you can't tell, say 'I don't know' 
18. Give a brief response to the question 'What are the limitations of the method as 
described in this paper?'. Justify your answer with direct quotes. If you can't tell, 
say 'I don't know' 
19. Give a brief response to the question 'What challenges remain even after the 
development of this method?'. Justify your answer with direct quotes. If you can't 
tell, say 'I don't know' 
 
Entity Extraction Questions 
For cell types: In th e attached CSV extract the cell type entities or cell type(s) in the 
"cell.type" column and produce a tab delimited output with the extracted values 
separated by commas in a column adjacent to the "cite" column. Please do not output 
any other columns from the original file. Additionally, please iterate through every row in 
the CSV so each row has an output. 
For tissue types: In the at tached CSV extract the tissue entities or tissue type(s) in the 
"tissue" column and produce a tab delimited output with the extracted values separated 
by commas in a column adjacent to the "cite" column. Please do not output any other 
columns from the original file. Additionally, please iterate through every row in the CSV 
so each row has an output. 
For diseases: In the at tached CSV extract the disease entities or disease(s) in the 
"disease" column and produce a tab delimited output with the extracted values 

 
22 
 
Complement-ARIE 
Landscape Analysis 
separated by commas in a column adjacent to the "cite" column. Please do not output 
any other columns from the original file. Additionally, please iterate through every row in 
the CSV so each row has an output. 
For cell endpoints: In the a ttached CSV extract the cell endpoint entities or cell 
endpoints in the "cellular.endpoints" column and produce a tab delimited output with the 
extracted values separated by commas in a column adjacent to the "cite" column. 
Please do not output any other columns from the original file. Additionally, please iterate 
through every row in the CSV so each row has an output 
For funding statement: In the at tached CSV map the "funding_statement" column to the 
funding organizations affiliate country, if it is a private organization or company then 
map to "private", if the row contains "no", or "NO_RESPONSE" then respond "none", 
and produce a tab delimited output with the extracted values separated by commas in a 
column called "country_org" contained in quotes adjacent to the "cite" column. Please 
do not output any other columns from the original file. Additionally, please iterate 
through every row in the CSV so each row has an output.   
 

 
23 
 
Complement-ARIE 
Landscape Analysis 
Appendix G. Biomedical database with FAIR score per question 
FAIR evaluation of 28 biomedical databases2. A score of 1 (yellow) indicates that the 
evaluator was able to explicitly identify the information pertaining to each question and a 
score of 0 (navy) indicates that the information could not be found. Scores were added 
for each question and database. Databases with the highest FAIR score are shaded. 
FAIR questions are listed in Appendix H. 
 
2 N H C D R : NINDS Human Cell and Data Repository; BioSystics-AP:  BioSystics Analytics Platform; CCDI MTP: Molecular Targets 
Platform; CMAP: Connectivity Map;  IDC: Imaging Data Commons; TCGA: The Cancer Genome Atlas; N DEx: The Network 
Dat
a Exchange; Hu
BMAP: The Human BioMolecular Atlas Program; IDC: Imaging Data Commons; BioGRID: Biological 
Gen
eral
 Repository for Interaction Datasets; CDS: Cancer Data Service; DABI: Data Archive for the BRAIN Initiative; GDC: 
Genomic Data Commons; GEA: Genomic Expression Archive; G TEx: Genotype-Tissue Expression; G WAS: Genome-wide 
Association Studies Catalog; G WAS Central; LINCS: Library of Integrated Network-Based Cellular Signatures; NCBI dbVar: 
Structural Variation Database; NHGRI-EBI G WAS Catalog; The NHGRI Genomic AnVIL: Data Science Analysis, Visualization, 
and Informatics Lab-space; PDC: Proteomic Data Commons; PRIDE: Proteomics Identifications Database; NIH GTR: 
Genetic Testing Registry 
Database
Q1 Q2 Q3 Q4 Q5 Q6 Q7 Q8 Q9 Q10 Q11 Q12 Q13 Q14 Q15 Q16 Q17 Q18 Q19 Q20 Q21 Q22 Q23 Q24 Q25 Q26 Q27 Q28 Q29
Database 
FAIR score
HCMI Searchable 
Catalog 17
NHCDR 15
BioSystics-AP 19
CCDI MTP 24
CMAP 16
TCGA 14
NDEx 22
HuBMAP 29
IDC 21
Metabolomics 
Workbench 20
BioImage Archive 20
BioGRID 15
CDS 19
DABI 12
GDC 18
GEA 17
GTEx 21
GWAS Catalog 25
GWAS Central 16
LINCS 27
NCBI dbVar 21
NHGRI-EBI GWAS 
Catalog 16
NHGRI Genomic AnVIL 7
PDC 17
PRIDE Database 20
NCATS OpenData 
Portal 8
NIH GTR 25
Uniprot 19
FAIR question score 24 19 20 4 25 19 16 20 19 27 27 12 20 16 27 23 27 18 24 15 7 8 15 8 11 21 15 11 22
Interoperable Reusable
in vitroin silicoNot categorize General Methods: HTS, omics approaches, imaging
Findable Accessible

 
24 
 
Complement-ARIE 
Landscape Analysis 
Appendix H. FAIR rubric questions 
Findable 
Q1: 
 
Is a unique, persistent, viewable identifier assigned for the data release and 
documented in the data release's metadata record?  
Q2: Is a separate identifier assigned for the data release's metadata record? 
Q3: Is the assigned separate identifier unique and persistent? 
Q4: Are the authors/originators' ORCID identifiers provided in the data release's landing page and data release metadata? 
Q5: Is a description included in the data release's metadata? 
Q6: Is the author/originator included in the data release's metadata? 
Q7: Is a data point of contact included in the data release's metadata? 
Q8: Is the data publication date included in the data release's metadata? 
Q9: If applicable, is the data type, data version and revision dates included in the data release's metadata? 
Accessible 
Q10
: 
 
Does the data release have a human readable landing page that provides direct 
access to the data? 
Q11
: Is this landing page publicly accessible? 
Q12
: Is the data release's author/originator information available on the landing page? 
Q13
: Does the data release's identifier take users to the human readable landing page? 
Q14
: 
Is the data distributor, and its contact information, included with the data release's 
landing page? 
Q15
: 
Can users obtain the data release's data and metadata files by manual actions 
(human)? 
Q16
: 
Can users obtain the data release's data files and metadata files by automated 
actions? 
Interoperable Q17
: 
 
Are all data files available in an open format that is commonly used by the relevant 
research community?  
Q18
: 
Are all data files available in multiple formats, including those that are machine 
readable? 
Q19
: Does the data release's metadata contain unique names/labels? 

 
25 
 
Complement-ARIE 
Landscape Analysis 
Q20
: 
Does the data release and metadata contain at least one name/label using a 
citable and publicly available source including community-recognized ontologies 
used in Resource Description Format (RDF)/linked data?  
Q21
: Is information about precision/accuracy documented in the metadata? 
Q22
: Is information about data value consistency documented in the metadata? 
Q23
: 
Is the relationship between the data and related data releases documented in the 
metadata? 
Reusable 
Q24
: 
 
Are recommended reuses included in the data release's metadata or landing page 
along with any reuse limits? 
Q25
: 
If input datasets are used, are the citations to the input datasets included with the 
data release's metadata?  
Q26
: Is the process/methodology summary included with the data release's metadata?  
Q27
: Is data quality information included with the data release's metadata?  
Q28
: 
Are citation(s) used to describe the process/methodology including the data quality 
information included with the data release's metadata?  
Q29
: Are related resources documented in the data release's metadata?  

 
26 
 
 
 
 
 
Complement-ARIE 
Landscape Analysis 
Supplemental Materials  
The following figures represent the distribution of biomedical NAM categories, keywords 
and answers to questions applied to generative AI.  
Counts represent the number of publications that included the keyword or generative AI 
f
ound information relevant to each question. Note that scales are different per figure. 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 

 
27 
 
 
 
 
 
Complement-ARIE 
Landscape Analysis 
 
In vitro biomedi
cal NAMs: 
 
Figure S1: Li
terature distribution of in vitro biomedical NAMs per keyword.  
In vitro:
literature distribution
0
100
200
300
400
500
700
600Publication counts

 
28 
 
Complement-ARIE 
Landscape Analysis 
 
Figure S2: Number of publications (x-axis) per question across in vitro 
categories. Information on publication count can be viewed in Table S1. 
In vitro
0 500 1000 1500 2000 2500
Workforce Considerations Discussed
Tissue Types Examined
Research Funding Details
Remaining Challenges after Method
Development
Population Modeled
Population Diversity and Variability
Incorporated
Model Metabolic Capacity Addressed
Method: New Technology or Refinement
of Existing Approach
Method Validation Methods Described
Method Technical Challenges Described
Method Regulatory Use Discussed
Method Limitations
Method Details Described
Human Physiology Elements Considered
Ethical Considerations Discussed
Economic Considerations Discussed
Cell Types Examined
2D cell culture
Cellular Endpoints Measured
3D cell culture
Disease(s) Examined
Bioprinting
Co-culture
Explant
Microphysiological
systems
Stem cell

 
29 
 
Complement-ARIE 
Landscape Analysis 
 
Tabl
e S1: Publication count per in vitro category for each question area applied to Generative AI. 
 
2D cell 
culture 
3D cell 
culture Bioprinting 
Co-
culture Explant 
Microphysiological 
systems 
Stem 
cell 
Workforce Considerations Discussed 1 3 1 0 0 0 3 
Tissue Types Examined 393 478 168 71 77 274 583 
Research Funding Details 232 288 84 48 36 166 337 
Remaining Challenges after Method 
Development 332 432 144 56 71 259 500 
Population Modeled 88 125 31 24 29 47 187 
Population Diversity and Variability 
Incorporated 7 5 1 0 2 4 14 
Model Metabolic Capacity Addressed 94 101 25 11 17 72 111 
Method: New Technology or 
Refinement of Existing Approach 390 479 157 72 73 309 535 
Method Validation Methods 
Described 308 354 92 63 56 172 412 
Method Technical Challenges 
Described 402 494 163 70 74 316 540 
Method Regulatory Use Discussed 13 9 1 2 2 11 7 
Method Limitations 248 354 98 46 56 194 363 
Method Details Described 413 514 170 72 76 318 581 
Human Physiology Elements 
Considered 336 424 145 65 68 223 516 
Ethical Considerations Discussed 29 29 12 5 9 16 47 
Economic Considerations Discussed 30 29 16 2 8 40 28 
Disease(s) Examined 240 296 85 47 55 166 340 
Cellular Endpoints Measured 351 406 127 69 66 238 499 
Cell Types Examined 395 468 163 71 74 278 582 
 

 
30 
 
 
 
 
 
 
 
Complement-ARIE 
Landscape Analysis 
In chemico biomedical NAMs: 
Figure S3: Literature distribution of in chemico biomedical NAMs per keyword.  
 
 
 
In chemico:
literature distribution
350
300
250s ount c
200on i at c
150i ubl P
0
50
100
Biochemical Assays Cell-free assay Ligand-receptor
binding assay
structure/identity
analysis

31 
Complement-ARIE 
Landscape Analysis 
Figure S4: Number of publications (x-axis) per question across in chemico 
categories. Information on publication count can be viewed in Table S2. 
In chemico
0 200 400 600 800
Workforce Considerations Discussed
Tissue Types Examined
Research Funding Details
Remaining Challenges after Method
Development
Population Modeled
Population Diversity and Variability
Incorporated
Model Metabolic Capacity Addressed
Method: New Technology or Refinement of
Existing Approach
Method Validation Methods Described
Method Technical Challenges Described
Method Regulatory Use Discussed
Method Limitations
Method Details Described
Human Physiology Elements Considered
Ethical Considerations Discussed
Economic Considerations Discussed
Disease(s) Examined
Cellular Endpoints Measured
Cell Types Examined Biochemical assays
Cell-free assays
Ligand-receptor
binding assays
Structure/identity
analysis

 
32 
 
Complement-ARIE 
Landscape Analysis 
 
Table 
S2: Publication count per in chemico category for each question area applied to Generative AI. 
 
 
Biochemical 
assays 
Cell-free 
assays 
Ligand-receptor 
binding assays 
Structure/identity 
analysis 
Workforce Considerations Discussed 1 0 0 0 
Tissue Types Examined 210 73 42 218 
Research Funding Details 136 42 35 134 
Remaining Challenges after Method 
Development 210 82 51 182 
Population Modeled 26 17 4 37 
Population Diversity and Variability 
Incorporated 1 0 0 0 
Model Metabolic Capacity Addressed 32 6 2 34 
Method: New Technology or Refinement of 
Existing Approach 251 81 70 260 
Method Validation Methods Described 151 56 41 172 
Method Technical Challenges Described 256 98 71 255 
Method Regulatory Use Discussed 5 1 2 6 
Method Limitations 136 51 32 127 
Method Details Described 285 104 77 274 
Human Physiology Elements Considered 191 66 42 151 
Ethical Considerations Discussed 5 2 1 1 
Economic Considerations Discussed 13 3 2 7 
Disease(s) Examined 153 59 31 132 
Cellular Endpoints Measured 124 38 24 103 
Cell Types Examined 186 63 40 168 
 

 
33 
 
 
 
 
 
Complement-ARIE 
Landscape Analysis 
In silico biomedical NAMs: 
Figure S5: Literature distribution of in silico biomedical NAMs per keyword.  
 
In silico:
literatute distributions 
0
100
200
300
400
500
600
700
800Publication count

 
34 
 
Complement-ARIE 
Landscape Analysis 
Figure S6: Number of publications (x-axis) per question across in silico 
categories. Information on publication count can be viewed in Table S3. 
 
 
 
In silico
0 500 1000 1500
Workforce Considerations Discussed
Tissue Types Examined
Research Funding Details
Remaining Challenges after Method Development
Population Modeled
Population Diversity and Variability Incorporated
Model Metabolic Capacity Addressed
Method: New Technology or Refinement of Existing
Approach
Method Validation Methods Described
Method Technical Challenges Described
Method Regulatory Use Discussed
Method Limitations
Method Details Described
Human Physiology Elements Considered
Ethical Considerations Discussed
Economic Considerations Discussed
Disease(s) Examined
Cellular Endpoints Measured
Cell Types Examined
Machine learning and
artificial intelligence
ADME
QSAR
Read across
Pharmacokinetic/pharm
acodynamic
Pathway analysis

 
35 
 
Complement-ARIE 
Landscape Analysis 
Table S3: Publication count per in silico category for each question area applied to Generative AI. 
 
 
Machine learning 
and artificial 
intelligence AD ME Q SAR 
Read 
across 
Pharmacokinetic/ 
pharmacodynamic 
Pathway 
analysis 
Workforce Considerations 
Discussed 5 0 1 0 0 0 
Tissue Types Examined 424 227 66 4 72 43 
Research Funding Details 305 125 43 3 35 24 
Remaining Challenges after 
Method Development 540 222 78 7 76 39 
Population Modeled 108 45 15 1 16 17 
Population Diversity and 
Variability Incorporated 12 5 1 1 7 3 
Model Metabolic Capacity 
Addressed 56 94 7 1 16 13 
Method: New Technology or 
Refinement of Existing 
Approach 616 231 89 8 78 42 
Method Validation Methods 
Described 236 147 41 2 36 15 
Method Technical Challenges 
Described 646 236 95 8 80 47 
Method Regulatory Use 
Discussed 20 10 5 5 9 10 
Method Limitations 359 147 47 5 50 27 
Method Details Described 692 272 114 8 96 50 
Human Physiology Elements 
Considered 360 218 63 2 69 37 
Ethical Considerations 
Discussed 20 12 1 1 2 4 

 
36 
 
 
Complement-ARIE 
Landscape Analysis 
Economic Considerations 
Discussed 46 13 5 1 10 4 
Disease(s) Examined 396 151 78 1 53 33 
Cellular Endpoints Measured 188 143 28 3 27 32 
Cell Types Examined 396 203 55 1 50 36 
 

 
37 
 
Complement-ARIE 
Landscape Analysis 
General Methods biomedical NAMs:  
 
Figure S7: Literature distribution of General Methods biomedical NAMs per 
keyw
ord.  
 
 
 
 
 
General Methods:
literature distribution
0
50
100
150
200
250
300Publication counts

Complement ARIE 
Landscape Analysis 
Figure S8: Number of publications (x-axis) per question across General Methods 
categories. Information on publication count can be viewed in Table S4. 
General Methods 
Cell Types Examined 
Cellular Endpoints Measured 
Disease(s) Examined 
Economic Considerations Discussed 
Ethical Considerations Discussed 
Human Physiology Elements Considered 
Method Details Described 
Method Limitations 
Method Regulatory Use Discussed 
Method Technical Challenges Described 
Method Validation Methods Described 
Method: New Technology or Refinement of Existing 
Approach 
Model Metabolic Capacity Addressed 
Population Diversity and Variability Incorporated 
Population Modeled 
Remaining Challenges after Method Development 
Research Funding Details 
Tissue Types Examined 
Workforce Considerations Discussed 
  
 
 
 
Biochemical assays 
CRISPER 
Epigenomics 
High throughput 
screening
Imaging 
Metabolomics 
Microbiome 
Proteomics 
Sequencing 
technology
Single cell assays 
Transcriptomics 
0 500 1000 1500 
 
 
 
 
 
 
   
 
-
38 

 
39 
 
Complement-ARIE 
Landscape Analysis 
Table S4: Publication count per General Method category for each question area applied to Generative  
 
Biochemical 
assays CRISPER Epigenomics HTS Imaging Metabolomics Microbiome Proteomics 
Sequencing 
technology 
Single 
cell 
assays Transcriptomics 
Workforce 
Considerations 
Discussed 0 1 0 1 1 0 0 0 0 0 0 
Tissue Types 
Examined 7 42 20 220 151 71 22 136 141 15 137 
Research Funding 
Details 7 13 7 136 90 34 12 77 71 8 70 
Remaining Challenges 
after Method 
Development 5 42 22 214 137 69 20 132 147 14 125 
Population Modeled 0 19 10 65 42 35 7 47 53 3 51 
Population Diversity 
and Variability 
Incorporated 0 2 3 10 2 4 1 6 10 0 2 
Model Metabolic 
Capacity Addressed 0 5 5 44 21 36 3 18 22 0 28 
Method: New 
Technology or 
Refinement of Existing 
Approach 8 45 20 234 149 75 16 147 164 13 129 
Method Validation 
Methods Described 0 29 4 115 94 28 6 72 0 6 65 
Method Technical 
Challenges Described 9 48 22 245 151 81 19 147 172 13 133 
Method Regulatory 
Use Discussed 0 1 0 12 4 1 0 0 5 0 3 
Method Limitations 2 38 14 155 110 50 14 86 96 10 19 

 
40 
 
Complement-ARIE 
Landscape Analysis 
 
Method Details 
Described 9 48 21 258 158 86 23 157 181 14 144 
Human Physiology 
Elements Considered 4 36 16 178 113 65 20 100 114 10 105 
Ethical Considerations 
Discussed 0 1 1 9 7 1 0 4 10 1 5 
Economic 
Considerations 
Discussed 0 3 0 16 11 2 1 4 13 0 5 
Disease(s) Examined 0 40 18 166 106 56 15 94 117 12 92 
Cellular Endpoints 
Measured 7 33 12 143 108 40 7 70 0 8 84 
Cell Types Examined 0 41 17 191 131 52 10 114 128 15 134 

 
H-1 
 
Complement-ARIE 
Landscape Analysis 
 