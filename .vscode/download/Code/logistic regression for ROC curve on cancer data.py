#import necessary modules
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
#can also import from cross_validation
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
import numpy as np
from sklearn.model_selection import GridSearchCV

#specify dataset
cancer=load_breast_cancer()

#let's make this dataset easier to view
df = pd.DataFrame(cancer.data, columns=cancer.feature_names)
df.head()
df['malignant'] = 1 - cancer.target

#now isolate data from target
y = df.pop('malignant')
X = df.copy(deep=True)

#split training and test data. 
X_train,X_test,y_train,y_test = train_test_split(X, y, test_size = 0.2, stratify = y, random_state = 8)
#'random_state = 42' just so that results stay constant for illustration

#Run grid search to find parameters
param_grid = [{'C': list(np.arange(0.1,10,0.1))}]
clf = LogisticRegression()
grid_search = GridSearchCV(clf, param_grid, cv=5, verbose=0, return_train_score = True).fit(X_train, y_train)
#Note method chaining above
#what are the best parameters?
#print(grid_search.best_params_)
#how should we expect this to do based on the validation scores?
#print('''best score = {:.2f}'''.format(grid_search.best_score_))

#Build an ROC curve by repeatedly replacing predictions based on different thresholds.
#   Each time, look at training accuracy and the confusion matrix

#start with the default threshold
accuracy_score(y_train, grid_search.predict(X_train))
#95% accuracy might look OK, but let's look at the confusion matrix
confusion_matrix(y_train, grid_search.predict(X_train))
#We sent 16 people home with cancer!

#using the model's predict_proba function, isolate the predicted P(X = malignant) for the training data
y_pred_prob = grid_search.predict_proba(X_train)[:,1]

#construct an object that contains a new set of classifications, where we manually set threshold
#start with the default value to verify we get the same confusion matrix as before
y_pred_class5 = np.where(y_pred_prob > 0.5, 1, 0)
accuracy_score(y_train, y_pred_class5)
#and verify the confusion matrix is the same
confusion_matrix(y_train,y_pred_class5)
#What are the TPR and FPR here?

#Now increase the threshold to 0.8 and regenerate the confusion matrix
y_pred_class8 = np.where(y_pred_prob > 0.8, 1, 0)
accuracy_score(y_train, y_pred_class8)
#accuracy's fallen. How about the confusion matrix?
confusion_matrix(y_train,y_pred_class8)
#what's happened in the confusion matrix? This is still the same logistic regression, just implemented
#   differently. Do you like this implementation more or less than the default? In the language of 
#   TPR and FPR, why do you or don't you like it?

#let's lower the threshold quite a bit
y_pred_class02 = np.where(y_pred_prob > 0.02, 1, 0)
accuracy_score(y_train, y_pred_class02)
#accuracy's fallen. How about the confusion matrix?
confusion_matrix(y_train,y_pred_class02)
#how does this compare to the default threshold? In the language of 
#   TPR and FPR, do you like this implementation?

#You've now computed 3 pairs of (TPR, FPR). Plot them in Excel or on a piece of paper. Do you see the ROC curve?


#let's lower the threshold quite a bit
y_pred_class01 = np.where(y_pred_prob > 0.001, 1, 0)
accuracy_score(y_train, y_pred_class01)
#accuracy's fallen. How about the confusion matrix?
confusion_matrix(y_train,y_pred_class01)