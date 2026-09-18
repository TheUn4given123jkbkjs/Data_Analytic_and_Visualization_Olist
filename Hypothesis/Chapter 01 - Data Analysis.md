Data Analysis and Visualization 

**Introduction to Data Analysis** 

_Prepared by: Tran Luong Quoc Dai, Ph.D._ 

# Outline 

- Introduction to Data 

- Data analysis vs. Data analytics 

- Process of data analytics 

- Introduction to Data analysis 

- Statistical science in Data analysis 

- Collecting data 

<mark>Jan 1st, 2025</mark> 

<mark>2</mark> 

# What is the data? 

- Data is a collection of facts, numbers, words, observations, or other useful information. 

- Through processing and analysis, organizations **transform raw data into valuable insights** for better decision-making and outcomes. 

- **Sources and Formats:** 

   - **Non-numerical qualitative data:** descriptive data such as customer reviews and open-ended survey responses. 

   - **Numerical qualitative data:** measurable data like sales figures, statistical measurements, or performance metrics. 

   - **Public data:** Freely available datasets, such as government statistics and census records. 

   - **Private data:** Proprietary information, such as customer purchase histories, healthcare records, and internal financial data. 

<mark>Jan 1st, 2025</mark> 

<mark>3</mark> 

# The Importance of Data 

## • **Digital Transformation:** 

   - Big data, sourced from social media, e-commerce, and financial transactions, is revolutionizing industries. 

   - Nicknamed “ **The New Oil** ” due to its unparalleled value in driving growth and innovation. 

- **Role in AI:** 

   - Data is the foundation for training AI and machine learning models, enhancing their accuracy and effectiveness. 

   - High-quality, diverse datasets are critical for refining predictive algorithms and enabling AI applications. 

- **Data Management:** 

   - Ensures data is well-organized, accessible, and ready for analysis. 

   - Addresses growing concerns about security, privacy, and compliance with regulations such as General Data Protection Regulation (GDPR). 

<mark>Jan 1st, 2025</mark> 

<mark>4</mark> 

# Types of Data 

- **Quantitative Data:** 

   - Defined by measurable, numerical values. 

   - Examples: Revenue figures, temperature readings, inventory counts. 

   - **Use Cases:** Statistical analysis, trend forecasting, budgeting, and performance tracking. 

- **Qualitative Data:** 

   - Descriptive, capturing characteristics or experiences beyond numerical measures. 

   - Examples: Customer feedback, social media comments, product reviews. 

   - **Use Cases:** Understanding user behavior, market trends, and customer experiences. 

- **Structured Data:** 

   - Highly organized, fitting into rows and columns in databases or spreadsheets. 

   - Examples: Customer records, financial reports, product inventories. 

   - **Use Cases:** Business intelligence, operational reporting, data querying. 

- **Unstructured Data:** 

   - It lacks a predefined format and often requires advanced tools for analysis. 

   - Examples: Emails, videos, social media posts, audio recordings. 

   - **Use Cases:** Sentiment analysis, complex pattern recognition, multimedia indexing. 

<mark>Jan 1st, 2025</mark> 

<mark>5</mark> 

# Advanced Types of Data 

## • **Semi-structured Data:** 

   - Combines structured and unstructured elements, often tagged for easier organization. 

   - Examples: XML files, JSON objects, and log files. 

   - **Use Cases:** Web scraping, API integrations, flexible data storage solutions. 

- **Metadata:** 

   - Data that describes other data, providing context and organization. 

   - Examples: File names, authorship, creation dates, and file sizes. 

   - **Use Cases:** Enhancing searchability, improving data management, and facilitating digital library organization. 

- **Big Data:** 

   - It encompasses massive datasets that are complex, high-volume and varied in type. 

   - Examples: E-commerce transactions, IoT sensor data, and social media activity. 

   - **Use Cases:** Customer behavior analytics, predictive maintenance, fraud detection, personalized marketing. 

<mark>Jan 1st, 2025</mark> 

<mark>6</mark> 

# Outline 

- Introduction to Data 

- Data analysis vs. Data analytics 

- Process of data analytics 

- Introduction to Data analysis 

- Statistical science in Data analysis 

- Collecting data 

<mark>Jan 1st, 2025</mark> 

<mark>7</mark> 

# Analysis vs. Analytics 

- According to the _Merriam-Webster_ dictionary: 

   - Analysis is separation of a whole into its component parts. 

   - Analytics is the method/science of logical analysis. 

- In simpler terms: 

**Analysis Analytics** 

Analysis focuses on the past, examining facts and Analytics uses this processed data to create models figures to understand what has already happened. that predict future outcomes or trends. Analysis involves reorganizing existing data to extract Analytics uses this analyzed information to predict the analyzed information. what may happen. 

<mark>Jan 1st, 2025</mark> 

<mark>8</mark> 

# Data analysis vs. Data analytics 

