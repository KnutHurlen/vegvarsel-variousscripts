########################################
#Read from file
#####################################

#First open .csv files in notepad to see what's there

#Use folder icon to select path

#Load necessary libraries
import pandas as pd
import os

#Mac
os.chdir('/Users/chandler/OneDrive - BI Norwegian Business School (BIEDU)/Library/Teaching Materials/DataSets')
#PC
#os.chdir('Z:\OneDrive - BI Norwegian Business School (BIEDU)\Library\Teaching Materials\DataSets')

#Import file
df1 = pd.read_csv('ex1.csv')

#open the loaded file to see what's there
df1
#do the same thing with the variable explorer

#compute the average of column a
df1[”a”].mean()
#huh?!
df1["a"].mean()
#quotes from Word not the same ASCII character!

#Now load ex2.csv and review
df2 = pd.read_table('ex2.csv')
df2
#what is this?

#clean up by changing separator 
df2 = pd.read_table('ex2.csv', sep=';')
df2

#compute the average grade
df2["grade"].mean()

#Will fail because grade has comma for decimal. Let's fix
df2 = pd.read_table('ex2.csv', sep=';', decimal = ',')
df2
df2["grade"].mean()
##############################


#########################
#Read data directly from clipboard (first copy ex2.csv contents to clipboard)
#########################

df3 = pd.read_clipboard(decimal = ",")
df3

############################
#Get json data using Web API
############################

import requests
url = 'https://api.github.com/repos/pydata/pandas/milestones/28/labels'
resp = requests.get(url)
data = resp.json()
issue_labels = pd.DataFrame(data)
issue_labels
issue_labels[0:3]
issue_labels.head()

#Let's generate some summary info about the data

issue_labels.sample(5)
issue_labels.describe()

###########
#Let's import a .csv file from the web, and get fancy with summarizing
#Thanks to: https://towardsdatascience.com/exploring-your-data-with-just-1-line-of-python-4b35ce21a82d
#Will require installing pandas_profiling
#############
import pandas_profiling
pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/planets.csv').profile_report().to_file('planets.html')

###############################
#Get data pre-loaded in scikit-learn
###############################

from sklearn.datasets import load_breast_cancer
cancer=load_breast_cancer()
cancer
#malignant target == 0

#let's make this dataset easier to view
df = pd.DataFrame(cancer.data, columns=cancer.feature_names)
df.head()
df['malignant'] = 1 - cancer.target
df.head()

#and now let's descrive the cancer data
df.describe()
pandas_profiling.ProfileReport(df).to_file('cancer_report.html')

############################
#Some others
###########################

#From twitter: http://www.tweepy.org/
#Via ODBC: pyodbc

############################
#Finally, let's write the cancer dataframe out to Excel
###########################

df.to_csv(r'cancer.csv', header=True, index=None, sep=' ')
df.to_csv(r'cancer.csv', header=True, index=None, sep=';')
df.to_excel(r'cancer.xls', header=True, index=None)
#NOTE: to_excel and savetxt are also options