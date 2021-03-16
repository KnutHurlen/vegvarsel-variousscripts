#import necessary modules
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model, datasets
#from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from tpot import TPOTRegressor

#specify dataset
diabetes = datasets.load_diabetes()
df = pd.DataFrame(diabetes.data, columns=diabetes.feature_names)
df.head()
df['progression'] = diabetes.target
#df.head()

#isolate data from target
y = df.pop('progression')
X = df

#y.head()

#split training and test data. 
X_train,X_test,y_train,y_test = train_test_split(X, y, test_size = 0.2)

#specify model
regr = linear_model.LinearRegression()
regr = TPOTRegressor(generations=5, population_size=50, verbosity=2, n_jobs = -1)
#regr = linear_model.Ridge()
#regr = linear_model.Lasso()

#train the model using all data
#regr.fit(X, y)

# Train the model using the training sets
regr.fit(X_train, y_train)


#Explained variance score: 1 is perfect prediction
regr.score(X, y)
regr.score(X_train, y_train)
regr.score(X_test, y_test)

#Generate predictions, then append to df, then write to Excel
results = X_test
y_pred=regr.predict(X_test)
results['progression'] = y_test
results['pred_progression'] = y_pred
results.to_excel(r'diabetes.xls', header=True, index=True)