- Data analysis involves examining a given dataset in detail by dividing it into smaller parts, studying each part individually, and exploring how they relate to one another. Data analytics contains a wide variety of activities and concepts related to data. 



<!-- Start of picture text -->
ebg Data Preparation Data Visualization<br>Lee (O) oe<br>= HalitS =<br>pot<br>Data Collection Data Analysis =<br><!-- End of picture text -->

- In short, data analysis is a specific method or process, while data analytics is the overall discipline that includes various processes and tools for managing and interpreting data. 

- Data analysis is an essential part of the data analytics process. 

- Data analysis involves examining past data in detail, using statistical methods to derive meaningful insights and conclusions. Data analytics uses various variables to create predictive models. 

~~ee~~ <mark>Jan 1st, 2025 9</mark> 

# Example 1: Trader 

- Most of us have a basic understanding of the stock market. Now, imagine you’re a beginner who wants to start trading profitably. Here’s a suggested initial action plan. 

   - As a new trader, you should research stock trends and market data to capture current conditions. This approach involves data analysis. 

   - With your understanding of market patterns, you can make informed predictions about future stock prices and decide which shares to buy. This illustrates how data analytics plays a crucial role in stock trading. 

<mark>Jan 1st, 2025</mark> 

<mark>10</mark> 

# Example 2: Bookstore 

- Data analysis: The bookstore owner reviews last year’s sales data to identify profit and sales trends across different seasons, months, and weeks. This process focuses on understanding past performance and aims to answer the question “What happened?” 

- Data analytics: By leveraging insights from historical data, analytics uses logical reasoning to forecast future sales patterns. This approach helps the bookstore plan inventory and promotions to meet anticipated demand for specific genres or titles in the coming months. 

<mark>Jan 1st, 2025</mark> 

<mark>11</mark> 

# Outline 

- Introduction to Data 

- Data analysis vs. Data analytics 

- Process of data analytics 

- Introduction to Data analysis 

- Statistical science in Data analysis 

- Collecting data 

<mark>Jan 1st, 2025</mark> 

<mark>12</mark> 

# Process of Data analytics 



<!-- Start of picture text -->
Define your<br>problem<br>Externalsets? data SQLDatastatementspipeline exO°<br>5 Collect the A foe) ak<br>data to}<br>06Po<br>B. Bc<br>Delete, impute,<br>nyclean values cea the —sEDA<br>data<br>data analysis<br>> 7A Tene < bh<br>Report your<br>°<br>on findings<br>= rudderstack CEA<br><!-- End of picture text -->

<mark>———eeeeeeee—CSC“‘=E Jan 1st, 2025 13</mark> ~~OO~~ 

# Step 1: Define your problem 

- **Purpose:** Specify the questions to answer and the key performance indicators (KPIs) to measure success. 

- **Understand Expectations:** 

   - Clarify stakeholders’ expectations for the solution. What do they want to achieve? 

   - Align on goals—descriptive analysis, actionable steps, or specific outputs (e.g., reports or metrics). 

- **Ask the Right Questions:** Reframe broad questions into actionable, data-driven queries (e.g., “What percentage of users use feature X?”). 

- **Focus on Specific Outcomes:** Determine if the goal is to provide descriptive insights, actionable recommendations, or a specific deliverable like a report or key metric. 

- **Key questions:** 

   - What problems are my stakeholders mentioning? 

   - What are their expectations for the solutions? 

<mark>Jan 1st, 2025</mark> 

<mark>14</mark> 

# Step 2: Collect the data 

- **Purpose:** Gather and store data from various sources for analysis, often with assistance from a data engineer. 

- **Types of Data Sources:** 

   - Internal Data: From within the organization (e.g., sales reports). 

   - External Data: From outside the organization, including: 

      - § First-party data: Collected directly by the organization. 

      - § Second-party data: Purchased from another organization. 

      - § Third-party data: Acquired from aggregators or external sources. 

- **Common Collection Methods:** Interviews, surveys, feedback, and questionnaires. 

- **Data Storage Tools:** 

   - Spreadsheets: For smaller datasets (e.g., MS Excel, Google Sheets). 

   - Databases: For larger datasets (e.g., SQL databases like Oracle or Microsoft SQL Server). 

- **Key Considerations:** Based on the scope and requirements of the analysis, identify the best data sources and storage solutions. 

<mark>Jan 1st, 2025</mark> 

<mark>15</mark> 

# Step 3: Clean the data 

- **Purpose:** Prepare data for analysis by cleaning, processing, and performing exploratory data analysis (EDA). 

- **Exploratory Data Analysis (EDA):** is an approach/philosophy for data analysis that employs a variety of techniques (mostly graphical) to uncover underlying structure, extract important variables, maximize insight into a data set, detect outliers and anomalies, ... (refer to [3] for more details). 

