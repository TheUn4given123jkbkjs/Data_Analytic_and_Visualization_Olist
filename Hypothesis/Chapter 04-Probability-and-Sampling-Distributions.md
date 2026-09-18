

Chapter 4: Probability and Sampling Distributions 

Lecturer: Ho Thi Linh, PHD 

###### Learning Objectives 



1 

###### Probability's Role in Statistical Inference 

Understand how probability provides the mathematical foundation for making reliable inferences from sample data to populations. 

###### Random Variables Classification 

2 

Distinguish between discrete and continuous random variables, recognising their unique properties and applications in statistical analysis. 

3 

###### Common Probability Distributions 

Identify and apply key distributions including Binomial and Normal, understanding when each is appropriate for different scenarios. 

4 

###### Random Sampling Importance 

Explain why random sampling is crucial for valid statistical inference and how it ensures representative data collection. 

###### Central Limit Theorem Applications 

Use the CLT to understand sampling distributions and make predictions about sample means from any population distribution. 

5 

###### Inferential Statistics and the Role of Probability What is Inferential Statistics? 



Inferential statistics involves using information gathered from a carefully selected sample4a subset of the larger population4to make educated statements and draw conclusions about the entire population of interest. 

###### The Critical Role of Probability 

Every inference we make must include a measure of reliability. We cannot simply state our conclusions; we must quantify how confident we are in them. Probability serves as our mathematical tool for measuring this reliability by quantifying the likelihood of different outcomes occurring. 

Without probability, our inferences would be mere guesses. With it, we can provide scientifically sound conclusions with measurable confidence levels. 

**Key Insight:** Probability transforms statistical inference from educated guessing into rigorous scientific methodology. 



### Understanding Random Variables 

**Definition:** A random variable  represents a quantitative measurement or observation obtained Y from an experiment or observational study. Its value is determined by chance and varies unpredictably from one observation to the next. 

Discrete Example 

   - Continuous Example 

- Y = Number of ticks found on a cow during veterinary inspection 

This takes countable values: 0, 1, 2, 3, ... ticks 

Y = Percentage of registered voters who cast ballots in an election This can take any value in the interval [0%, 100%] 

###### Research Case Study: Performance-Enhancing Drugs 



Consider a study investigating the prevalence of performance-enhancing drug use amongst professional athletes. This exemplifies the challenge of making population-level inferences from sample data. 

###### Sample Selection 

1 

Researchers select a representative sample of athletes from various sports and competition levels. 

###### Data Collection 

2 

Through confidential surveys and testing, data on drug use patterns is gathered. 

###### Population Inference 

3 

The sample proportion is used to estimate the true population proportion of drug users. 

The reliability of this inference4how confident we can be in our estimate4is determined entirely through probability theory. Without probability, we cannot quantify the uncertainty inherent in extending sample results to the entire population. 

### Exercise 1.1: Salmon Migration Study 



Marine biologists conduct a comprehensive study on the migration patterns and survival rates of tagged salmon populations in the Pacific Northwest. 

###### Population of Interest 

All salmon in the targeted river systems during the migration season4potentially hundreds of thousands of fish across multiple species and age groups. 

###### Study Sample 

A carefully selected subset of 2,500 salmon that are captured, tagged with electronic sensors, and released to track their migration routes and survival outcomes. 

Need for Reliability Measures 

Since we're using sample data to make claims about the entire salmon population, we must quantify our confidence. Probability allows us to state: "We are 95% confident that the true survival rate falls between X% and Y%." 

##### Finding the Probability of an Event 



###### Understanding Probability 

Probability serves as our measure of the likelihood that a specific event will occur. It provides a numerical value between 0 and 1 that quantifies uncertainty. 

###### The Relative Frequency Approach 

This fundamental approach to probability interpretation states that if we repeat an experiment many times under identical conditions, the relative frequency of any event will approach its true probability as the number of repetitions increases towards infinity. 



<!-- Start of picture text -->
probability<br><!-- End of picture text -->

This approach connects theoretical probability with real-world observations, making it particularly valuable for statistical applications. 

P(Event) = Number of times event occurs lim n³> n 

