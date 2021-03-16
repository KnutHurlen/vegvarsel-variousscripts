#import necessary modules
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
#can also import from cross_validation
#from sklearn.cross_validation import train_test_split
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import GridSearchCV
#Choose and import the model family from scikit-learn
from sklearn.neighbors import KNeighborsClassifier

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

#create some lists to store results
#training_accuracy = []
CV_accuracy = []

#try neighbors 1-25
neighbors_settings = range(1, 25)

#run NN model across the specified range
for num_neighbors in neighbors_settings:
    #specify/fit a model
    clf = KNeighborsClassifier(n_neighbors=num_neighbors)
    clf_acc = cross_val_score(clf, X_train, y_train, cv=5, scoring='accuracy')
    CV_accuracy.append(clf_acc.mean())


#plt.plot(neighbors_settings, training_accuracy, label="training accuracy")
plt.plot(neighbors_settings, CV_accuracy, label="test accuracy")
plt.ylabel("Accuracy")
plt.xlabel("n_neighbors")
plt.legend()

#Let's now use the CV results to choose a model
clf = KNeighborsClassifier(n_neighbors=6)
clf.fit(X_train, y_train)
y_model = clf.predict(X_test)
clf.score(X_train, y_train)
accuracy_score(y_test, y_model)
confusion_matrix(y_test, y_model)

#Thanks to Muller and Guido, 2017 
#and https://medium.com/@kathrynklarich/exploring-and-evaluating-ml-algorithms-with-the-wisconsin-breast-cancer-dataset-506194ed5a6a