- **Data Cleaning:** 

   - Remove duplicates, irrelevant data, or misspellings. 

   - Impute missing or faulty values with reasonable substitutes. 

   - Ensure data integrity and document all changes for transparency and reproducibility. 

- **Addressing Bias:** Check for and eliminate biases in the data to ensure balanced representation. 

- **Post-Cleaning Validation:** Perform another round of EDA to confirm that the cleaned data follows expected distributions. 

- **Tools:** Use functions in SQL and Excel to clean and format the data. 

- **Importance:** Clean, unbiased, well-documented data ensures accurate analysis, helps identify trends, and provides meaningful insights. 

<mark>Jan 1st, 2025</mark> 

<mark>16</mark> 

# Step 4: Perform data analysis 

- **Purpose:** Use cleaned data to uncover trends, perform calculations, and identify insights. 

- **Analysis Techniques:** 

   - Basic methods: Funnel analysis, pivot tables (Excel), and SQL queries. 

   - Advanced methods: Statistical models and machine learning algorithms. 

- **Machine Learning (ML):** 

   - Requires splitting data into training and testing sets for model building. 

   - Utilize AI techniques to explain model predictions and understand hidden causal relationships. 

- **Tools:** 

   - **Excel/SQL:** Built-in functions, pivot tables, and temporary tables for calculations. 

   - **Programming Languages:** Python and R, with libraries/packages for advanced analysis. 

- **Importance:** This step provides actionable insights and a deeper understanding of trends, essential for decision-making. 

<mark>Jan 1st, 2025</mark> 

<mark>17</mark> 

# Step 5: Report your findings 

- **Purpose:** Summarize and communicate findings, tying insights into a compelling story for stakeholders. 

- **Product:** 

   - Single numbers, dashboards with KPIs, or detailed reports. 

   - Visuals such as charts, graphs, and tables convey trends and insights. 

- **Audience:** Tailor presentation formats for both technical and non-technical stakeholders. 

- **Techniques:** 

   - Select visualization methods that best suit the data and message. 

   - Transform raw information into clear, accessible narratives. 

- **Key Goals:** 

   - Simplify complex information, making it understandable and accessible to both technical and non-technical audiences. 

   - Use storytelling to highlight key points and guide decision-making. 

- **Outcome:** Facilitate a clear understanding of findings to support informed decisions and future planning. 

<mark>Jan 1st, 2025</mark> 

<mark>18</mark> 

# Outline 

- Introduction to Data 

- Data analysis vs. Data analytics 

- Process of data analytics 

- Introduction to Data analysis? 

   - What is Data Analysis? 

   - Types of data analysis 

- Statistical science in Data analysis 

- Collecting data 

<mark>Jan 1st, 2025</mark> 

<mark>19</mark> 

# What is Data analysis? 

- Data analysis is a core component of analytics, focusing specifically on the in-depth examination of data. 

- Data analysis is a focused activity that forms a single step within the broader data analytics pipeline. 

- Its goal is to interpret and describe data, generating predictions that give insights into data. 

- There are various approaches we can use for data analysis: 

   - _A/B Testing_ : Compares two groups to evaluate differences. 

   - _Data Fusion & Integration_ : Combines data from various sources for greater accuracy. 

   - _Data Mining_ : Extracts patterns from large datasets for insights. 

   - _Machine Learning_ : Automates model development using algorithms. 

- Data analysis is studying an existing dataset without needing new data collection, aiming to extract useful information. 

<mark>Jan 1st, 2025</mark> 

<mark>20</mark> 

# Types of Data analysis 

- Descriptive analysis 

- Diagnostic analysis 

- Predictive analysis 

- Prescriptive analysis 

<mark>Jan 1st, 2025</mark> 

<mark>21</mark> 

# Descriptive analysis 

- **<u>Definition:</u>** Descriptive analytics provides a summary and analysis of past data to understand what occurred. It is typically used to answer questions such as “What happened?” and “How many?”. 

- **<u>Goal:</u>** In qualitative and quantitative research, descriptive analysis is often the first step in data analysis, providing a foundation for more advanced statistical or inferential analyses. 

- **<u>Method:</u>** Descriptive analysis typically includes statistical summaries and basic calculations, such as averages, percentages, or counts. 

- **<u>Require:</u>** To use descriptive analytics effectively, it’s essential to ensure your data is accurate and high-quality. 

<mark>Jan 1st, 2025</mark> 

<mark>22</mark> 

# Descriptive analysis (cont.) 

- **<u>Examples:</u>** 

   - A candy store can use past sales data to identify popular products and seasonal trends. For instance, candy sales typically increase in December, when Christmas arrives. 

   - A retail company analyzed history data and discovered that its annual sales reached $1.2 million, with December contributing 25% of the total revenue. This insight helps identify peak sales periods for resource allocation and marketing strategies. 

   - A tech company monitors app feature usage and discovers that 75% of active users use feature X, while feature Y has the lowest engagement at 15%. This insight highlights where to focus feature improvements or promotional efforts. 

   - Patient data can be summarized to identify prevalent health trends. For example, an analysis may show that most flu cases occur between October and June, highlighting the need for targeted vaccination campaigns. 

