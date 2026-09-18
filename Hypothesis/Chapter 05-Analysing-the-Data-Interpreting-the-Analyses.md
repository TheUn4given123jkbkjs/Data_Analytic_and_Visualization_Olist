

<!-- Start of picture text -->
y DAITON HODU C THANGTON BUCUNIVERSITYTHANG<br><!-- End of picture text -->

**Chapter 5: Analysing the Data, Interpreting the Analyses** 

**Lecturer:** Ho Thi Linh, PHD 

#### **Context: Learning from Data** 

01 

02 

Defining the Problem Collecting the Data Identify research questions and objectives clearly Gather information through surveys and experimental studies 

03 

04 

Summarising the Data Apply descriptive statistics and probability distributions 

Analysing & Communicating Draw inferences and present findings effectively 

**Today's Focus:** Step 4 3 Making inferences from sample data to understand entire populations 

#### **Foundation of Inference** 

###### Population 

###### Sample 

**Definition:** All measurements of interest in your study 

**Definition:** Subset of the population we actually observe 

**Parameters (Unknown):** 

Mean (¿) 

**Statistics (Known):** 

Variance ( ²) 

- Proportion (p) 

Mean (3) Variance (s²) Proportion (p�) 

**Goal:** Use sample information to make reliable inferences about the entire population 

#### **Types of Statistical Inference** 

Estimation 

**Goal:** Estimate population parameter values 

**Methods:** 

Hypothesis Testing **Goal:** Test whether parameter meets a specific condition 

Point Estimate (e.g., 3 for ¿) Interval Estimate (Confidence Intervals) 

**Methods:** 

Test Statistic calculation 

Provides a range of plausible values for unknown parameters 

P-value interpretation 

Results in a decision to reject or fail to reject H 

#### **Estimating the Population Mean (¿)** 

###### Point Estimation 

The sample mean (3) serves as our best point estimate for the population mean (¿). This single value represents our most reasonable guess based on available sample data. 

Interval Estimation (Confidence Intervals) 

For large samples (n g 30) or when population standard deviation ( ) is known, we construct confidence intervals using: 

Ã CI : yË ± z ³/2 n 

When is unknown but the sample size is large, we substitute the sample standard deviation (s) for . This approach leverages the Central Limit Theorem, which ensures our sampling distribution approximates normality. 

#### **Determining Required Sample Size (n)** 

Achieving desired precision requires careful sample size planning. The margin of error (E) determines how close our estimate will be to the true parameter. 

###### Sample Size Formula 

2 2 z Ã ³/2 n = E<sup>2</sup> 

Key Requirements Preliminary estimate of needed Desired margin of error (E) Confidence level specification 

Practical Applications Survey planning Experimental design Controlling Type I and Type II errors 

###### **Hypothesis Testing for ¿: Procedure** 

###### **Standardised Test Statistic** 



<!-- Start of picture text -->
yË 2 ¿0<br>z =<br>n<br>Ã/<br><!-- End of picture text -->

###### Right-tailed Test 

- 1 Reject H  if z g z 

Used when testing if parameter is greater than specified value 

###### Left-tailed Test 

- 2 Reject H  if z f 3z 

Used when testing if parameter is less than specified value 

###### Two-tailed Test 

3 Reject H  if |z| g z /2 

Used when testing if parameter differs from specified value 

Decision making relies on either rejection regions or P-value comparisons with the significance level . 

###### **Example: Hypothesis Test for ¿** 

###### **Case Study: Cholesterol Levels** 

###### Given Data Hypotheses 

Sample size: n = 100 

H : ¿ = 190 (null hypothesis) 

Sample mean: 3 = 178.2 

H°: ¿ b 190 (alternative hypothesis) 

Sample std dev: s = 45.3 

Hypothesised mean: ¿  = 190 

Significance level: = 0.05 

01 

02 

03 

Calculate Test Statistic 

Determine Critical Value 

###### Make Decision 

z j 32.60 For = 0.05, two-tailed: ±1.96 Since |32.60| > 1.96 ³ Reject H 

**Conclusion:** Mean cholesterol level differs significantly from 190, providing evidence that the population mean is not equal to the hypothesised value. 

