Data Analysis and Visualization 

**Categorical Data** 

_Instructor: Tran Luong Quoc Dai, Ph.D._ 

# Outline 

- **Introduction to Categorical Data** 

- Inferences About a Population Proportion 

- Inferences About the Difference Between Two Population Proportions 

<mark>Feb 2nd, 2025</mark> 

<mark>2</mark> 

# Introduction 

- Up to this point, we have been primarily concerned with sample data measured on a quantitative scale. 

- Sometimes encounter situations where the levels of the variable of interest are identified only by name or rank. 

- Data obtained from these types of variables are called categorical or count data, and we are interested in the number of times each level of that variable occurs. 

- This data is often used to count and classify studies on topics such as product quality control, traffic, environmental pollution, or price comparison. 

<mark>Feb 2nd, 2025</mark> 

<mark>3</mark> 

# Example about Categorical Data 

- **Quality Control:** Based on quality standards, products on an assembly line can be classified into three categories: acceptable, repairable, or rejected. 

- **Traffic Study:** Researchers analyze commuter transportation choices, such as cars, motorcycles, buses, or bicycles, to understand traffic patterns and improve infrastructure. 

- **Pollution Study:** Scientists examine lake water samples to identify different algae species and count their occurrences, assessing environmental health. 

- **Drug Price Survey:** Consumer protection groups compare prescription drug prices across different city areas to identify price variations and ensure fair pricing. 

<mark>Feb 2nd, 2025</mark> 

<mark>4</mark> 

# Outline 

- Introduction to Categorical Data 

- **Inferences About a Population Proportion** 

   - Binomial experiment 

   - Estimating Parameter 𝜋 

   - Approximate normal distribution 

   - Confidence Interval for 𝜋 

   - Determine Sample Size 

- Inferences About the Difference Between Two Population Proportions 

<mark>Feb 2nd, 2025</mark> 

<mark>5</mark> 

# Binomial experiment 

- Each trial results in one of two outcomes: **success** (probability 𝜋) or **failure** (probability 1 −𝜋). 

- The probability distribution of the number of successes _y_ follows a **binomial distribution** : 



<!-- Start of picture text -->
- My yy<br>Py)= Gy ML<br><!-- End of picture text -->

<mark>Feb 2nd, 2025</mark> 

<mark>6</mark> 

# Estimating Parameter 𝜋 

- The point estimate of the binomial parameter 𝜋 is a value that we can intuitively choose. 

- In a random sample of _n_ elements from a population where the proportion of successes is 𝜋 , the best estimate of 𝜋 is **the sample proportion of successes** . 

- If _y_ represents the number of successes in _n_ trials, the sample proportion is calculated using the formula: 



<!-- Start of picture text -->
n~ _ J<br>r=<br>n<br><!-- End of picture text -->

~~rr~~ <mark>Feb 2nd, 2025 7</mark> 

<mark>Feb 2nd, 2025</mark> 

# Approximate Normal Distribution 

- Because _y_ has a mound-shaped distribution, which can be approximated by a normal distribution when the condition: 



<!-- Start of picture text -->
5 .<br>SS => _— ><br>n=G@.t—7m) (or, equivalently, nw = 5 and n(1 — 7) = 5)<br><!-- End of picture text -->

- The distribution of          can also be approximated by a tt =y/n normal distribution with mean and standard deviation as follows: 



<!-- Start of picture text -->
be = 7<br><!-- End of picture text -->

- The accuracy of the approximation increases as _n_ becomes larger. 

~~rr~~ <mark>Feb 2nd, 2025 8</mark> 

# Confidence Interval for 𝜋 

- We can use **normal approximation** to construct a _100(1−α)%_ confidence interval: 

> ~ — Y¥ is the sample proportion aT 7 is the critical value from the standard normal distribution. el 2 is the standard error. ne / (1-7) 

- This interval provides an estimate of π with a specified level of confidence 𝛼. 

~~rr~~ <mark>Feb 2nd, 2025 9</mark> 

<mark>Feb 2nd, 2025</mark> 

# When 𝜋 is close to 0 or 1 

- Another issue in estimating 𝜋 arises when it is close to 0 or 1. In these cases, the population proportion is often estimated as 0 or 1 unless the sample size is large. 

- However, these estimates are unrealistic because they suggest no successes or failures in the population. 

- Instead of using the previously mentioned formula for "𝜋, some adjustments have been proposed to prevent extreme estimates: 



<!-- Start of picture text -->
:<br>~<br>T<br>aaj. = +3) when y =0<br><!-- End of picture text -->



<!-- Start of picture text -->
a (n + 3)<br>T agi. = (n*3) when y =n<br><!-- End of picture text -->

~~rr~~ <mark>Feb 2nd, 2025 10</mark> 