<mark>Jan 1st, 2025</mark> 

<mark>23</mark> 

# Diagnostic analysis 

- **<u>Definition:</u>** Diagnostic analytics goes beyond descriptive analytics by identifying the root causes of issues. It answers questions like “Why did it happen?” and “What caused it?”. 

- **<u>Goal:</u>** This approach involves exploring data to find relationships and correlations that explain specific problems. 

- **<u>Method:</u>** The commonly used techniques are regression analysis, hypothesis testing, and causal analysis. 

- **<u>Require:</u>** Challenges include obtaining high-quality data and ensuring accurate insights. Additionally, the techniques involved can be complex, often requiring specialized skills to apply effectively. 

<mark>Jan 1st, 2025</mark> 

<mark>24</mark> 

# Diagnostic analysis (cont.) 

- **<u>Examples:</u>** 

   - An eco-friendly store saw a revenue surge in one state, driven by increased sales of canvas tote bags. Analysis revealed the cause: the state's new law banning plastic bags boosted demand for reusable alternatives. 

   - A company's hiring report revealed that one department hired the most employees, but there was no net increase in its department. It was losing people as fast as it had hired them. Further analysis found the issue centered on a team with below-average industry pay. This insight led the company to review pay scales, gather employee feedback, and implement retention strategies. 

   - A manufacturer faced irregular failures in valuable machines. Diagnostic analytics of machine logs revealed a recent software update as the likely cause. Uninstalling the update confirmed and resolved the issue. 

<mark>Jan 1st, 2025</mark> 

<mark>25</mark> 

# Predictive analysis 

- **<u>Definition:</u>** Predictive analytics analyze historical data and predict future events. It is often used to answer questions such as “What is likely to happen?” or “What if?”. 

- **<u>Goal:</u>** This analysis predicts future outcomes based on current or historical data, though predictions are only estimates. 

- **<u>Method:</u>** Predictive analysis typically uses statistical and machine learning techniques to analyze previous data. 

- **<u>Require:</u>** Accurate predictions require high-quality data, and selecting the proper modeling techniques is essential. The accuracy of predictive analytics depends on the detail and depth of the data used. 

<mark>Jan 1st, 2025</mark> 

<mark>26</mark> 

# Predictive analysis (cont.) 

- **<u>Examples:</u>** 

   - In marketing, consumer data is abundant and leveraged to create content, advertisements, and strategies to reach better potential customers where they are. You engage in predictive analytics by examining historical behavioral data and using it to predict what will happen in the future. 

   - Healthcare providers use predictive analytics to identify patients at risk of developing certain diseases, enabling early interventions and personalized treatment plans. 

   - Banks can use predictive analytics to evaluate credit risk and decide whether to approve a loan. Open banking enables the creation of personalized behavioral models to assess creditworthiness, offering customers better and more affordable access to financial products like accounts, credit cards, and mortgages. 

<mark>Jan 1st, 2025</mark> 

<mark>27</mark> 

# Prescriptive analysis 

- **<u>Definition:</u>** Prescriptive analysis combines the insight from previous analyses to provide recommendations for actions. It is commonly used to answer questions such as “What should we do?” or “How can we improve?”. 

- **<u>Goal:</u>** This approach involves using optimization techniques to identify the best course of action given a set of constraints and objectives. 

- **<u>Method:</u>** This analytics requires a comprehensive understanding of the data and the ability to model and simulate various scenarios to determine the optimal course of action. It is the most complex of the four analytics approaches. 

- **<u>Require:</u>** This analytics requires high-quality data for accurate analysis and optimization. The complexity of optimization algorithms often requires specialized skills to implement effectively. 

<mark>Jan 1st, 2025</mark> 

<mark>28</mark> 

# Prescriptive analysis (cont.) 

- **<u>Examples:</u>** 

   - A key priority for transportation companies is <u>optimizing route planning.</u> Freight operators rely on prescriptive analytics, which considers weather conditions and fuel prices, to identify the fastest and most fuel-efficient routes. This approach leads to on-time deliveries and lower operational expenses. 

   - Prescriptive analytics enables marketers to analyze emerging trends and gain data-driven insights, helping them optimize ad placements and content types. For example, if younger audiences engage more with interactive polls on social media, marketers can adapt their strategies <u>to prioritize this content, increasing reach and engagement.</u> 

   - Understanding guests' preferences is crucial in the hotel industry. Hotels use prescriptive analytics to <u>segment their customer base,</u> enabling them to offer personalized packages and experiences. This approach enhances customer satisfaction, fostering repeat bookings, positive reviews, and the potential for brand advocacy. 

<mark>Jan 1st, 2025</mark> 

<mark>29</mark> 