#### **Inference for ¿ ( Unknown, Small n)** 

When population standard deviation is unknown and sample size is small, we use the Student's t-distribution, assuming the population follows a normal distribution. 

###### **Key Formulas** 

Test Statistic 

Confidence Interval 



<!-- Start of picture text -->
yË 2 ¿0<br>t =<br>n<br>s/<br><!-- End of picture text -->

s <u>yË ± t</u> ~~³/2,n21~~ ~~<u>n</u>~~ 

Follows t-distribution with (n-1) degrees of freedom 

Provides interval estimate when is unknown 

**Important:** The t-distribution accounts for additional uncertainty introduced by estimating with s, resulting in wider confidence intervals compared to z-intervals. 

#### **Dealing with Non-normal Populations** 

When dealing with small sample sizes from non-normal populations, traditional t-tests become invalid. This situation requires alternative statistical approaches. 

Bootstrap Methods 

Resampling techniques that create thousands of bootstrap samples from original data. These methods don't require normality assumptions and provide robust estimates of sampling distributions. Computationally intensive but flexible Works well with various population shapes Provides empirical confidence intervals 

Median-based Inference Non-parametric approaches like the Sign Test focus on population medians rather than means. These methods are distribution-free and robust to outliers. 

No distributional assumptions required Less sensitive to extreme values May sacrifice statistical power for robustness 

###### **Case Study: Nurses' Health Study** 

168 

# 36.92 

# 6.73 

Sample Size Sample Mean Participants in health study Average health metric 

Standard Deviation Measure of variability 

###### Research Hypothesis 

Testing whether the population mean exceeds 30 (¿ > 30) 

Results 

**95% Confidence Interval:** (35.90, 37.94) 

**Conclusion:** Since the entire confidence interval lies above 30, we have strong evidence that the mean PCF exceeds the recommended threshold. This provides compelling statistical support for the research hypothesis. 

### **Comparing Two Means (¿¡ 3 ¿¢)** 

When comparing means from two independent populations, we must carefully consider our assumptions and choose the appropriate statistical method. 

###### Essential Assumptions 

Independence 

Random, independent samples from each population 



Normality 

Populations approximately normally distributed 

Two Analytical Approaches 

Equal Variances 

Unequal Variances 

**Method:** Pooled t-test 

**Method:** Separate-variance t' test 

Assumes ¡² = ¢² and combines sample variances for greater precision 

Accounts for ¡² b ¢² using individual sample variances 

###### **Pooled t-Test ( ¡² = ¢²)** 

When population variances are assumed equal, we can pool sample variances to create a more precise estimate of the common population variance. 

###### Pooled Variance Formula 



This weighted average gives more influence to the sample with larger degrees of freedom. 

###### Test Statistic 



The test statistic follows a t-distribution with (n¡ + n¢ - 2) degrees of freedom. The pooled standard error accounts for variability in both samples whilst assuming equal population variances. 

**Advantage:** Increased degrees of freedom lead to more powerful tests when the equal variance assumption is valid. 

## **Separate-Variance t' Test ( ¡² b ¢²)** 

When population variances differ substantially, the separate-variance approach provides more reliable inferences by avoiding the equal variance assumption. 

###### **Test Statistic** 

###### **Confidence Interval** 



<!-- Start of picture text -->
2 (yË1 2 yË2) 2 D0<br>t =<br>2 2<br>s s<br>1 + 2<br>n1 n2<br><!-- End of picture text -->



<!-- Start of picture text -->
2 2<br>s s<br>1 2<br>( y Ë 1 2 y Ë 2 ) ± t³/2 +<br>n1 n2<br><!-- End of picture text -->

Uses individual sample variances without pooling 

Provides interval estimate for difference in means 

