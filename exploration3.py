import pandas as pd
from lib.Helpers import currencyToFloat
from lib.Helpers import propTypeObject
from lib.Helpers import stringToFloat
from lib.Helpers import setLabel
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn.model_selection import train_test_split
import matplotlib as mpl
mpl.use('TkAgg')
import seaborn as sns
from scipy.stats import skew
from scipy.stats.stats import pearsonr
import numpy as np

df_2012 = pd.read_csv('./data/data-2012.csv')
df_2013 = pd.read_csv('./data/data-2013.csv')
df_2014 = pd.read_csv('./data/data-2014.csv')

df_all = pd.concat([df_2012, df_2013, df_2014])
df_all = df_all.sample(frac=1)
'Print df_all columns'
x_train = df_all[['Land', 'Market', 'Min. Bid', 'Finished Sq. Ft.','lastSalesPrice', 'lat', 'lng', 'Property Class Code', 'highestSalesPrice', 'lowestSalesValue', 'Stories', 'Constructed Year', 'Bedrooms']]
x_train['Market'] = x_train['Market'].apply(currencyToFloat)
x_train['Land'] = x_train['Land'].apply(currencyToFloat)
x_train['Min. Bid'] = x_train['Min. Bid'].apply(currencyToFloat)
x_train['Stories'] = x_train['Stories'].apply(float)
x_train['Bedrooms'] = x_train['Bedrooms'].apply(stringToFloat)
x_train['Constructed Year'] = x_train['Constructed Year'].apply(float)
x_train['Finished Sq. Ft.'] = x_train['Finished Sq. Ft.'].apply(stringToFloat)
print x_train.head(20)
'Test normalize data'
numeric_feats = x_train.dtypes[x_train.dtypes != "object"].index
skewed_feats = x_train[numeric_feats].apply(lambda x: skew(x.dropna())) #compute skewness
skewed_feats = skewed_feats[skewed_feats > 0.75]
skewed_feats = skewed_feats.index

x_train[skewed_feats] = np.log1p(x_train[skewed_feats])
'Get my labels'
y_train = df_all['Status'].apply(setLabel).values

'Get Dummies'
x_train = pd.get_dummies(x_train)
'Replace null vals with average'
x_train = x_train.fillna(x_train.mean())
'Graph Correlation'
labels = []
values = []
for col in x_train:
    labels.append(col)
    values.append(np.corrcoef(x_train[col].values, y_train)[0, 1])

corr_df = pd.DataFrame({'col_labels': labels, 'corr_values': values})
print corr_df.head(10)
ind = np.arange(len(labels))
width = 0.9
fig, ax = mpl.pyplot.subplots(figsize=(12, 40))
rects = ax.barh(ind, np.array(corr_df.corr_values.values), color='y')
ax.set_yticks(ind)
ax.set_yticklabels(corr_df.col_labels.values, rotation='horizontal')
ax.set_xlabel("Correlation coefficient")
ax.set_title("Correlation coefficient of the variables")
mpl.pyplot.show()