|**Approach**|**Definition**|**Answers the quesitons**|
|---|---|---|
|Descriptive|Describes and summarizes data to gain insights<br>into what has happened in the past.|•<br>What happened?<br>•<br>How many?|
|Diagnostic|Identifies the root cause of an issue or problem.|•<br>Why did it happen?<br>•<br>What caused it?|
|Predictive|Analyzes historical data and makes predictions<br>about future events.|•<br>What is likely to happen?<br>•<br>What if?|
|Prescriptive|Provides recommendations for actions you should<br>take based on the analysis.|•<br>What should we do?<br>•<br>How can we improve?|



<mark>Jan 1st, 2025</mark> 

<mark>30</mark> 

# Outline 

- Introduction to Data 

- Data analysis vs. Data analytics 

- Process of data analytics 

- Introduction to Data analysis 

- Statistical science in Data analysis 

- Collecting data 

<mark>Jan 1st, 2025</mark> 

<mark>31</mark> 

# Statistical science in Data analysis 

- **What is Statistics?** 

   - The study of designing studies/experiments, collecting, modeling, and analyzing data. 

   - Helps make informed decisions and scientific discoveries under uncertain and variable conditions. 

   - Core principle: Learning from Data to address real-world problems. 

- **Applications:** 

   - Social scientists: Analyze societal trends like juvenile crime rates. 

   - Medical researchers: Evaluate survival rates of therapies. 

   - Corporate executives: Monitor quarterly sales. 

   - Market researchers: Assess consumer preferences. 

   - Engineers: Examine contamination in water samples. 

   - Government employees: Analyze census data and policy impacts. 

<mark>Jan 1st, 2025</mark> 

<mark>32</mark> 

# Why study Statistics? 

- **Evaluate published data** 

   - Informed assessment of numerical facts in media, advertisements, polls, and research studies. 

   - Understanding the validity of inferences made from samples. 

   - Distinguishing between accurate and misleading data presentations. 

- **Criticize data-based reports** 

   - Statistics can be used to distort the truth, either intentionally or unintentionally. 

   - A well-informed reader can identify when data has been manipulated or misrepresented. 

<mark>Jan 1st, 2025</mark> 

<mark>33</mark> 

# The Role of Statistics in Various Fields 

- Statistics is a critical tool in science, business, and industry. Professionals across fields must understand its concepts, strengths, and limitations to make informed decisions and interpret data effectively. 

   - **Court Trials** : Statistics and probability are increasingly used to evaluate the quality of evidence. 

   - **Sciences** : Social, biological, and physical sciences rely on statistical methods, using sample surveys and experiments to observe natural phenomena and test theories. 

   - **Business** : Statistical techniques help forecast sales and profits based on sample data. 

   - **Engineering and Manufacturing** : Statistics monitor product quality and ensure consistency. 

   - **Accounting** : Sampling techniques support audits by analyzing account data. 

`o` ......... 

<mark>Jan 1st, 2025</mark> 

<mark>34</mark> 

# Example 

An American history professor at a major university was interested in knowing the history literacy of college freshmen. In particular, he wanted to find what proportion of college freshmen at the university knew which country controlled the original 13 colonies prior to the American Revolution. The professor sent a questionnaire to all freshman students enrolled in CS 101 and received responses from 318 students out of the 7,500 students who were sent the questionnaire. One of the questions was “What country controlled the original 13 colonies prior to the American Revolution?” 

- a) What is the population of interest to the professor? 

- b) What is the sampled population? 

- c) Is there a major difference in the two populations? Explain your answer. 

- d) Suppose that several lectures on the American Revolution had been given in CS 101 prior to the students receiving the questionnaire. What possible source of bias has the professor introduced into the study relative to the population of interest? 

<mark>Jan 1st, 2025</mark> 

<mark>35</mark> 

# Outline 

- Introduction to Data 

- Data analysis vs. Data analytics 

- Process of data analytics 

- Introduction to Data analysis 

- Statistical science in Data analysis 

- Collecting data 

<mark>Jan 1st, 2025</mark> 

<mark>36</mark> 

# Collecting data 

- A _case_ refers to an _experimental unit_ , which is an individual from whom data are collected. 

- For humans, cases are often referred to as _participants_ , while for animals, the term _subjects_ is commonly used. 

- A _variable_ is a measurable characteristic that can take on different values, meaning it varies between cases. 

- A _constant_ remains the same across all cases in a research study. 

- **Examples:** 

   - A teacher examines whether first-year students who spend more time reading at home achieve higher homework and exam grades. In this study, the students are the **_cases_** , and the **_three variables_** are the amount of time spent reading at home, homework grades, and exam grades. The student’s year level is **_constant_** because all participants are in their first year. 

   - Researchers investigate the relationship between age and weight in a sample of 100 male sea otters ( _Enhydra lutris_ ). In this study, the **_cases_** are 100 otters, and the **_two variables_** are age and weight. Biological sex is a **_constant_** because all subjects are male, and species is also a **_constant_** because all are sea otters. 