The degrees of freedom calculation becomes complex (Welch's approximation), but statistical software handles this automatically. This method maintains proper Type I error rates even when variances differ. 

**Key Advantage:** Robust performance regardless of whether population variances are equal or unequal. 

###### **Example: Tennis Racket Study** 

This compelling case study demonstrates why choosing the correct statistical method matters when variances and sample sizes differ between groups. 

1 

- Problem Identification 

Comparing oversized versus conventional tennis rackets for performance differences 

- 2 Variance Assessment 

Statistical tests revealed unequal variances between the two racket types 

- 3 Method Selection 

Separate-variance t' test required due to unequal variances assumption violation 

- 4 Conflicting Results 

Pooled t-test rejected H , but t' confidence interval contained 0 

**Critical Learning Point:** When variances and sample sizes differ substantially, the pooled t-test can provide misleading results. Always verify assumptions before selecting your analytical approach. 

###### **Advanced Methods: Paired Data & Non-parametric Alternatives** 

###### Paired Data Analysis 

When observations are naturally paired (before/after, matched subjects), analyse the differences d_i = y¡� - y¢� rather than treating samples as independent. 



This approach eliminates between-subject variability, often resulting in more powerful tests. 

###### Non-parametric Alternatives 

Independent Samples 

###### **Wilcoxon Rank-Sum Test** 

Compares distributions without assuming normality. Ranks all observations and compares rank sums between groups. 

Paired Data 

###### **Wilcoxon Signed-Rank Test** 

Analyses signed ranks of differences, robust to outliers and nonnormal distributions. 

**When to Use:** These distribution-free methods are essential when normality assumptions are severely violated, providing reliable inference without parametric assumptions. 

#### **Comparing Two Proportions** 

When comparing proportions between two independent groups, we employ specialised statistical techniques to determine whether observed differences are statistically significant or merely due to random variation. 

###### Test Statistic 



<!-- Start of picture text -->
2<br>p^1 p^2<br>z =<br>p^(1 2 p^)(1/n1 + 1/n2)<br><!-- End of picture text -->

This z-statistic compares the difference between sample proportions to the expected standard error under the null hypothesis. 



<!-- Start of picture text -->
Confidence Interval<br>p^1(12p^1) p^2(12p^2)<br>(p^ 1 2 p^ 2 ) ± z ³/2 n 1 + n 2<br>The confidence interval provides a range of plausible<br>values for the true difference between population<br>proportions.<br><!-- End of picture text -->

#### **Inferences About Variances ( ²)** 

Moving beyond means and proportions, understanding variability within populations is crucial for comprehensive statistical analysis. Variance measures how spread out data points are from the central tendency, providing insight into the consistency and reliability of our observations. 

In many practical applications, the amount of variation in data can be just as important as4or even more important than4the average value itself. This section explores the statistical methods for making inferences about population variances. 

**The Critical Importance of Variability** Why Variability Matters 

In statistical analysis, variability is often as crucial as the mean itself. Understanding and controlling variation forms the foundation of effective decision-making across numerous fields. 

Quality Control 

Risk Assessment 

Manufacturing processes require consistent output. High variability indicates unstable processes, leading to defective products and increased costs. Monitoring variance helps maintain quality standards. 

In finance and insurance, variability measures uncertainty and risk. Lower variance typically indicates more predictable outcomes, whilst higher variance suggests greater potential for both gains and losses. 

#### **Single Variance Inference** 

When making inferences about a single population variance, we utilise the chi-square distribution. This approach allows us to test hypotheses about population variance and construct confidence intervals. 

###### Chi-Square Test Statistic 



<!-- Start of picture text -->
2 (n 2 1)s 2<br>Ç = 2<br>Ã<br>0<br><!-- End of picture text -->



<!-- Start of picture text -->
Confidence Interval<br>(n21)s 2 (n21)s 2<br>2 , 2<br>[ ÇU ÇL ]<br><!-- End of picture text -->

This statistic follows a chi-square distribution with (n-1) degrees of freedom under the null hypothesis that the population variance equals ². 

The confidence interval for variance uses upper (Ç²}) and lower (Ç²·) critical values from the chisquare distribution, providing bounds for the true population variance. 

###### **Practical Example: Coffee Weights Analysis** 



###### **Coffee Weight Variability Study** 

A coffee manufacturer wants to assess the consistency of their packaging process. They collected data from 30 packages and calculated the following statistics: 30 3.43 

Sample Size Sample Standard Deviation 

