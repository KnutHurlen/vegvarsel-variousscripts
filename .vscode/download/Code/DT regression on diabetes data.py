#import necessary modules
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model, datasets
#from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt

#specify dataset
diabetes = datasets.load_diabetes()
df = pd.DataFrame(diabetes.data, columns=diabetes.feature_names)
df.head()
df['progression'] = diabetes.target
df.head()

#isolate data from target
y = df.pop('progression')
X = df

#split training and test data. 
X_train,X_test,y_train,y_test = train_test_split(X, y, test_size = 0.2)

# Instantiatte and Fit regression model
regr = DecisionTreeRegressor(max_depth=2)
regr.fit(X_train, y_train)

# Predict
y_pred = regr.predict(X_test)

#Explained variance score: 1 is perfect prediction

#regr.score(X_train, y_train)
regr.score(X_test, y_test)
