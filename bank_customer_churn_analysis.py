# Our Project Description
As commonly understood, acquiring a new customer incurs higher costs compared to retaining an existing one.
Hence, it is beneficial for banks to understand the reasons that prompt a customer to terminate their association with the institution.
By preventing customer churn, companies can design loyalty programs and retention initiatives aimed at retaining a maximum number of customers.

- Analysis of Bank customers information to try to predict the profile of people that will churn
- For the students, it allows us to better understand the banking system and customer information
- This is a good usecase to practice our skills learned in class and try to have an impact on customer behavior

Content:
* RowNumber — corresponds to the record (row) number and has no effect on the output. Contains random values and has no effect on customer leaving the bank.
* Surname — the surname of a customer has no impact on their decision to leave the bank.
* CreditScore — can have an effect on customer churn, since a customer with a higher credit score is less likely to leave the bank.
* Geography — a customer’s location can affect their decision to leave the bank.
* Gender — it’s interesting to explore whether gender plays a role in a customer leaving the bank
* Age — this is certainly relevant, since older customers are less likely to leave their bank than younger ones.
* Tenure — refers to the number of years that the customer has been a client of the bank. Normally, older clients are more loyal and less likely to leave a bank
* Balance — also a very good indicator of customer churn, as people with a higher balance in their accounts are less likely to leave the bank compared to those with lower balances.
* NumOfProducts — refers to the number of products that a customer has purchased through the bank.
* HasCrCard — denotes whether or not a customer has a credit card. This column is also relevant, since people with a credit card are less likely to leave the bank.
* IsActiveMember — active customers are less likely to leave the bank
* EstimatedSalary — as with balance, people with lower salaries are more likely to leave the bank compared to those with higher salaries.
* Exited — whether or not the customer left the bank.

# Visualization of the Dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from google.colab import drive
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf
import sklearn.metrics
import sklearn.model_selection

pip install pandas-profiling

import pandas_profiling

df = pd.read_csv('https://drive.google.com/uc?export=download&id=1Gl_3o47h0qf3gKMKtHxQzGCB7KCx-E2a')

df.head()

display(df)

df.describe()

# Clean the data - We will remove 3 columns as they don't bring value to our dataset
df_clean=df.copy().drop(columns=['RowNumber','CustomerId','Surname'])
df_clean

# How many unique values are in each Columns of Data ?
for i in df_clean.columns:
    if len(df_clean[i].unique())<6:
      print(F'{i}:',len(df_clean[i].unique()),'Values:',df_clean[i].unique())
    else:
      print(F'{i}:',len(df_clean[i].unique()))

# Quick Analysis - This is a lot of info directly computed. Maybe better to use functions to do it manually?
pandas_profiling.ProfileReport(df_clean, title="Pandas Profiling Report", explorative=True)

# Heatmap to look for correlation
plt.figure(figsize=(10,7)),
sns.heatmap(df_clean.corr(),vmin=0, vmax=1,annot=True);

df_clean.describe()

"""# Churn Analysis

## Our Goal with this data

We will be interested in predicting the churn of the customer, namely the column ``Exited`` based on the others.

In the class we present OLS method and logistic regression to predict 2 different type of variable (continue and discontinue). As ``Exited`` is a binary variable, we'll use the logistic regression to fit it.

##Splitting into Test and Training Data

We will be fitting a model to this data, and we will want to know how good a fit that model is, so let's split the data into test and training data.
To do this, we'll use our friend from the previous notebook, the sklearn.model_selection.train_test_split function.

We will be using the [``statsmodels.glm``](https://www.statsmodels.org/stable/generated/statsmodels.genmod.generalized_linear_model.GLM.html) (generalized linear model) function for this example, because its ``summary`` function allows us to examine the impact of individual parameters.

We could have equivalently used the [``statsmodels.logit``](https://www.statsmodels.org/devel/generated/statsmodels.discrete.discrete_model.Logit.html) function, which does binary logistic regression. If we had multiple classes that we wanted to predict, we could use the [``statsmodels.MNlogit``](https://www.statsmodels.org/dev/generated/statsmodels.discrete.discrete_model.MNLogit.html) function.
"""

df_train, df_test = sklearn.model_selection.train_test_split(
    df_clean, test_size=0.5, shuffle=True, random_state=7)