<mark>Feb 2nd, 2025</mark> 

Confidence Interval when 𝜋 is close to 0 or 1 

- In those cases where _y = 0_ or _y = n_ , the standard approximation method is no longer valid for calculating confidence intervals for 𝜋. 

- Instead, confidence intervals derived from the binomial distribution can be used. 

- When y = 0, the confidence interval is: 



<!-- Start of picture text -->
(0,1 — (a/2)"")<br><!-- End of picture text -->

- When y = n, the confidence interval is: 



<!-- Start of picture text -->
((@/2)"/",1)<br><!-- End of picture text -->

<mark>Feb 2nd, 2025</mark> 

<mark>11</mark> 

# Determine Sample Size 

- The formula for determining the required sample size _n_ for a confidence interval of a population proportion _π_ is: 



<!-- Start of picture text -->
n= aig (1 — =<br>E?<br><!-- End of picture text -->

`o` is the critical value from the standard normal distribution for Za/2 the desired confidence level. `o` _π_ is the estimated population proportion, using _π=0.5_ gives the maximum sample size). 

`o` _E_ is the margin of error (half of the confidence interval width). 

~~rr~~ <mark>Feb 2nd, 2025 12</mark> 

<mark>Feb 2nd, 2025</mark> 

# Example 

- The publisher of a new book series has decided to conduct a more extensive study. They wanted to determine how many random readers they needed to survey to estimate the proportion of readers who would find the series appealing. 

- The publisher wants the estimator to be within ±0.03 of the true proportion with a 95% confidence level. 

<mark>Feb 2nd, 2025</mark> 

<mark>13</mark> 

# Solution 

- The required sample size to achieve this accuracy is given by the formula: 2a /2 -1(1 — 7) 

- The publisher wants the 95% confidence interval to be of the form: 7 + 0.03 E = 0.03 

- For a 95% confidence level, we have: 



<!-- Start of picture text -->
Za/2 = 20.025 — 1.96.<br><!-- End of picture text -->

~~cc~~ <mark>Feb 2nd, 2025 caaaaaaaaaaacacaaaaaaaasaaaaaaaa 14</mark> 

<mark>Feb 2nd, 2025</mark> 

Solution (cont.) 

- If no prior information about π is available, we use π=0.5 to obtain the maximum required sample size: 



<!-- Start of picture text -->
— (1:96)? 2 x 0.5 x (1-05)<br>ny _<br>(0.03)? _ 4 gz<br><!-- End of picture text -->

- Thus, **1,068 readers** need to be surveyed to ensure that the estimate of π is within ±0.03 of the actual value with 95% confidence. 

<mark>Feb 2nd, 2025</mark> 

<mark>15</mark> 

# Outline 

- Introduction to Categorical Data 

- Inferences About a Population Proportion 

- **Inferences About the Difference Between Two Population Proportions** 

   - Sampling Distribution Approximation 

   - Conditions for Normal Approximation 

   - Confidence Interval for _π1_ - _π2_ 

<mark>Feb 2nd, 2025</mark> 

<mark>16</mark> 

Inferences About the Difference Between Two Population Proportions 

- Many real-world problems involve the comparison of two binomial parameters. 

- • For example: 

   - social scientists may compare the proportion of women who use prenatal healthcare services in two communities with different socioeconomic backgrounds. 

   - A marketing director might want to compare public awareness of a newly launched product with a competitor’s. 

   - An education researcher may analyze the difference in graduation rates between students from urban and rural schools. 

   - A medical study could investigate whether the success rate of a new treatment differs between two patient groups. 

<mark>Feb 2nd, 2025</mark> 

<mark>17</mark> 

# Statistical Inference for Two Binomial Proportions 

- Statistical inferences about two binomial proportions are often expressed through their difference. 

- For comparisons of this type, we assume that independent random samples are drawn from two binomial populations with unknown parameters, denoted as _π1, π2._ 

- If there are _y1_ successes in a random sample of size _n1_ from population 1 and _y2_ successes in a random sample of size _n2_ from population 2, then the point estimates of _π1_ and _π2_ respectively: 



<!-- Start of picture text -->
Y1 ~ — v2<br>T= —_, 12 = —_<br>Ny ng<br><!-- End of picture text -->

<mark>18 ccc ccc ccc ccc cc cc</mark> 

~~LCCC~~ <mark>Feb 2nd, 2025 18 ccc ccc ccc ccc cc cc</mark> 

# Sampling Distribution Approximation 

- The sample proportion difference is used to construct confidence intervals or conduct hypothesis tests. 



<!-- Start of picture text -->
1 — Tr<br><!-- End of picture text -->

- The sampling distribution of          can be approximated by a Tt — To normal distribution with mean and standard error: 



<!-- Start of picture text -->
Lit. = T1 — M2<br><!-- End of picture text -->



