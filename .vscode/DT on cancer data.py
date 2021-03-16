#import necessary modules
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.tree import export_graphviz
#from sklearn.tree import export_graphviz
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_breast_cancer
from dmba import plotDecisionTree

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

#choose model, applying pre-pruning (max_depth = 2)
clf = DecisionTreeClassifier(max_depth=2,random_state=0)

#fit model
clf.fit(X_train, y_train)

#used trained/fitted model to predict
y_model = clf.predict(X_test)

#Generate the predicted probabilities
clf.predict_proba(X_test)

#plot tree
#plotDecisionTree(clf, feature_names = X_train.columns)

#plot tree: http://webgraphviz.com/
export_graphviz(clf, out_file="tree.gv", class_names=["benign", "malignant"],feature_names=cancer.feature_names, impurity=False, filled=True)

#assess results in several different ways 
clf.score(X_train, y_train)
accuracy_score(y_test, y_model)
#confusion_matrix(y_train, tree.predict(X_train))
confusion_matrix(y_test, y_model)