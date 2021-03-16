#import necessary modules
import pandas as pd
#import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
#can also import from cross_validation
#from sklearn.cross_validation import train_test_split
from sklearn.datasets import load_breast_cancer

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
training_accuracy = []
test_accuracy = []

#try neighbors 1-25
neighbors_settings = range(1, 25)

#run NN model across the specified range
for num_neighbors in neighbors_settings:
	#specify/fit a model
	clf = KNeighborsClassifier(n_neighbors=num_neighbors)
	clf.fit(X_train, y_train)

	#store accuracy
	training_accuracy.append(clf.score(X_train, y_train))

	#record accuracy on holdout data
	test_accuracy.append(clf.score(X_test, y_test))


plt.plot(neighbors_settings, training_accuracy, label="training accuracy")
plt.plot(neighbors_settings, test_accuracy, label="test accuracy")
plt.ylabel("Accuracy")
plt.xlabel("n_neighbors")
plt.legend()
#plt.show()

#choose "best" model from plot, and generation confusion matrix for that
#choose model (max_depth ~ 8).
#We're committing a major sin here. What is it?
clf = KNeighborsClassifier(n_neighbors=8)
clf.fit(X_train, y_train)
y_model = clf.predict(X_test)
clf.score(X_train, y_train)
accuracy_score(y_test, y_model)
confusion_matrix(y_test, y_model)

###############
#Generate predictions, then append to df, then write to Excel
###############
results = pd.DataFrame(X_test)
y_pred=clf.predict(X_test)
y_pred_prob= clf.predict_proba(X_test)
results['actual_benign'] = y_test
results['pred_benign'] = y_pred
results['pred_prob_benign'] = y_pred_prob[:,1]
#results.to_excel(r'cancer_model.xls', header=True, index=True)