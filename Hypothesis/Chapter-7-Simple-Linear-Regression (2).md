# **Chapter 7: Simple Linear Regression (SLR)** 

**An Essential Tool in Statistical Methods and Data Analysis** 

**Key Goal:** Understand the fundamental model, parameter estimation, and interpretation of SLR. 

Instructor: Ho Thi Linh, PHD. 

## Introduction to Regression Analysis 

What is Regression Analysis? 

Regression analysis is a powerful statistical technique used to model the functional relationship between a response variable and one or more explanatory variables. It serves as the foundation for understanding how variables interact and influence one another in real-world scenarios. 

###### Simple Linear Regression (SLR) 

SLR uses a **single independent variable (x)** to predict a dependent variable (y), assuming a linear relationship between them. This makes it an ideal starting point for learning predictive modeling. 

###### Description 

###### Estimation/Prediction 

###### Variable Identification 

Provides a functional relationship describing the main features of the dataset 

Estimates response variable values for unseen explanatory variable values 

Determines which explanatory variables affect the response, leading to cost savings and process focus 

## The SLR Model and Assumptions 

The Simple Linear Regression Model 

The basic prediction model assumes y is a linear function of x, plus an error term: 

_y_ = _³_ 0 + _³_ 1 _x_ + _÷_ 

###### Model Components 

###### Formal Assumptions 

- **y:** Dependent/Response variable 

   1. **Linearity:** True relation is linear, E(÷)=0 

- **x:** Independent/Explanatory variable 

   2. **Homoscedasticity:** Constant variance Var(÷)= Ã ² 

- ³ **:** True population intercept 

   3. **Independence:** Errors are independent 

- ³ **¡:** True population slope 

   4. **Normality:** Errors are normally distributed 

- ÷ **:** Random error term 

These assumptions are critical for valid statistical inference and must be verified during model diagnostics. 

#### Parameter Estimation: The Least-Squares Method 

We estimate the population parameters ( ³ and ³ ¡) using sample data to find the best prediction line: _y_ ^ = _³_<sup>^</sup> 0 + _³_<sup>^</sup> 1 _x_ 

###### The Criterion Calculate Estimates 

###### Best Fit Line 

Minimize the Total Squared Prediction Error Apply calculus to find optimal parameter Obtain the line that minimizes prediction (Sum of Squared Residuals) values errors 

###### The Objective Function 



###### Estimated Slope 

###### Estimated Intercept 



Where Sxx is the sum of squared x deviations 

Where Sxy is the sum of x deviations times y deviations 

##### Measuring Variability and Fit 

###### 1. Estimated Error Variance (Ã�²±) 

Measures the variance around the regression line (mean squared prediction error): 



**Degrees of Freedom:** n22 (two d.f. lost by estimating ³ and ³ ¡) 

###### 2. Residual Standard Deviation (s±) 

The square root of the estimated error variance, interpreted using the **Empirical Rule:** 

About **95% of prediction errors** will fall within ±2s± of the regression line. 

###### 3. Coefficient of Determination (r²) 

Measures the proportionate reduction in error achieved by using the regression line instead of the mean 3 for prediction: 



**Range:** 0 to 1, where higher values indicate better fit 

###### Example: Road Resurfacing Project (Part I) 

###### **Scenario** 

###### **Data Table** 

Predicting the cost of road resurfacing projects (y) based on **Cost y ($1,000s) Mileage x (miles)** the mileage resurfaced (x). 6.0 1.0 Summary Statistics (n=5) x� = 4.0 miles 14.0 3.0 3 = $14,000 10.0 4.0 Sxx = 20.0 Sxy = 60.0 14.0 5.0 26.0 7.0 01 02 03 Calculate ³<sup>�</sup> ¡ Calculate ³<sup>�</sup> Prediction Equation _³_<sup>^</sup> 1 = 60.0 = 3.0 _³_<sup>^</sup> 0 = 14.0 2 3.0(4.0) = 2.0 _y_ ^ = 2.0 + 3.0 _x_ 20.0 

**Interpretation:** For each additional mile, the predicted cost increases by $3,000. The intercept ($2,000) represents the fixed cost of starting the project. 

### Example: Road Resurfacing Project (Part II) 

Prediction Equation 