Probability Example: Water Quality Analysis Dataset: Daily Fluoride Readings 



Environmental scientists collect daily fluoride concentration measurements from a municipal water supply over several months to assess compliance with health standards. 

01 

02 

###### Define the Question 

###### Identify Relevant Data 

What is the probability that a randomly selected day shows fluoride concentration above 0.90 ppm? 

Examine the frequency distribution and identify all class intervals where fluoride levels exceed 0.90 ppm. 

03 

04 

Calculate Relative Frequencies 

###### Sum to Find Probability 

For each relevant class interval, compute the relative frequency (count ÷ total observations). 

Add all relative frequencies for classes above 0.90 ppm to obtain the final probability estimate. 

### Exercise 2.1: Rolling Two Dice 



###### Experimental Setup 

When rolling two fair dice simultaneously, there are 36 equally likely outcomes. Each specific combination (such as rolling a 3 on the first die and a 5 on the second) has a probability of 1/36. 

###### Event B: Sum Equals 4 

###### Event C: Sum f 4 

Find P(B) by identifying all ways to achieve a sum of 4: 

- (1,3): First die = 1, Second die = 3 

Find P(C) by enumerating all outcomes with sums of 2, 3, or 4: 

- (2,2): First die = 2, Second die = 2 

      - Sum = 2: (1,1) 1 way 

   - (3,1): First die = 3, Second die = 1 

- Therefore, P(B) = 3/36 = 1/12 

   - Sum = 3: (1,2), (2,1) 2 ways Sum = 4: (1,3), (2,2), (3,1) 3 ways 

- Therefore, P(C) = 6/36 = 1/6 

- Types of Random Variables **Type Definition Examples Discrete** Takes on a countable number of Number of heads in coin flips, number of distinct values, often integers customers served, exam scores (when graded as whole numbers) 

- **Continuous** Can take on infinitely many values Height measurements, reaction time, within any given interval temperature readings, blood pressure levels 

- Understanding this distinction is crucial because discrete and continuous random variables require different mathematical approaches for calculating probabilities. Discrete variables use probability mass functions, while continuous variables use probability density functions. 

- ~~<mark>—</mark>~~ 

##### Probability Distributions for Discrete Variables 



###### Essential Properties 

Example: Tossing Two Fair Coins 

For any discrete random variable , the probability Y distribution must satisfy two fundamental requirements: 

0 f P(y) f 1 

P(y) = 1 3 

Let  represent the number of heads observed:Y 

|**(Heads)**<br>y|P(y)|
|---|---|
|0|0.25|
|1|0.50|
|2|0.25|



###### Additivity Principle 

For mutually exclusive events (events that cannot occur simultaneously): 

Notice that all probabilities sum to 1.00, confirming this is a valid probability distribution. 

P(Y = 1 or Y = 2) = P(1) + P(2) 

### The Binomial Distribution 



When to Use the Binomial Distribution 

The binomial distribution applies to experiments involving repeated independent trials where each trial has exactly two possible outcomes (success or failure), and the probability of success remains constant across all trials. 

Parameters Mean Formula Standard Deviation Formula n: Number of independent trials ¿ = np conducted Ã = np(1 2 p) p: Probability of success on each The expected number of successes individual trial across all trials Measures the typical deviation from the expected number of successes 

###### Binomial Example: Turf Grass Germination 



An agricultural researcher plants 20 premium turf grass seeds, where each seed has an 85% probability of successful germination under optimal conditions. 

20 

0.85 

17 

Sample Size 

Success Rate 

Expected Mean 

Number of seeds planted (n) Probability of germination (p) ¿ = np = 20(0.85) = 17 seeds 

# 1.60 

Standard Deviation 

Ã = 20(0.85)(0.15) j 1.60 

**Critical Analysis:** If only 12 seeds germinate, this is (17 2 12)/1.60 = 3.1 standard deviations below the expected value4a highly unusual result that might indicate problems with seed quality or growing conditions. 

###### The Poisson Distribution 



###### Purpose and Applications 

The Poisson distribution models the number of events occurring within a fixed interval of time or space, given that these events happen at a known average rate and are independent of each other. 