<!-- Start of picture text -->
I m™(1 — 77) 1™2(1 — 712)<br>ng<br>1 2<br><!-- End of picture text -->

~~rr~~ <mark>Feb 2nd, 2025 19</mark> 

<mark>Feb 2nd, 2025</mark> 

# Conditions for Normal Approximation 

- This approximation is valid if the same conditions for a normal approximation to a single binomial distribution are applied to both binomial populations. 

|• Specifically, the normal approximation for<br>is appropriate if:<br>Tt — Tr|
|---|





<!-- Start of picture text -->
mm>5 and n(l—7)>5 for i=1,2.<br><!-- End of picture text -->

- Since _π1_ and _π2_ are unknown, validity is checked using: 



~~rr~~ <mark>Feb 2nd, 2025 20</mark> 

<mark>Feb 2nd, 2025</mark> 

# Confidence Interval for _π1_ - _π2_ 

- Estimated Standard Error: 



<!-- Start of picture text -->
Cine = |] mmi(lm(1-—7~ mm)i) + fta(lTo(1 —~ 72)2)<br>n n<br>1 2<br><!-- End of picture text -->

- The confidence interval takes the standard form: 



<!-- Start of picture text -->
M1 — Te £ 2/2 + OF, Fy<br><!-- End of picture text -->

~~rr~~ <mark>Feb 2nd, 2025 21</mark> 

<mark>Feb 2nd, 2025</mark> 

# Example 

- A publishing company is test-marketing a new book series in two cities: Ho Chi Minh and Ha Noi. The company's marketing strategy in Ho Chi Minh relies primarily on online advertisements, while in Ha Noi, it allocates an equal budget to a mix of online ads, newspaper promotions, bookstore events, and social media campaigns. Two months after launching the campaign, the company surveys to assess consumer awareness of the book series. 

- Calculate a 95% Confidence Interval for the city Difference in the proportions of all consumers who are aware of the book series. 

||**Ho Chi Minh**|**Ha Noi**|
|---|---|---|
|Number of respondents|600|530|
|Number aware of the book series|390|400|



<mark>Feb 2nd, 2025</mark> 

<mark>22</mark> 

# Solution 

- Since the awareness proportion is higher in Ha Noi, we define Ha Noi as Region 1. 



<!-- Start of picture text -->
Tm = 400 = 0.755, m2 = 300 = 0.650<br>530 600<br><!-- End of picture text -->

- The estimated standard error is: 



<!-- Start of picture text -->
bem = | (0.755) (0.245) . (0.650)(0.350) _ 9 gogs<br>530 600<br><!-- End of picture text -->

- For 95% confidence, we use: 



<!-- Start of picture text -->
Zo/2 = 1.96<br><!-- End of picture text -->

~~i~~ <mark>Feb 2nd, 2025 .cccccccccccccccccY 23</mark> 

Solution (cont.) 

- The 95% confidence interval is: 



<!-- Start of picture text -->
(0.755 — 0.650) + 1.96 x 0.0283<br>0.105 + 0.0555 = (0.049, 0.161)<br><!-- End of picture text -->

- This confidence interval indicates that between **4.9% and 16.1%,** more consumers in Ha Noi than in Ho Chi Minh are aware of the book series. 

~~rr~~ <mark>Feb 2nd, 2025 24</mark> 

<mark>Feb 2nd, 2025</mark> 

# Exercises 

1. A car dealership launching a new sales campaign has decided to conduct a more extensive study. They want to determine how many potential customers need to be randomly surveyed to estimate the proportion of buyers interested in purchasing a car from their dealership. The dealership wants the estimator to be within ±0.03 of the true proportion with a 95% confidence level. Suppose previous studies suggest that at least 80% of potential customers will likely consider buying a car from the dealership. 

<mark>Feb 2nd, 2025</mark> 

<mark>25</mark> 

# Exercises 

2. A company test-markets a new computer model in Ho Chi Minh City and Cao Lanh. 

      - In Ho Chi Minh City, the company’s advertising focuses mainly on social media and online marketing. 

   - In Cao Lanh, the company uses a mix of online ads, radio, and newspaper promotions. 

   - After two months, the company surveys potential customers to assess their awareness of the new computer model. 

||**Ho Chi Minh**|**Ha Noi**|
|---|---|---|
|Number of respondents|608|530|
|Number aware|392|413|



Calculate a 90% confidence interval for the city difference in the proportions of all consumers who are aware of the product.. 

<mark>Feb 2nd, 2025</mark> 

<mark>26</mark> 

# References 

[1] R. Lyman Ott, Micheal T. Longnecker. _An Introduction to Statistical Methods and Data Analysis_ . Cengage Learning, 2016. 

<mark>Feb 2nd, 2025</mark> 

<mark>27</mark> 

