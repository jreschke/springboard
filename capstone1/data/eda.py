# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 18:43:33 2020

@author: jenny
"""

#importing packages for EDA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# scipi is a library for statistical tests and visualizations 
from scipy import stats
# random enables us to generate random numbers
import random
import seaborn as sns
import statsmodels.api as sm
from statsmodels.graphics.api import abline_plot
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn import linear_model, preprocessing
import warnings # For handling error messages.

#%% importing data file
dat = pd.read_csv("C:\\Users\\jenny\\Desktop\\springboard\\capstone1\\eda\\users-data.csv")
print(dat.shape)
dat = dat.iloc[:,0:11]

#%%
users_data = dat.dropna(axis=0)
print(users_data.shape)

#%% looking at the data set
print(users_data.info())#this looks good with 6 continuous parameters and four discrete types
print(users_data.describe())
print(users_data.groupby('weapon').describe())
#%% making some initial plots
users_data.boxplot()#number of shots has some extreme values, may not be valuable for analysis
plt.xlabel('box plots of contiuous parameters')

users_data.shots.hist(bins=20)
plt.xlabel('shots')
plt.ylabel('count of shots')

max_values = users_data.groupby('weapontype').max()#looking the accuracy there some values that are over 1.0 which is not possible

#remove rows where the accuracy is greater than 1.0
user_data_filtered = users_data[users_data['accuracy']<=1]#removed 35 rows

sns.pairplot(user_data_filtered)
#looking at this plot, accuracy seems to only be the parameter with a real distribution

#pearson correlation
user_data_filtered.corr()
#this shows what fundamentaly makes sense. For example, hits and shots are highly correlated. Kills correlates well with everything but KD and accuracy.

#making a swarmplot of the KD based on weapon types
sns.swarmplot(x='weapontype',y='kdRatio',data=user_data_filtered,hue='gametype')
plt.xticks(rotation=-15)
plt.xlabel('weapon types')
plt.ylabel('KD Ratio')

#setup the rankings so to determine possible relationships
user_data_filtered['ranking']=1
ranking = 1
for i in range(1,len(user_data_filtered)):
    if user_data_filtered.iloc[i,9]!=user_data_filtered.iloc[(i-1),9]:
        ranking =ranking+1
        user_data_filtered.iloc[i,11] = ranking
    else:
        user_data_filtered.iloc[i,11]=ranking


#heat map of variables with ranking
sns.heatmap(user_data_filtered.corr())

#heat map of variables based on weapon type
for i in user_data_filtered['weapontype'].unique():
    sns.heatmap(user_data_filtered.loc[user_data_filtered['weapontype']==i,:].corr())
    plt.title('Weapon type: '+i)
    plt.savefig('weapon-type-'+i+'.png')
    plt.show()

#linear regression on accuracy and ranking
X = user_data_filtered.loc[:,['accuracy','hits','kills','headshots','shots','deaths']]
X = sm.add_constant(X)
y = user_data_filtered.loc[:,'kdRatio']
X_train,  X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)

# Create the model
ols_model = sm.OLS(y_train,X_train)
ols_model = ols_model.fit()
ols_model.summary()
