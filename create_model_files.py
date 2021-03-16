from azure.storage.blob import ContainerClient
from pandas import read_csv
from io import StringIO
from imblearn.over_sampling import RandomOverSampler
from sklearn.model_selection import GridSearchCV
#from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import StratifiedKFold
# import pandas as pd
# from collections import Counter
import pickle
import config

blob_service = ContainerClient.from_connection_string(config.blockblob, "model-inputs")
blob_service_up = ContainerClient.from_connection_string(config.blockblob, "treepickles")

inputfiles = blob_service.list_blobs()
for file in inputfiles:
    f = blob_service.download_blob(file.name)
    df = read_csv(StringIO(f.content_as_text()))

    data = df.values
    X, y = data[:, :-1], data[:, -1]

    oversample = RandomOverSampler(sampling_strategy='minority')
    X_over, y_over = oversample.fit_resample(X, y)

    X_train,X_test,y_train,y_test = train_test_split(X_over, y_over, test_size = 0.33, stratify = y_over)
    clf = RandomForestClassifier(random_state=1)

    n_estimators = [10, 30, 50]
    max_depth = [15, 25, 30, 50]
    min_samples_split = [5, 10, 15]
    min_samples_leaf = [2, 5, 10, 15] 

    hyperF = dict(n_estimators = n_estimators, max_depth = max_depth,  
                min_samples_split = min_samples_split, 
                min_samples_leaf = min_samples_leaf)

    gridF = GridSearchCV(clf, hyperF, cv = 3, verbose = 1, 
                        n_jobs = -1) 

    model = gridF.fit(X_train, y_train)
    blob_service_up.upload_blob(str(file.name).replace(".csv", "") + ".pickle", data=pickle.dumps(model), overwrite=True)




