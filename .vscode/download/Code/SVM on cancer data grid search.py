#import necessary modules
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
#can also import from cross_validation
from sklearn.datasets import load_breast_cancer
from sklearn.svm import LinearSVC
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
X_train,X_test,y_train,y_test = train_test_split(X, y, test_size = 0.2, stratify = y)
#maybe add 'random_state = 42' for illustration

#Run grid search to find parameters
param_grid = [{'C': list(np.arange(0.1,10,0.1))}]
clf = LinearSVC()
grid_search = GridSearchCV(clf, param_grid, cv=5, verbose=1, return_train_score = True).fit(X_train, y_train)
#Note method chaining above
#what are the best parameters?
print(grid_search.best_params_)
#how should we expect this to do based on the validation scores?
print('''best score = {:.2f}'''.format(grid_search.best_score_))

#train the model using default options. Note method chaining in first option
#y_model = LinearSVC().fit(X_train, y_train).predict(X_test) #. Review volatility in random seed
#svm = LinearSVC(random_state = 1).fit(X_train, y_train)
#svm = LinearSVC(random_state = 20).fit(X_train, y_train)

#view confusion matrix
confusion_matrix(y_train, grid_search.predict(X_train))

#predict for the holdout, compute accuracy, and view the confusion matrix
y_model = grid_search.predict(X_test)
accuracy_score(y_test, y_model)
confusion_matrix(y_test, y_model)