print('Training Data:')
display(df_train.head())
print('')
print('Test Data:')
display(df_test.head())

display(df_train['Exited'].head())

"""## Computing the fit"""

logistic_formula = ('Exited ~ Age + Balance + IsActiveMember')
# We took the variable that showed the highest correlation on the heating map but didn't take into account Credit score for instance. We will take it into account in a second iteration
logreg_fit = smf.glm(formula=logistic_formula, data=df_train, family=sm.families.Binomial()).fit()
display(logreg_fit.summary())
# We could alternatively use the logit function
# logreg_fit = smf.logit(formula=logistic_formula, data=df_train).fit()

"""We see that all P values for the taken attributes are very low, showing that they are significant for the fit.

## Making predictions

Let's take a look at the values predicted by this model.
"""

test_prediction = logreg_fit.predict(df_test)

print('Predicted test values')
display(test_prediction)
print('')
print('Actual test values:')
display(df_test['Exited'])

"""We can notice that for the line 1977, the prediction is far from the actual result, so we can see that it has some trouble predicting actuall churn sometimes.

Notice that the output is not ``Yes`` (1) or ``No`` (0), but rather a probability of ``Yes`` (1).

If we want to interpret these values as either ``Yes`` (1) or ``No``(0) then we'll need to select a cutoff. Here we show the result of using a cutoff of 0.5 (so, 50% probability).
"""

(test_prediction > 0.5).head()

"""Using a 0.5 cutoff, we can see that we have 1 error displayed on the head

## Evaluating our fit

The simplest evaluation we can do is to compute the fraction of elements that we compute accurately.
"""

test_accurately_predicted = df_test['Exited'] == (test_prediction > 0.5)
test_accurately_predicted.head()

np.sum(test_accurately_predicted) / len(df_test)

"""This can be interpreted as the raw accuracy of our classifier: 80.64%

##Second Iteration

Let's try again but this time we use all attributes to see if the result gets better
"""

logistic_formula_2 = ('Exited ~ Age + Balance + IsActiveMember + CreditScore + Geography + Gender + Tenure + NumOfProducts + HasCrCard + EstimatedSalary')
logreg_fit_2 = smf.glm(formula=logistic_formula_2, data=df_train, family=sm.families.Binomial()).fit()
display(logreg_fit_2.summary())
# We could alternatively use the logit function
# logreg_fit = smf.logit(formula=logistic_formula, data=df_train).fit()

"""We can see that other values appears as significant, namely geography and gender."""

test_prediction_2 = logreg_fit_2.predict(df_test)

print('Predicted test values')
display(test_prediction_2)
print('')
print('Actual test values:')
display(df_test['Exited'])

test_accurately_predicted_2 = df_test['Exited'] == (test_prediction_2 > 0.5)
test_accurately_predicted_2.head()

np.sum(test_accurately_predicted_2) / len(df_test)

"""# We see that we won almost 1% of accuracy!

##Third Iteration
"""

logistic_formula_3 = ('Exited ~ Age + Balance + IsActiveMember + Geography + Gender')
logreg_fit_3 = smf.glm(formula=logistic_formula_3, data=df_train, family=sm.families.Binomial()).fit()
display(logreg_fit_3.summary())
# This time we used the significant variables in order to improve the accuracy

test_prediction_3 = logreg_fit_3.predict(df_test)

print('Predicted test values')
display(test_prediction_3)
print('')
print('Actual test values:')
display(df_test['Exited'])

test_accurately_predicted_3 = df_test['Exited'] == (test_prediction_3 > 0.5)
test_accurately_predicted_3.head()

np.sum(test_accurately_predicted_3) / len(df_test)

"""We once again improved our model a little bit by chosing the right attributes.

We must be carefull, we could improve the model again by changing and finding the right cutoff.

## Computing Precision and Recall

Let's compute the precision and recall of our model using a cutoff of 0.5. To do this, let's compute the number of true positives, false positives, and false negatives.
"""

# True positives have Exited==1 (True) and we predicted True.
n_true_positives  = np.sum(
    (df_test['Exited'] == 1)  & (test_prediction_3 > 0.5))
# False positives have Exited==0 (False) but we predicted True
n_false_positives = np.sum(
    (df_test['Exited'] == 0) & (test_prediction_3 > 0.5))