###### Common applications include: 

- Number of phone calls per hour 

- Defects per manufactured item 

- Traffic accidents per month 

Radioactive decay events per secondMathematical Formula 



Where  represents the expected number of events in the given interval.¿ 

###### Practical Example 

In a laboratory study,  represents the number of mice captured in humane traps during a 24-hour period, with an Y average capture rate of ¿ = 2.3 mice per day. 

### Continuous Random Variables 



Fundamental Difference from Discrete Variables 

For continuous random variables, the probability of any single exact value is always zero: P(Y = a) = 0. This occurs because there are infinitely many possible values within any interval. 

###### Calculating Probabilities Over Intervals 

Instead of point probabilities, we calculate probabilities over intervals using integration: 

b P(a f Y f b) = f(y) dy +a 

Where f(y) is the probability density function (PDF). The PDF describes the relative likelihood of different values, and the area under the curve between any two points gives the probability for that interval. 

**Key Insight:** For continuous variables, we always ask "What's the probability that Y falls within this range?" rather than "What's the probability that Y equals this specific value?" 

#### The Normal Distribution 



###### Defining Characteristics 

The normal distribution is completely defined by two parameters: the mean  (which determines the centre) and the standard ¿ deviation  (which determines the spread). This distribution is perfectly symmetric and bell-shaped.Ã 

###### Symmetry Property 

###### Empirical Rule 

The distribution is perfectly symmetric about its mean, with Approximately 68% of values fall within 1 standard 50% of values above and 50% below .¿ deviation, 95% within 2 standard deviations, and 99.7% within 3 standard deviations of the mean. 

###### Standardisation with Z-Scores 

Any normal distribution can be converted to the standard normal distribution using the Z-score transformation: 

<u>y 2 ¿</u> Z = Ã 

This transformation allows us to use standard normal tables to find probabilities for any normal distribution. 

#### Applied Example: Ozone Pollution Analysis 



###### Problem Context 

Environmental scientists monitor daily ozone concentrations in an urban area. Historical data shows that ozone levels follow a normal distribution with mean ¿ = 70 parts per billion (ppb) and standard deviation Ã = 13 ppb. 

Calculating P(Y > 96) 

01 

02 

03 

Standardise the Value 

###### Interpret the Z-Score 

###### Find the Probability 

96 2 70 26 Z = = = 2.0 13 13 

A Z-score of 2.0 means the value 96 ppb Using standard normal tables or is exactly 2 standard deviations above statistical software: P(Z > 2.0) = 0.0228 or the mean. approximately 2.28%. 

**Environmental Significance:** There's only a 2.28% chance of observing ozone levels above 96 ppb on any given day, indicating such readings represent unusually high pollution events. 



#### Essential Python Libraries for Statistical Analysis 

###### scipy.stats 

###### NumPy 

###### **Statistical Inference** 

###### **Numerical Computing** 

Probability density functions (PDF) 

Random number generation 

Cumulative distribution functions (CDF) 

Array operations 

P-value calculations 

Mathematical functions 

Hypothesis testing tools 

Statistical computations 

###### statsmodels 

###### scikit-learn 

###### **Statistical Modelling** 

###### **Machine Learning** 

- Regression analysis 

Predictive modelling 

- Time series analysis 

Classification algorithms 

- Statistical inference 

Cross-validation 

Model diagnostics 

Feature selection 

## Why Do We Need Sampling? 



###### Population Size Constraints 

- 1 Real-world populations are often enormous4millions or billions of individuals. Studying every member would be impractical, time-consuming, and prohibitively expensive. 

###### Cost-Effective Inference 

- 2 Sampling enables us to draw reliable conclusions about entire populations using only a fraction of the data, dramatically reducing research costs whilst maintaining statistical validity. 

   - Design Considerations 

- 3 Successful sampling requires careful methodology to avoid selection bias, ensure representativeness, and maintain the integrity of statistical inference. 

### Simple Random Sampling 



**Definition:** Each possible sample of size n has an equal probability of being selected from the population. 

###### **Key Benefits** 