<mark>Jan 1st, 2025</mark> 

<mark>37</mark> 

# Categorical & Quantitative Variables 

- Variables can be classified into two main types based on the kind of data they represent: 

   **1. Categorical Variables** : These are variables that represent groupings or categories. The categories may have no logical order or a logical order with inconsistent differences between groups. Categorical variables are also known as _qualitative variables_ . 

**Example** : A teacher asks his class about their preferred kind of book—fiction, non-fiction, or fantasy. This is a categorical variable because the responses are grouped into non-ordered categories. 

**2. Quantitative Variables** : These variables take on numerical values with meaningful magnitudes and consistent intervals. Quantitative variables are also referred to as _numerical variables_ . 

**Example** : A runner tracks the number of steps he takes each day. Since the number of steps is measured in numerical values with meaningful magnitudes and consistent intervals, it is a quantitative variable. 

<mark>Jan 1st, 2025</mark> 

<mark>38</mark> 

# Explanatory & Response Variables 

- One variable can be used to predict or explain differences in another variable: 

   **1. Explanatory Variable** : Also called the independent or predictor variable, this variable explains variations in the response variable. In an experimental study, the researcher manipulates this variable. 

   **2. Response Variable** : Also called the dependent or outcome variable, it is the variable whose value is influenced by or depends on the explanatory variable. In an experimental study, it represents the outcome measured after the explanatory variable is manipulated. 

- **Examples:** 

   - A team studies how the origin of cocoa beans affects hyperactivity levels. They compare cocoa from three regions: Vietnam, Africa, and Mexico. The _explanatory variable_ is the origin of the cocoa bean, with three places (Vietnam, Africa, and Mexico). The _response variable_ is the level of hyperactivity. 

   - An I-Ching research team wants to know if they can use the time to predict the weather. They take a random sample of 50 days and record the time of day and corresponding weather conditions. The team wants to use the time to predict the weather, so the _explanatory variable_ is time, and the _response variable_ is the weather. 

<mark>Jan 1st, 2025</mark> 

<mark>39</mark> 

# Overview of Studies 

There are two main type of studies: 

- **Observational Studies:** 

   - The researcher observes and records information about the subjects under study without interfering with the processes generating the data. 

   - In this role, the researcher remains a passive observer of the events unfolding. 

   - In observational studies, we sample from populations where the factors (or treatments) are already present and compare samples with respect to the factors (treatments) of interest to the researcher. 

- **Experimental Studies:** 

   - The researcher actively manipulates specific variables, known as explanatory variables, and observes their effects on the response variables related to the experimental subjects. 

   - In an experimental study’s controlled environment, we can randomly assign the people as objects under study to the factors (or treatments) and then observe the response of interest. 

<mark>Jan 1st, 2025</mark> 

<mark>40</mark> 

# Observational Studies 

- **Definition:** 

   - The researcher observes and records information about the subjects under study without interfering with the processes generating the data. 

`o` In this role, the researcher remains a passive observer of the events unfolding. 

- **Limitations:** 

   - **Confounding bias:** The response variable may be influenced by factors other than the explanatory variable. These uncontrolled factors are called confounding variables. 

   - **Lack of Control:** Because the researcher cannot control the physical setting or these additional variables, it becomes difficult to separate their effects from those of the explanatory variable. 

   - **No Causation:** Addressing various biases and sampling problems is crucial to ensuring a survey reliably represents the population’s current state. One common challenge in observational studies is mistakenly attributing cause-andeffect relationships to spurious associations between factors. 

<u>Example: A central public health question is the relationship between dietary fat intake and heart disease. However,</u> it would be unethical to randomly assign participants to high-fat diets and monitor them over time to determine whether heart disease develops. 

<mark>Jan 1st, 2025</mark> 

<mark>41</mark> 

# Observational Studies (cont.) 

- Observational studies can be categorized as either comparative or descriptive: 

   - Comparative studies compare the effectiveness of two or more methods to achieve a specific outcome. Alternatively, comparisons might focus on groups with a shared characteristic. 

      - <u>Example:</u> 

      - § Healthcare delivery methods may be compared based on cost effectiveness. 

      - § Analyzing the starting incomes of engineers who graduated from private versus public universities. 

   - Descriptive studies aim to characterize a population or process based on specific attributes. <u>Example:</u> 

      - § Examining the health status of children under 5 in families without health insurance. 

      - § Analyzing the frequency of overcharges by companies contracted under federal military agreements. 

<mark>Jan 1st, 2025</mark> 

<mark>42</mark> 

# Three basic types of Observational studies 

- A sample survey is a study that provides information about a population at a specific time (current information). 

<u>Example: In the health sciences, a sample survey involves asking all participants about their current disease status and</u> any past exposures to the disease. 

