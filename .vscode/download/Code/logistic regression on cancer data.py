#import necessary modules
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
#can also import from cross_validation
from sklearn.datasets import load_breast_cancer

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
X_train,X_test,y_train,y_test = train_test_split(X, y, test_size = 0.2, stratify = y)
#maybe add 'random_state = 42' for illustration

#Choose and import the model family from scikit-learn
from sklearn.linear_model import LogisticRegression
#from sklearn.svm import LinearSVC

#train the model using the default regularization parameter C=1. Try different parameters
logreg = LogisticRegression(C=1.0).fit(X_train, y_train)

#assess the model based on test data performance
#clf.fit(X_train, y_train)
y_model = logreg.predict(X_test)
logreg.score(X_train, y_train)
accuracy_score(y_test, y_model)
confusion_matrix(y_test, y_model)

#Thanks to Muller and Guido, 2017
#Note susceptibility to random_state; switch from 42 to 2017 and re-execute
