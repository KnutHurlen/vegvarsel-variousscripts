#import necessary modules
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.tree import export_graphviz
#from sklearn.tree import export_graphviz
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_breast_cancer
from dmba import plotDecisionTree
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
#can add 'random_state = 42' to ensure consistency across runs

#Run grid search to find parameters
param_grid = [{'max_depth': list(range(1,8))}] # params to try in the grid search
clf = DecisionTreeClassifier()
grid_search = GridSearchCV(clf, param_grid, cv=5, verbose=1, return_train_score = True)
grid_search.fit(X_train, y_train)
#what are the best parameters?
print(grid_search.best_params_)
#how should we expect this to do based on the validation scores?
print('''best score = {:.2f}'''.format(grid_search.best_score_))

#predict for the holdout, compute accuracy, and view the confusion matrix
y_model = grid_search.predict(X_test)
accuracy_score(y_test, y_model)
confusion_matrix(y_test, y_model)