- A prospective study (nghiên cứu theo thời gian) observes a population at the present using a sample survey and then follows the subjects over time to track the occurrence of specific outcomes. 

<u>Example: A prospective study begins by identifying a group of disease-free individuals and monitoring them over time</u> until some develop the disease. The occurrence or absence of the disease is then analyzed about variables measured at the start of the study. 

- A retrospective study (nghiên cứu bệnh chứng) currently observes a population using a sample survey and gathers information about the subjects regarding outcomes that have already occurred. 

<u>Example:</u> In a retrospective study, two groups of subjects are identified: _cases_ (those with the disease) and _controls_ (those without the disease). The researcher then examines the subjects’ past health habits to determine correlations with their current health status. 

<mark>Jan 1st, 2025</mark> 

<mark>43</mark> 

# Experimental Studies 

- **Definition:** 

   - The researcher actively manipulates certain variables, known as explanatory variables, and observes their effects on the response variables related to the experimental subjects. 

   - The purpose is to determine causal relationships. 

   - Researchers control crucial factors through randomization or controlled settings by assigning experimental units to treatments or selecting units from treatment populations. 

- **Limitation:** 

   - **Cost and Resource Intensive** : Designing, executing, and maintaining experiments can be expensive and resource-heavy, especially in controlled environments. 

   - **Artificiality of Controlled Environments** : Highly controlled environments may not replicate real-world conditions, reducing the natural validity of the findings. 

   - **Limited Scope** : Experimental studies often focus on specific variables, potentially ignoring broader systemic factors or complex interactions. 

   - **Difficulty in Generalizing Results** : Results obtained in artificial settings may not accurately represent outcomes in more natural or varied real-world scenarios. 

   - **Ethical Concerns** : Certain manipulations may not be moral or feasible, especially when dealing with human or animal subjects. 

<mark>Jan 1st, 2025</mark> 

<mark>44</mark> 

# Experimental Studies (cont.) 

- An experimental study can be conducted in various ways: 

   - The researcher aims to gather information from a natural, undisturbed setting. 

<u>Example:</u> A study might compare the reading scores of second-grade students in public, religious, and private schools. 

- The researcher works within a highly controlled laboratory environment, which is an artificial setting for the study. 

<u>Example:</u> Studying the impact of humidity and temperature on ticks’ life cycles would require a laboratory setting, as it would be impossible to control these factors in the ticks’ natural environment. 

<mark>Jan 1st, 2025</mark> 

<mark>45</mark> 

# Experimental Studies (cont.) 

- The experiment should accurately reflect the true state of nature. 

- To ensure the experiment is useful, there must be a careful balance between controlling conditions and representing reality. 

- In experimental studies, the researcher controls the important factors by one of two methods: 

   - **Method 1:** The researcher randomly assigns subjects to different treatments. The researcher controls the selection of experimental units from a homogeneous population and their assignment to the treatments. 

<u>Example: 10 rats might be randomly assigned to each of four dose levels of an experimental drug.</u> 

- **Method 2:** Subjects are randomly selected from different populations of interest. While the researcher controls the random sampling from the populations, they do not control how the subjects are assigned to the treatments. 

<u>Example: 50 male and 50 female dogs might be randomly selected from animal shelters in large and small cities and</u> tested for heartworms. 

<mark>Jan 1st, 2025</mark> 

<mark>46</mark> 

# Systematic Planning in Experimental Studies 

- A systematic plan is essential to ensure reliability and accuracy before conducting experiments. 

- Key components: 

   - Define research objectives and treatments. 

   - Identify and account for extraneous factors (e.g., environmental or unit differences). 

   - Use randomization to assign units to treatments or select units from populations. 

- Goal of Randomization: 

   - Randomization ensures observed differences in treatment group responses are due to group differences, not uncontrolled factors. 

<mark>Jan 1st, 2025</mark> 

<mark>47</mark> 

# Systematic Planning in Experimental Studies (cont.) 

- The plan should also include many other aspects of how to conduct the experiment. Some of the items that should be included in such a plan are listed here: 

   1. The research objectives of the experiment. 

   2. The selection of the factors that will be varied (the treatments). 

   3. The identification of extraneous factors that may be present in the experimental units or in the environment of the experimental setting (the blocking factors). 

   4. The characteristics to be measured on the experimental units (response variable). 

   5. The method of randomization, either randomly selecting experimental units from treatment populations or randomly assigning experimental units to treatments. 

   6. The procedures to be used in recording the responses from the experimental units. 

   7. The selection of the number of experimental units assigned to each treatment may require designating the level of significance and power of tests or the precision and reliability of confidence intervals. 

   8. A complete listing of available resources and materials. 

<mark>Jan 1st, 2025</mark> 

<mark>48</mark> 

# Terminology 

- **Designed Experiment** : A structured investigation to observe, measure, and compare groups based on a specified response, with researcher-controlled elements ensuring valid statistical inferences. 