# False negatives have Exited==1 (True) but we predicted False
n_false_negatives = np.sum(
    (df_test['Exited'] == 0) & (test_prediction_3 <= 0.5))

"""Using this we can apply our formula for precision and recall.

"""

precision = n_true_positives / (n_true_positives + n_false_positives)
print('Precision: ' + str(precision))
recall    = n_true_positives / (n_true_positives + n_false_negatives)
print('Recall: ' + str(recall))

"""Our model has a precision of 0.58 - in other words, when it predicts someone will exit the bank, it is correct 58% of the times.

Our model has a recall of 0.05 - in other words, it correctly identifies 5% of all exits.

We can see that the model is pretty poor in terms of performance. Let's evaluate the model with a different method to validate our result.

### Evaluating using ``classification_report``

This can get very tedious to compute. Fortunately the ``sklearn`` library has many helpful functions for evaluating classifiers, including the [``sklearn.metrics.classification_report``](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html) function.

Let's take a look at its output. This function returns a dictionary for every class -- we happen to be doing binary classification here, so we just care about the ``Exited`` class, so just print the results for the `['1']` class.
"""

display(sklearn.metrics.classification_report(
    df_test['Exited'], test_prediction_3 > 0.5, output_dict=1)['1'])

"""We can see that we have the same precision as before. However the recall is different.

Let's try to enhance the model bby changing the cutoff, by focusing on the recall

### Adjusting cutoffs for sensitivity or specificity

Sensitivity is the ability of a test to correctly identify those who default(true positive rate), whereas test specificity is the ability of the test to correctly identify those who don't default (true negative rate).

Suppose we are particularly concerned with the recall. We could decrease the cutoff to get a higher recall (at the expense of lower precision).
"""

display(sklearn.metrics.classification_report(
    df_test['Exited'], test_prediction_3 > 0.25, output_dict=1)['1'])

"""We can see that with a cutoff of 0.25, the recall is much better

### Evaluation using ``confusion_matrix``

A confusion matrix can be helpful to see where classifications are accurate. The function [``sklearn.metrics.confusion_matrix``](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html) will compute this for you

Let's create a prettier design that the default one
"""

def DrawConfusionMatrix(confusion_matrix):
  # Taken from https://gist.github.com/shaypal5/94c53d765083101efc0240d776a23823
  class_names = ['Didnt Exited', 'Exited']
  df_cm = pd.DataFrame(confusion_matrix, index=class_names, columns=class_names)
  fig = plt.figure(figsize=(4, 3))
  heatmap = sns.heatmap(df_cm, annot=True, fmt='d')
  heatmap.yaxis.set_ticklabels(heatmap.yaxis.get_ticklabels(), rotation=0, ha='right')
  heatmap.xaxis.set_ticklabels(heatmap.xaxis.get_ticklabels(), ha='center')
  plt.ylabel('True label')
  plt.xlabel('Predicted label')
  plt.title('Confusion Matrix')
  plt.show()

Matrix_50 = sklearn.metrics.confusion_matrix(df_test['Exited'], test_prediction_3 > 0.5)
DrawConfusionMatrix(Matrix_50)

"""This requires some interpretation.

The top row is how the true ``No`` records were classified. The top-left entry is how many ``No`` records were correctly classified as ``No``, and the top-right is how many ``No`` records were incorrectly classified as ``Yes``.

The bottom row is for the true ``Yes`` records. The bottom-right is how many ``Yes`` entries were correctly classified as ``Yes``, and the bottom-left is how many ``Yes`` records were incorrectly classified as ``No``.

This time we tried again with a 0.25 cutoff
"""

Matrix_25 = sklearn.metrics.confusion_matrix(df_test['Exited'], test_prediction_3 > 0.25)
DrawConfusionMatrix(Matrix_25)

"""### ROC Curve

The receiver operating characteristic curve, which plots true positive rate as a function of false positive rate, is a helpful tool for evaluating a classifier.

The function [``sklearn.metrics.roc_curve``](https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html) calculates everything that we need to know about this.

This function returns three arrays.
* The ``thresholds`` result will be a sequence of cutoff values.
* The ``tpr`` will be the true positive rate (AKA the recall of the ``Yes`` category AKA the sensitivity of the model) at each of these thresholds.
* The ``fpr`` will be the false positive rate (AKA 1 minus the recall of the ``No`` category) at each of these thresholds.
"""

