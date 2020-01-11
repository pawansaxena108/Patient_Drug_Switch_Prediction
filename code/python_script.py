# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""Titatanic.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_Y5CxSZyVd3ts7dpPCadVI7h1xhmhyVg
"""

!pip install category_encoders

import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
import seaborn as sns
from matplotlib import pyplot as plt
import os
import zipfile
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold,GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,Imputer,OneHotEncoder
import category_encoders as ce
from sklearn.model_selection import train_test_split
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

from google.colab import drive
drive.mount('/content/drive')
with zipfile.ZipFile('/content/drive/My Drive/titanicdataset-traincsv.zip','r') as zip1:
   zip1.extractall()

train=pd.read_csv('/content/train.csv')
x_test=pd.read_csv('/content/drive/My Drive/test.csv')
y_test=pd.read_csv('/content/drive/My Drive/gender_submission.csv',usecols=['Survived'])

X=train[set(train.columns)-{'Survived'}]
Y=train.Survived
Y.columns=['Survived']

X.drop(['Name','Ticket'],axis=1,inplace=True)

x_train, x_val, y_train, y_val= train_test_split(X,Y,test_size=.2)

x_test=x_test[x_train.columns]

categorical=[x_train.columns[(np.where(x_train.dtypes=='object'))]]
categorical=categorical[0].values.tolist()

numerical=list(set(x_train.columns)-set(categorical))

class NumericalImputer(BaseEstimator, TransformerMixin):
  mean_values={}
 
  def __init__(self,values):
    if not isinstance(values,list):
      self.features=[values]
    else:
      self.features=values
  def fit(self,X,y=None):
    for var in self.features:
      self.mean_values[var]=X[var].mean()
    return self
  def transform(self,X):
      X=X.copy()
      #print(self.features)
      for var in self.features:
        #print(self.mean_values[var])
        X[var]=X[var].fillna(self.mean_values[var]) 
        #print(self.mean_values)

      return X

class CategoricalImputer(BaseEstimator, TransformerMixin):
  mode_values={}
  x=pd.DataFrame()
 
  def __init__(self,values):
    if  not isinstance(values,list):
      self.features=[values]
    else:
      self.features=values
  def fit(self,X,y=None):
    for var in self.features:
      self.mode_values[var]=X[var].mode()
    return self
  def transform(self,X):
      X=X.copy()
      for var in self.features:
        
         X[var]=X[var].fillna(self.mode_values[var][0])
      return X

classifier=LogisticRegression()

encoder2=OneHotEncoder(handle_unknown='ignore')

imputer1=SimpleImputer(strategy='most_frequent')
imputer2=NumericalImputer(numerical)
imputer3=CategoricalImputer(categorical)
encoder=ce.BinaryEncoder(handle_unknown='ignore',return_df=True)

pipeline =Pipeline(steps=[('imputer2',imputer2),('imputer3',imputer3),('encoder',encoder)])



grid_search=GridSearchCV(classifier,param_grid={'C':[.001,.01,.1,1]},cv=2)

grid_search.fit(transformed,y_train)

pipeline.fit(x_train,y_train)

grid_search.score(x_test,y_test)

pipeline.fit(x_train)

np.where(transformed.apply(lambda x: x==1))

grid_search.score(x_test,y_test)

transformed=pipeline.transform(x_test)

encoder=ce.BinaryEncoder()

df=pd.DataFrame({'A':list('pawan'),'B':list('saxen')})

transformed.head()

class DropUnneccearyColumn(BaseEstimator,TransformerMixin):
  def __init__(self,vars):
    print("inside __init__")
    if not isinstance(vars,list):
         self.features=[vars]
    else:
         self.features=vars    

  def fit(self,X):
    self.columndroped=self.features
    print("inside fit")
    
    print(self)
    return self

  def transform(self,X):
       print("inside transfrom")
       #print(X)
       X.drop(self.columndroped,axis=1,inplace=True)
       return self

from sklearn.metrics import confusion_matrix,roc_auc_score

confusion_matrix(y_test,y_pred)

roc_auc_score(y_test,y_pred)