- **Variables** : 

   - **Factors (Controlled Variables)** : Selected by the researcher to define comparison groups based on the hypothesis. 

   - **Response Variables** : Measured outcomes, not controlled by the researcher. 

- **Treatments** : Conditions created from factor levels to address research questions. 

   - **Single Factor** : Treatments equal factor levels. 

   - **Multiple Factors** : Treatments formed by combining factor levels (factorial treatment design). 

<mark>Jan 1st, 2025</mark> 

<mark>49</mark> 

# Example 

- A researcher studies the conditions that maximize weight gain in commercially raised shrimp. The study focuses on three water temperatures (25°C, 30°C, 35°C) and four water salinity levels (10%, 20%, 30%, 40%). Shrimp are raised in containers set to these specified temperature and salinity conditions. The weight gain of the shrimp in each container is recorded after six weeks. 

- Other factors, like shrimp density, variety, size, and feeding type, can also influence weight gain, but these are kept constant during the study. 

- The experiment uses 24 containers, and a specific shrimp variety and size is selected. The shrimp density in each container is fixed, and one of the three water temperatures and one of the four salinity levels are randomly assigned to each container. All other conditions are controlled and kept the same across the 24 containers for the study duration. Despite efforts to control variables, some level of variation will naturally occur. 

- After six weeks, the shrimp are harvested and weighed. 

- Identify the response variable, factors, and treatments in this example. 

<mark>Jan 1st, 2025</mark> 

<mark>50</mark> 

# Designs for Experimental Studies 

- Experimental design refers to how participants are allocated to different experimental groups. 

- The key principles of experimental design are: 

   **1. Replication** : 

      - This involves repeating treatments within the experiment. 

      - Replication enhances reliability by providing more precise estimates of treatment effects compared to relying on a single observation. 

   **2. Randomization** : 

      - Randomization is the process of assigning treatments to experimental units entirely by chance. 

      - This ensures that the allocation is unbiased and reduces the influence of confounding variables. 

   **3. Local Control** : 

      - Local control refers to minimizing experimental error by organizing the experimental area into smaller, homogeneous blocks. 

      - This helps account for variations within the experimental environment and improves the accuracy of the results. 

<mark>Jan 1st, 2025</mark> 

<mark>51</mark> 

# Completely Randomized Design (CRD) 

- **Definition** : 

   - Simplest experimental design based on randomization and replication, ensuring that each experimental unit has an equal chance of receiving any treatment. 

   - Differences among experimental units receiving the same treatment are attributed to experimental error. 

   - Suitable for homogeneous experimental unit. 

- **Advantages:** 

   - CRD allows maximum use of all available experimental materials. 

   - The design accommodates any number of treatments and ensures equal application of treatments multiple times. 

   - The analysis remains straightforward even if some observations are lost, rejected, or missing. 

   - It provides the highest number of degrees of freedom for estimating error variance. 

- **Disadvantages:** 

   - CRD tends to have higher experimental error without applying the principle of local control. 

   - In some cases, CRD may provide less information than other experimental designs. 

<mark>Jan 1st, 2025</mark> 

<mark>52</mark> 

# Randomized Block Design (RBD) 

- **Definition:** 

   - A Randomized Block Design is a statistical experimental design that controls variability among experimental units by grouping them into “blocks” based on a specific characteristic. 

   - Within each block, treatments are randomly assigned to units. 

   - The goal is to isolate the variability attributable to the blocking factor and focus on treatment effects. 

- **Advantages:** 

   - The design reduces the effects of confounding variables by grouping similar units into blocks, leading to more accurate treatment comparisons. 

   - It allows for better detection of treatment differences with fewer experimental units. 

- **Disadvantages:** 

   - The design can become challenging when the number of treatments or blocks increases. 

   - This design controls for only one extraneous source of variability (due to blocks). Additional extraneous sources of variability tend to increase the error term, making it more difficult to detect treatment differences. 

<mark>Jan 1st, 2025</mark> 

<mark>53</mark> 

# Latin Square Design (LSD) 

- **Definition:** 

   - The LSD is a statistical experimental design used when there are two sources of variability that need to be controlled or “blocked.” 

   - This design is used to compare _t_ -treatment means in the presence of two extraneous sources of variability. 

   - The t treatments are then randomly assigned to the rows and columns so that each treatment appears in every row and every column of the design. 

- **Advantages:** 

   - The design is appropriate for comparing t-treatment means in the presence of two sources of extraneous variation, each measured at t levels. 

   - The analysis is quite simple. 

- **Disadvantages:** 

   - The Latin square best compares t treatments when 5 ≤ 𝑡 ≤10. 

   - Any additional extraneous sources of variability tend to inflate the error term, making detecting differences among the treatment means more complex. 

   - The effect of each treatment on the response must be approximately the same across rows and columns. 

<mark>Jan 1st, 2025</mark> 

<mark>54</mark> 