Packages measured for weight Grams - measure of weight variation in consistency analysis the sample 

**Results for 99% Confidence Interval:** 

CI for ²: (6.56, 26.21) square grams CI for : (2.56, 5.12) grams 

These intervals suggest the true population standard deviation lies between 2.56 and 5.12 grams with 99% confidence. 

###### **Comparing Two Variances** 

When comparing variability between two independent populations, we employ the F-test. This powerful tool helps determine whether two populations have significantly different variances. 

###### **F-Test Statistic** 

1 

2 s 1 F = 2 s 2 

The ratio of sample variances follows an F-distribution when both populations are normally distributed with equal variances under H . 

###### **Confidence Interval for Ratio of Standard Deviations** 

<u>s1 1 s1</u> F [ s2 F³/2 , s2 ³/2 ~~<u>]</u>~~ 2 

This interval estimates the ratio of population standard deviations, providing insight into relative variability between groups. 

#### **Critical F-Test Assumptions** 

**Warning:** The F-test is highly sensitive to departures from normality. Violation of this assumption can severely inflate Type I error rates, leading to incorrect conclusions about variance equality. 

01 

02 

03 

Verify Normality Consider Alternatives Interpret Cautiously Use normal probability plots, If normality is questionable, consider Even small deviations from Shapiro-Wilk tests, or other non-parametric alternatives or normality can affect F-test reliability, normality assessments before robust variance comparison so interpret results within this proceeding with F-tests. methods. context. 

#### **Multiple Variances Testing** 

###### **Brown-Forsythe-Levene (BFL) Test** 

When comparing more than two variances simultaneously, the BFL test provides a robust alternative to traditional F-tests. This method is particularly valuable when normality assumptions are questionable. 

###### Null Hypothesis 

###### Methodology 

H : All population variances are equal across groups 

Uses ANOVA on absolute deviations from group medians, making it more robust to non-normality than traditional variance tests 

This approach provides greater reliability when dealing with real-world data that may not perfectly follow normal distributions. 

###### **Case Study: E. coli Detection Methods** 

Comparing Variability Between Detection Methods 

Researchers compared the variability of two E. coli detection methods: HEC (Hydrophobic Grid-Membrane Filter) and HGMF (Hydrophobic Grid-Membrane Filter) to determine if measurement precision differs between techniques. 

1 Study Design 

Independent samples tested using both HEC and HGMF methods to assess measurement variability 

- 2 Statistical Analysis 

F-test conducted: F = 1.35 (not statistically significant at = 0.05) 

- 3 Conclusion 

Variances are similar between methods, allowing researchers to proceed with mean comparisons using pooled variance methods 

This finding is crucial for subsequent analyses, as similar variances justify using more powerful statistical tests for comparing mean detection rates between the two methods. 

#### **Summary of Key Statistical Procedures** 

Understanding when to apply different statistical procedures is essential for proper data analysis. This comprehensive summary guides your choice of appropriate methods based on the parameter of interest and underlying assumptions. 

|**Parameter**|**Inference**|**Distribution**|**Key Assumptions**|
|---|---|---|---|
|¿|Test/CI|z or t|Normality (if n small)|
|¿¡3¿¢|Test/CI|t or t2|Independence, equal/unequal variances|
|¿d|Test/CI|t|Normality of differences|
|²|Test/CI|Ç²|Normality|
|¡²/<br>¢²|Test/CI|F|Normality|
|Multiple<br>²|Test|BFL|Robust alternative|



##### **Verification of Statistical Assumptions** 

Proper statistical inference depends critically on meeting underlying assumptions. Failure to verify these assumptions can lead to invalid conclusions and poor decision-making. 

###### Independence 

Ensure observations are collected independently. Violation leads to underestimated standard errors and inflated Type I error rates. Consider study design, sampling methods, and potential clustering effects. 

###### Normality Assessment 

Use multiple approaches: normal probability plots (Q-Q plots), histograms, and formal tests like Shapiro-Wilk. Visual methods often more informative than formal tests, especially with large samples. 

###### Equal Variance Testing 

Apply robust tests like Brown-Forsythe-Levene rather than F-tests when normality is questionable. Examine residual plots and consider transformations if heteroscedasticity is detected. 

