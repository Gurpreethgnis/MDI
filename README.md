# MDI
Missing Data Imputation Python Library (version 0.1)

This repository offers techniques for handling missing data and encoding categorical data such that it is appropriate to neural network classifiers and other tasks. We provide six different imputation strategies and include examples using the Adult dataset. Will soon include data, python and latex code for a wip paper on MDI, Random Forest and Neural Networks.

## Techniques for handling categorical missing data
We categorize proposed imputation methods into six groups listed below:

**Case substitution**
One observation with missing data is replaced with another non-sampled obser- vation.

**Summary statistic**
Replace the missing data with the mean, median, or mode of the feature vec- tor. Using a numerical approach directly is not appropriate for nonordinal categorical data.

**One-hot**
Create a binary variable to indicate whether or not a specific feature is missing.

**Hot deck and cold deck**
Compute the K-Nearest Neighbors of the observation with missing data and assign the mode of the K-neighbors to the missing data. algorithm.

**Prediction Model**
Train a prediction model (e.g., random forests) to predict the missing value.

**Factor analysis**
Perform factor analysis (e.g., principal component analysis (PCA)) on the design matrix, project the design matrix onto the first N eigenvectors and replace the missing values by the values that might be given by the projected design matrix.

## Adult Dataset example ##
The figure below shows frequency of job category in the Adult dataset before
and after the imputation techniques above were used.  
Code can be found [here](example_adult.py)

![Adult dataset Imputation](adult_hist.png)

## Congresssional voting records dataset example ##
Code can be found [here](example_votes.py)

![Congresssional voting records dataset imputation](votes_hist.png)

## TO DO
** Modify plot_results to include hyperparameters tried **

** Modify predict_with_best_model to print best model params R**

**Compare with classification using one-hot data R**

**Artificially perturb the data to generate missing observations R DONE** 

**Compare with random forest classification- J**

**Impute with Logistic Regression, Random Forest and SVM - R DONE** 

**Compute error bars for prediction accuracy - J**

**Use Non-Negative Matrix Factorization instead of PCA - R**

**Add python file that has a fit and predict function for the best models - R DONE**