_y_ ^ = 2.0 + 3.0 _x_ 

###### Measuring Model Fit 

###### Correlation Coefficient 

**Given:** 

SS(Total) = Syy = 224 



<!-- Start of picture text -->
S 60.0<br>xy<br>r = = = 0.896<br>SxxSyy 20.0 × 224<br><!-- End of picture text -->

SS(Error) = £ (yi - wi)² = 44 

Since r is **positive** , y increases as x increases. 

Coefficient of Determination: 

Note: r² j (0.896)² j 0.803 

224 2 44 2 _r_ = = 0.804 224 

**Interpretation:** Use of the regression model reduces the squared prediction error by **80.4%** , suggesting a strong linear relationship. 

###### Inference on the Slope ( ³ ¡) 

We use the sample slope (³<sup>�</sup> ¡) to make inferences about the true population slope ( ³ ¡), which tells us whether x has predictive value for y. Standard Error of ³<sup>�</sup> ¡ 

_se s´_<sup>^</sup> 1 = _Sxx_ 

Hypothesis Testing 

###### Confidence Interval for ³ ¡ 

**Hypotheses:** 

H : ³ ¡ = 0 (no linear relationship) H°: ³ ¡ b 0 (linear relationship exists) 



This interval quantifies the uncertainty in the slope estimate and provides a range of plausible values for the true slope parameter. 

**Test Statistic (t-distribution):** 

_<u>´</u>_<sup>^</sup> 1 2 0 _t_ = _s´_<sup>^</sup> 1 

with df = n 2 2 

**Important Note:** The overall F-test for the model (F = MS(Regression)/MS(Error)) yields the exact same conclusion as the two-sided t-test on the slope in SLR, since F = t². 

#### Prediction and Prediction Intervals 

Regression is often used to predict a new y-value (wn+1) for a given new x-value (xn+1). Understanding the difference between prediction and confidence intervals is crucial. 

Prediction Interval (PI) 

###### Confidence Interval (CI) 

Predicts an **individual y value** for xn+1 

This interval is **wider** because it accounts for both sampling error (estimating ³ , ³ ¡) and inherent random error (÷) 

Estimates the **mean (average) y value** E(y) for all cases with xn+1 Narrower than PI because it only accounts for sampling error in parameter estimation 

###### General Form 

**Estimate ± t** ³ **/2 × (Standard Error)** 

1 <u>(</u> _xn_ +1 2 _x_ Ë)<sup>2</sup> _y_ ^ _n_ +1 ± _t³_ /2 ç<sup>_s_</sup> _e_ 1 + + _n Sxx_ 

Note the term **+1** inside the square root for the Prediction Interval, which is omitted for the Confidence Interval. 

**Extrapolation Warning:** Both intervals widen significantly as xn+1 moves farther from x� (the center of the data), reflecting increased risk and uncertainty in predictions outside the observed data range. 

###### Python Tools for SLR 

Python is a crucial language for data science, utilizing specialized libraries for statistical modeling. Understanding these tools helps you implement SLR effectively in practice. 

###### **Essential Libraries for Statistical Modeling** 

|**Library**|**Primary Function**|**Relevance to SLR**|
|---|---|---|
|**statsmodels**|Classical (Frequentist) Statistics,<br>Econometrics|Estimating Linear Models (OLS, GLM), provides<br>detailed statistical inference (p-values, standard<br>errors). Integrates with Patsy for formula<br>specification (e.g., 'y ~ x0 + x1')|
|**NumPy**|Scientific Computing, Multidimensional<br>Arrays|Provides underlying linear algebra functions, such as<br>numpy.linalg.lstsq (Least Squares solution)|
|**scikit-learn**|General-Purpose Machine Learning|Focuses on prediction; useful for techniques like<br>Lasso and Ridge regression, extensions of linear<br>regression|
|**Seaborn/Matplotlib**|Visualization|Essential for visualizing data via scatter plots<br>(regplot) and assessing model assumptions|
|Implementation|Visualization|Diagnostics|
|statsmodels and scikit-lea|rn provide<br>Seaborn's regplot creates sca|tter plots<br>All libraries offer tools for model|
|simple APIs for fitting line<br>models|ar regression<br>with fitted regression lines<br>automatically|validation and assumption checking|



