import pandas as pd
pd.set_option('display.float_format', lambda x: '%.3f' % x)
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
from tabulate import tabulate

df_2012 = pd.read_csv('./data/data-2012.csv')
df_2013 = pd.read_csv('./data/data-2013.csv')
df_2014 = pd.read_csv('./data/data-2014.csv')

df_all = pd.concat([df_2012, df_2013, df_2014])
df_all = df_all.dropna(subset=['Pin'])
# df_all = df_all.sample(frac=1)
'Print df_all columns'
x_train = df_all[['Land', 'Market', 'Min. Bid', 'Finished Sq. Ft.','lastSalesPrice', 'Property Class Code', 'highestSalesPrice',  'Bedrooms']]
x_train['Market'] = x_train['Market'].apply(currencyToFloat)
x_train['Land'] = x_train['Land'].apply(currencyToFloat)
x_train['Min. Bid'] = x_train['Min. Bid'].apply(currencyToFloat)
# x_train['Stories'] = x_train['Stories'].apply(stringToFloat)
x_train['Bedrooms'] = x_train['Bedrooms'].apply(stringToFloat)
# x_train['Constructed Year'] = x_train['Constructed Year'].apply(stringToFloat)
x_train['Finished Sq. Ft.'] = x_train['Finished Sq. Ft.'].apply(stringToFloat)

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
x_train['Pin'] = df_all['Pin']
'Graph Correlation'
labels = []
values = []
for col in x_train:
    labels.append(col)
    values.append(np.corrcoef(x_train[col].values, y_train)[0, 1])

corr_df = pd.DataFrame({'col_labels': labels, 'corr_values': values})


# 'Train My Keras'
#
# from keras.layers import Dense
# from keras.models import Sequential
# from keras.regularizers import l1
# from sklearn.preprocessing import StandardScaler
#
# X_train = StandardScaler().fit_transform(x_train)
##y_train = df_all['Status'].apply(setLabel).values

# X_tr, X_test, y_tr, y_test = train_test_split(X_train, y_train, random_state = 3)
#
# model = Sequential()
# model.add(Dense(12, input_dim=X_tr.shape[1], activation='relu'))
# model.add(Dense(8, activation='relu'))
# model.add(Dense(1, activation='sigmoid'))
#
# # Compile model
# model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# # Fit the model
# model.fit(X_tr, y_tr, epochs=150, batch_size=10)
# # evaluate the model
# predictions = model.predict(X_test)
# pred = [round(x[0]) for x in predictions]
'Train my conventional'
X_train, X_test, y_train, y_test = train_test_split(x_train, y_train, test_size= 0.33, random_state=42)
clf = DecisionTreeClassifier(random_state=0)
print 'training'
clf.fit(X_train, y_train)
print 'predicting'
pred = clf.predict(X_test)
#
'Print Accuraccy'
acc = accuracy_score(pred, y_test)
print (acc, 'accuracy_score')
test_array = X_test.values


'Print precision_score'
total_deed = len([x for x in y_test if x == 1.0])
total_correct_pred = [i for i, x in enumerate(y_test) if x == 1.0 and pred[i] == 1.0]
total_missed_pred = len([x for i, x in enumerate(y_test) if x == 1.0 and pred[i] == 0.0])
total_wrong_pred = len([x for i, x in enumerate(pred) if x == 1.0 and y_test[i] == 0.0])
print ('total correct predictions for deed', len(total_correct_pred))
print ('total missed predictions for deed', total_missed_pred)
print ('total wrong predictions for deed', total_wrong_pred)

'Examples'
pins = list(X_test.iloc[total_correct_pred]['Pin'])
predicted_props = df_all[df_all['Pin'].isin(pins)]
print len(predicted_props[predicted_props['Property Class Code'] == '905 - VAC-RES-LOT'])
# print tabulate(predicted_props, headers="keys")