###### **Implementation** 

**Ensures Valid Inference:** Creates unbiased estimates of population parameters 

Simple random sampling can be achieved through various methods: 

**Statistical Foundation:** Provides the theoretical basis for confidence intervals and hypothesis tests 

**Eliminates Bias:** Prevents systematic errors from convenience or judgement sampling 

- Random number tables 

- Computer-generated random numbers Physical randomisation devices 

## Example: Selecting Cities 



Consider selecting 2 cities from the 10 largest U.S. cities. This demonstrates the fundamental principles of combinatorial probability in sampling. 

1 

2 

3 

Calculate Total Combinations 

The number of ways to choose 2 cities from 10: 

10! = = 45 ( 210) 2!(10 2 2)! 

Determine Selection Probability 

Each specific pair has equal probability: 

P(any specific pair) = 1 j 0.022 45 

###### Verify Randomness 

This equal probability ensures that our sample selection process is truly random and unbiased. 

###### Sampling Methods in Practice 



Real-world sampling extends beyond simple random sampling to address practical constraints and improve efficiency. Different contexts require different approaches. 

1 

2 

3 

Survey Research 

Experimental Design 

Python Implementation 

**Stratified Sampling:** Divide population into strata, sample within each 

**Random Assignment:** Participants randomly assigned to treatment groups 

# Pandas sampling df.sample(n=100, random_state=42) 

**Cluster Sampling:** Sample groups (clusters) rather than individuals 

**Systematic Sampling:** Select every kth member from a list 

**Blocking:** Group similar units before 

randomisation 

**Matched Pairs:** Pair similar subjects, randomise within pairs 

# NumPy choice np.random.choice(population, size=100, replace=False) 

### Exercise 4.2: Practical Sampling 



A membership organisation with 45,000 members uses a computer system to randomly select 1,250 member IDs for a survey. This scenario illustrates modern sampling techniques. 

###### **Scenario Analysis** 

###### **Questions to Consider** 

The organisation's approach demonstrates several key principles: 

   1. **Identify the sampling method:** What type of sampling is being used? 

- **Population Size:** 45,000 total members **Sample Size:** 1,250 selected members **Selection Method:** Computer-generated random selection 

   2. **Bias reduction:** How does this method reduce potential bias compared to other approaches? 

   3. **Representativeness:** What assumptions must hold for valid inference? 

- **Sampling Fraction:** Approximately 2.8% of the population 

###### Understanding Sampling Distributions 



Sampling distributions form the foundation of statistical inference, connecting population parameters with sample statistics through probability theory. 

###### **Population Parameters** 

Fixed, unknown values: 

- 1 ¿ (population mean) 

   - Ã (population standard deviation) 

p (population proportion) 

###### **Sample Statistics** 

Random variables from samples: 

- 2 yË (sample mean) 

   - s (sample standard deviation) 

   - p^ (sample proportion) 

###### **Sampling Distribution** 

3 

The probability distribution of a statistic across all possible samples of size n. 

## Defining the Sampling Distribution 



**Sampling Distribution:** The probability distribution of a statistic obtained from repeated sampling of a population. 

This concept is fundamental to statistical inference because it allows us to: 



<!-- Start of picture text -->
Dx<br><!-- End of picture text -->



<!-- Start of picture text -->
«<br><!-- End of picture text -->



<!-- Start of picture text -->
a<br><!-- End of picture text -->

Measure Accuracy Construct Confidence Conduct Hypothesis Tests Intervals Quantify how close our sample Evaluate whether observed sample statistics are likely to be to the true Create ranges of plausible values for results provide evidence for or population parameters. population parameters based on against specific claims about sample data. populations. 

#### Example: Small Population Analysis 



Consider a small population to illustrate sampling distribution concepts clearly. This concrete example helps visualise how sampling distributions emerge from repeated sampling. 

###### **Population Details** 

###### **Sample Means** 

**Population:** {2, 3, 4, 5, 6, 7, 8, 9, 10, 11} 

Examples of  values:yË 

**Population Mean:** ¿ = 6.5 

**Sample Size:** n = 2 **Total Possible Samples:** ( 210) = 45 

