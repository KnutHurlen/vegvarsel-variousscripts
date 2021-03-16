#import necessary modules
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix
#from sklearn.tree import export_graphviz
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier

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
clf = RandomForestClassifier(max_depth=2, random_state=0)

#fit model
clf.fit(X_train, y_train)

#used trained/fitted model to predict
y_model = clf.predict(X_test)

#Generate the predicted probabilities
clf.predict_proba(X_test)

#assess results in several different ways 
clf.score(X_train, y_train)
accuracy_score(y_test, y_model)
#confusion_matrix(y_train, tree.predict(X_train))
confusion_matrix(y_test, y_model)

import matplotlib.pyplot as plt

confusion_matrix = confusion_matrix(y_test, y_model)
import seaborn as sn
sn.heatmap(confusion_matrix, annot=True)
plt.xlabel('Predicted', fontsize=15)
plt.ylabel('Actual', fontsize=15)
plt.show()
