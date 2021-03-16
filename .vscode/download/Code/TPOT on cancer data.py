#This script illustrates use of the Python library tpot (tree-based pipeline optimization tool)
#   on the breast cancer dataset. In part becaues the dataset is just really small, tpot does not 
#   radically outperform simpler models. But the script illustrates a few important points:
#       -long runtimes in auto-ML
#       -how to pickle models such that they're portable
#       -the scope of tpot's search (via print(clf))

import pandas as pd
import numpy as np
from tpot import TPOTClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
#from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_breast_cancer
import pickle

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

#instantiate a TPOT classifier.
#This will instantiate clf as a 5-generation genetic algorithm (GA), each generation having 
#   a population of 50 chromosomes
clf = TPOTClassifier(generations=5, population_size=50, verbosity=2, n_jobs = -1)
#n_jobs indicates the number of threads; -1 indicates "use all available"

#Fit the classifier
clf.fit(X_train, y_train)
#will probably get a warning that xgboost is not available. try installing it and re-running.
#   Gradient Boosted trees are powerful!
#conda install -c anaconda py-xgboost
#OR !pip install xgboost


#This will tell you what tpot did:
#print(clf)
#and this will tell you the pipeline tpot chose
#clf.fitted_pipeline_

#evaluate the model on train, then on holdout
confusion_matrix(y_train, clf.predict(X_train))
y_model = clf.predict(X_test)
confusion_matrix(y_test, y_model)

#and lets look at some performance scores
from sklearn import metrics
print(metrics.classification_report(y_test, y_model))

#Suppose you want to use this model for prediction, but you don't want to always re-train.
#Here are several ways to store a trained model for subsequent prediction w/o re-training

#Store the trained pipeline as its own .py file. This would thus be callable in another script
clf.export('tpot_cancer_pipeline.py')

#Create an object that is the pickled model pipeline. This can be saved in a relational DB, passed as
#   an argument to another Python function, etc. This makes models' "predict" methods very portable.
s = pickle.dumps(clf.fitted_pipeline_) #this 's' is portable 
clf2 = pickle.loads(s) #this is exactly the same as clf, above
clf2.score(X_test, y_test)

#Store pickled prediction pipeline
filename = 'cancer_tpot_predict.sav'
pickle.dump(clf.fitted_pipeline_, open(filename, 'wb'))

#And load pickled prediction pipeline
loaded_model = pickle.load(open(filename, 'rb'))
loaded_model.score(X_test, y_test)