###### **Key Insight** 

{2,3}: yË = 2.5 {5,7}: yË = 6.0 

- {9,11}: yË = 10.0 

All 45 values form a distribution that describes the behaviour of .Y<sup>Ë</sup> 

The distribution of all 45 possible sample means  creates yË the sampling distribution of , which centres perfectly at Y<sup>Ë</sup> the population mean of 6.5. 

## Properties of the Sample Mean 



The sample mean  has predictable statistical properties that form the foundation for Y<sup>Ë</sup> statistical inference. 

###### Expected Value 

¿Y<sup>Ë</sup> = ¿ 

**Unbiased Estimator:** The expected value of the sample mean equals the population mean, regardless of sample size. 



<!-- Start of picture text -->
Standard Error<br>Ã<br>ÃY Ë =<br>n<br><!-- End of picture text -->

**Precision Increases:** As sample size increases, the standard error decreases, making estimates more precise. 

###### Distribution Shape 

**Normal Population:** If the ~~population follows a normal~~ distribution, then  is exactly Y<sup>Ë</sup> normally distributed for any sample size. 

These properties hold true regardless of the underlying population distribution, making the sample mean a powerful tool for statistical inference. 

### Central Limit Theorem 



### The Magic of Large Samples 

**Central Limit Theorem:** When n is sufficiently large, the sampling distribution of  Y<sup>Ë</sup> approaches a normal distribution, regardless of the population's shape. 

¿, <u>n</u> Ã ~~)~~ 

Y<sup>Ë</sup> > N ( 

Universal Application Works for any population distribution 4skewed, uniform, bimodal, or unknown shape. 

###### Sample Size Guidelines 

Generally effective when n g 30, though smaller samples may suffice for symmetric populations. 

###### Practical Power 

Enables normal-based inference procedures even when population distributions are unknown. 

Example: Penny Ages Distribution This simulation demonstrates the Central Limit Theorem using penny ages, which typically follow a right-skewed distribution with ¿ j 13.47 years. 15 10 5 0 n = 1 n = 5 n = 25 **Distribution Evolution Key Observations n = 1:** Maintains original right skew Notice how the mean remains consistent around 13.47 **n = 5:** Shows reduced skewness across all sample sizes, whilst the shape becomes increasingly normal as sample size increases. **n = 25:** Approaches normal distribution ~~<mark>-</mark>~~ 

###### Sample Size Determination 



Determining appropriate sample sizes requires balancing statistical precision with practical constraints. This example shows how to calculate minimum sample sizes for specific probability requirements. 

###### **Problem Setup** 

###### **Solution Process** 

**Objective:** Ensure P(Y<sup>Ë</sup> < 150) f 0.01 Using the standard normal distribution: 

**Known Parameters:** 

Population mean: ¿ = 160 Population standard deviation: Ã = 20 Required probability: f 0.01 

Solving for n: 

150 2 160 ~~= 22.326~~ <u>n</u> 20/ 

n j 22 

**Conclusion:** At least 22 measurements are needed to meet the specified probability requirement. 

**Practical Note:** Always round up to the next whole number when determining sample sizes, as you cannot collect a fraction of an observation. 

## Exercise 5.4: CLT Simulation 



This simulation exercise reinforces Central Limit Theorem concepts using a normal population with specified parameters. Students can verify theoretical predictions through computational analysis. 

###### **Simulation Parameters** 

###### **Tasks to Complete** 

- **Population:** Normal distribution 

   1. State the expected mean of Y<sup>Ë</sup> 

- **Mean:** ¿ = 43 

   2. Calculate the expected standard deviation of Y<sup>Ë</sup> 

- **Standard deviation:** Ã = 7 

   3. Explain the relationship to CLT 

- **Sample size:** n = 16 

   4. Optional: Run simulation in R to verify results 

- **Replications:** 10,000 samples 

**Expected Results:** The simulation should confirm that ¿Y<sup>Ë</sup> = 43 and ÃY<sup>Ë</sup> = 7/ 16 = 1.75, with a perfectly normal distribution since the population is already normal. 