fpr, tpr, thresholds = sklearn.metrics.roc_curve(df_test['Exited'], test_prediction_3)

thresholds

"""This can be used to visualize the true positive and false positive rate as a function of threshold."""

plt.plot(thresholds, fpr, label='False Positive Rate')
plt.plot(thresholds, tpr, label='True Positive Rate')
plt.xlabel('Threshold')
plt.ylabel('Accuracy')
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.legend()
plt.show()

"""Or, we can plot true positive rate as a function of false positive rate, to get the ROC curve."""

plt.plot(fpr, tpr)
plt.xlabel('False positive rate')
plt.ylabel('True positive rate')
plt.show()

"""The area under the ROC curve (the AUC of the ROC) can be computed using numerical integration. The function [``numpy.trapz``](https://docs.scipy.org/doc/numpy/reference/generated/numpy.trapz.html) computes numerical integrals using the [trapeziodal rule](https://en.wikipedia.org/wiki/Trapezoidal_rule).




"""

auc = np.trapz(y=tpr, x=fpr)
display(auc)

"""###Let's optimize the cutoff with the Youden's index method."""

tnr = 1 - fpr

youdens_curve = tpr + tnr - 1
youdens_index_argmax = youdens_curve.argmax()
youdens_index_cutoff = thresholds[youdens_index_argmax]
print('Maximum Youden\'s Index: %f' % youdens_curve[youdens_index_argmax])
print('                Cutoff: %f' % youdens_index_cutoff)

plt.plot(thresholds, tpr, label='TPR')
plt.plot(thresholds, tnr, label='TNR')
plt.plot(thresholds, youdens_curve, label='Youden\'s Index Curve')
plt.scatter(thresholds[youdens_index_argmax], tpr[youdens_index_argmax])
plt.scatter(thresholds[youdens_index_argmax], tnr[youdens_index_argmax])
plt.scatter(thresholds[youdens_index_argmax], youdens_curve[youdens_index_argmax])
plt.xlabel('Cutoff')
plt.legend()
plt.xlim(0, 1)
plt.show()

plt.plot(thresholds, youdens_curve)
plt.xlabel('Cutoff')
plt.ylabel('YoudensIndex')
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.show()

plt.plot(fpr, fpr, label='FPR(1-Specificity)')
plt.plot(fpr, tpr, label='TPR(Sensitivity)')
plt.plot(
    [youdens_index_cutoff,youdens_index_cutoff],
    [youdens_index_cutoff,youdens_index_cutoff + youdens_curve[youdens_index_argmax]],
    label='Youdens\' Index')
plt.xlabel('False positive rate')
plt.legend()
plt.show()

display(sklearn.metrics.classification_report(
    df_test['Exited'], test_prediction_3 > 0.1985, output_dict=1)['1'])

"""We can see that we have greatly improved our recall

# To go further

***Logistic Regression***
"""

df_reg=df.copy().drop(columns=['RowNumber','CustomerId','Surname'])
df_reg

df_reg['Gender']=pd.get_dummies(df_reg['Gender'],drop_first=True)
Geography_dumies=pd.get_dummies(df_reg['Geography'],drop_first=True)
df_reg=df_reg.drop(columns=['Geography'])
df_reg=pd.concat([df_reg,Geography_dumies],axis=1)
#the idea of this manipulation is to convert our geographical variable (text) into binary variable. And if we have 0 at both Germany and Spain this means it's France.
df_reg

"""***Random Forest***"""

x=df_reg.copy().drop(columns=['Exited']).values
y=df_reg['Exited'].values
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=42)

from sklearn.ensemble import RandomForestClassifier

model_rfc=RandomForestClassifier(n_jobs=-1)
parameters = {'n_estimators':[50,100,200,300,400],'max_depth':[3,4,5,6]}
model_rfc_grid = GridSearchCV(model_rfc, parameters,cv=10,verbose=1,n_jobs=-1).fit(x_train,y_train)
print(model_rfc_grid.best_params_)

print('Random Forest Classifier Cros validation score:',model_rfc_grid.best_score_*100)

model_rfc=RandomForestClassifier(n_jobs=-1,n_estimators=400,max_depth=6)
model_rfc.fit(x_train,y_train)
print('Random Forest Classifier Train score:',model_rfc.score(x_train,y_train)*100)