###### **Essential Graphical Methods for Data Analysis** 

Graphical methods provide intuitive understanding of data patterns, distributions, and relationships that numerical summaries alone cannot capture. These visual tools are indispensable for assumption checking and result interpretation. 



Histogram Boxplot Reveals distribution shape, Displays median, quartiles, identifying skewness, modality, spread, and outliers efficiently. and potential outliers. Essential Excellent for comparing for assessing normality distributions across multiple assumptions. groups. 

Normal Probability Plot Most reliable method for checking normality. Points falling along straight line indicate normal distribution. 



Profile Plot Scatterplot Shows mean responses across Visualises relationships between different conditions or time variables, revealing correlation points, revealing trends and strength, linearity, and potential interaction patterns. outliers. 

#### **Statistical vs Practical Significance** 

###### **The Critical Distinction** 

A fundamental principle in applied statistics: **statistical significance does not automatically imply practical significance** . This distinction is crucial for meaningful data interpretation. 

Statistical Significance 

Indicates that observed differences are unlikely due to chance alone (p < ). However, with large sample sizes, even trivial differences can be statistically significant. 

Practical Significance Refers to whether the magnitude of difference matters in real-world contexts. Small but statistically significant differences may lack practical importance. 

**The analyst's role extends beyond computation to thoughtful interpretation.** Consider effect sizes, confidence intervals, and domain expertise when drawing conclusions from statistical tests. 

###### **Effective Communication of Statistical Results** 

Clear communication transforms statistical analysis into actionable insights. A well-structured report ensures that findings reach and influence decision-makers effectively. 

1 2 Objectives & Methodology Descriptive Summaries Clearly state research questions, Present both numerical summaries and hypotheses, and analytical approaches. informative graphics. Tables and figures Provide sufficient detail for replication should stand alone and convey key whilst remaining accessible to the messages without requiring extensive intended audience. text. 

3 Inference Methods Justify choice of statistical procedures and clearly state assumptions. Address any violations and their potential impact on conclusions. 

4 5 Assumption Verification Results & Conclusions Document assumption checking Present findings in context, distinguishing procedures and results. Include relevant between statistical and practical diagnostic plots and discuss implications significance. Use confidence intervals for interpretation. alongside p-values for richer interpretation. 

6 Recommendations Translate statistical findings into actionable recommendations. Consider limitations, alternative explanations, and suggestions for future research. 

###### **Preview: Analysis of Variance (ANOVA)** 

###### Extending Beyond Two-Sample Comparisons 

When comparing means across more than two groups, ANOVA provides a comprehensive framework that controls familywise error rates whilst testing for overall differences. 

1 

2 

3 

###### **Between vs Within Variation** 

###### **F-Statistic Logic** 

###### **Decision Rule** 

ANOVA partitions total variation into components: variation between group means and variation within groups. This separation forms the foundation for testing. 

2 s B F = 2 s W 

Large F-values indicate that between-group variation exceeds what we'd expect from within-group variation alone, suggesting real group differences. 

When F is sufficiently large (exceeds critical value), we reject H  and conclude that at least one group mean differs significantly from the others. 

ANOVA represents the natural extension of two-sample t-tests to multi-group scenarios, maintaining statistical rigour whilst providing comprehensive insights into group comparisons. 

###### **Mastering Statistical Inference** 

Statistical inference represents the culmination of the 'Learning from Data' process, transforming raw observations into meaningful insights that inform decisions and advance knowledge. 

Mean Estimation & Testing Population Comparisons Foundation techniques for single population Methods for comparing means between inference using z and t distributions independent groups and paired observations 

Clear Communication Variance Inference Translating statistical findings into actionable Chi-square and F-tests for understanding and insights for decision-makers comparing population variability 

**The ultimate goal:** Use statistical methods to make rational, evidence-based inferences about populations from sample data, then communicate these findings clearly and effectively to stakeholders who can act upon them. 

Mastery of these concepts empowers you to extract meaningful insights from data, assess uncertainty appropriately, and contribute to evidence-based decision-making across diverse fields of study and practice. 

