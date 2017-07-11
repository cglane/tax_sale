from sklearn.model_selection import train_test_split
from lib.Helpers import currencyToFloat
from lib.Helpers import propTypeObject
from lib.Helpers import stringToFloat
import pandas as pd
import matplotlib as mpl
mpl.use('TkAgg')
import seaborn as sns
import ast
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn import tree

def setLabel(value):
    if value == 'DEED':
        return 1.0
    return 0.0

'Print Columns'

df_2012 = pd.read_csv('./data/data-2012.csv')
df_2013 = pd.read_csv('./data/data-2013.csv')
df_2014 = pd.read_csv('./data/data-2014.csv')

df_prop = pd.concat([df_2012, df_2013, df_2014])
print df_prop.columns

'Percent Total Deeded'
vacant_lots = df_prop[df_prop['Property Class Code']== '905 - VAC-RES-LOT']
deeded_properties = df_prop[df_prop['Status'] == 'DEED']
vacant_deeded = deeded_properties[deeded_properties['Property Class Code'] == '905 - VAC-RES-LOT']
print (len(df_prop), 'total properties')
print (len(deeded_properties), 'deeded_properties')
print ((float(len(deeded_properties))/len(df_prop))*100, 'Percent Deeded')
print (float(len(vacant_deeded))/len(deeded_properties)*100, 'percent deeded vacant lots')
print (float(len(vacant_deeded))/len(vacant_lots)*100, 'Percent vacant deeded')


'Print lat longitude of deeded properties'

df_latlong = df_2013[df_2013['lat'].notnull()]
df_latlong = df_latlong[df_latlong['lat'] < 34.0]
deeded_lat = df_latlong[df_latlong['Status'] == 'DEED']
other_lat = df_latlong[df_latlong['Status'] != 'DEED']


mpl.pyplot.figure(figsize=(12, 12))
graph = sns.jointplot(x=deeded_lat.lat.values, y=deeded_lat.lng.values, color='r', size=10)
# graph.x = other_lat.lat.values
# graph.y = other_lat.lng.values
# graph.plot_joint(mpl.pyplot.scatter, c='b', marker='x')

mpl.pyplot.ylabel('Longitude', fontsize=12)
mpl.pyplot.xlabel('Latitude', fontsize=12)
mpl.pyplot.show()


'Graph Property Class Code'
cnt_srs = df_prop['Property Class Code'].value_counts()
mpl.pyplot.figure(figsize=(12,6))
sns.barplot(cnt_srs.index, cnt_srs.values, alpha=0.8, color='g')
mpl.pyplot.xticks(rotation='vertical')
mpl.pyplot.xlabel('Property Types', fontsize=12)
mpl.pyplot.ylabel('Number of Occurrences', fontsize=12)
mpl.pyplot.show()

'Graph Missing Values'

missing_df = df_prop.isnull().sum(axis=0).reset_index()
missing_df.columns = ['column_name', 'missing_count']
missing_df = missing_df.ix[missing_df['missing_count'] >0]
missing_df = missing_df.sort_values(by='missing_count')
ind = np.arange(missing_df.shape[0])
width = 0.9
fig, ax = mpl.pyplot.subplots(figsize=(12,18))
rects = ax.barh(ind, missing_df.missing_count.values, color='blue')
ax.set_yticks(ind)
ax.set_yticklabels(missing_df.column_name.values, rotation='horizontal')
ax.set_xlabel("Count of missing values")
ax.set_title("Number of missing values in each column")
# mpl.pyplot.show()

'Show column types, probably all strings....'

dtype_df = df_prop.dtypes.reset_index()
dtype_df.columns = ["Count", "Column Type"]

'Set Values'
x_train = df_prop[['Land', 'Market', 'Min. Bid', 'Finished Sq. Ft.','lastSalesPrice', 'Property Class Code']]
x_train.fillna(0, inplace=True)
x_train['Market'] = x_train['Market'].apply(currencyToFloat)
x_train['Land'] = x_train['Land'].apply(currencyToFloat)
x_train['Min. Bid'] = x_train['Min. Bid'].apply(currencyToFloat)
x_train['Property Class Code'] = x_train['Property Class Code'].apply(propTypeObject)
x_train['Finished Sq. Ft.'] = x_train['Finished Sq. Ft.'].apply(stringToFloat)
'Set Label'
y_train = df_prop['Status'].apply(setLabel).values

'Graph heat map'

labels = []
values = []
for col in x_train:
    labels.append(col)
    values.append(np.corrcoef(x_train[col].values, y_train)[0, 1])

corr_df = pd.DataFrame({'col_labels': labels, 'corr_values': values})
print corr_df.head(10)

X_train, X_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.33, random_state=42)


clf = svm.SVC()
print 'training'
clf.fit(X_train, y_train)
print 'predicting'
pred = clf.predict(X_test)
'(Test Val, Prediction Val)'
# print zip(y_test, pred)
'Print Accuraccy'
acc = accuracy_score(pred, y_test)
print (acc, 'accuracy_score')
'Print precision_score'
total_deed = len([x for x in y_test if x == 1.0])
total_correct_pred = len([x for i, x in enumerate(y_test) if x == 1.0 and pred[i] == 1.0])
total_missed_pred = len([x for i, x in enumerate(y_test) if x == 1.0 and pred[i] == 0.0])
total_wrong_pred = len([x for i, x in enumerate(pred) if x == 1.0 and y_test[i] == 0.0])
print total_deed
print ('total correct predictions for deed', total_correct_pred)
print ('total missed predictions for deed', total_missed_pred)
print ('total wrong predictions for deed', total_wrong_pred)

print
