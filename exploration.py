import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


fileNames = ['data-2012.csv', 'data-2013.csv', 'data-2014.csv']
'Print Columns'

"""[u'Unnamed: 0', u'bedrooms', u'bathrooms', u'owner_address',
       u'Deed Book', u'Winning Bid /\nReceipt No', u'lotSizeSqFt', u'Cert No',
       u'Item', u'lastSoldPrice', u'Deed Page', u'address', u'property_code',
       u'Bidder', u'Status', u'longitude', u'Pin', u'taxAssessmentYear',
       u'Bundle', u'Min. Bid /\nPayment Date', u'taxAssessment',
       u'Date Status Changed', u'yearBuilt', u'Tax Payer', u'lastSoldDate',
       u'zestimate', u'latitude', u'zpid', u'auction_year'],"""
data_2012 = pd.read_csv('./data/data-2012.csv')
data_2013 = pd.read_csv('./data/data-2013.csv')
data_2014 = pd.read_csv('./data/data-2014.csv')
frames = [data_2012, data_2013, data_2014]
df_prop = pd.concat(frames)

'Percent Total Deeded'
vacant_lots = df_prop[df_prop['property_code']=='905 - VAC-RES-LOT']
deeded_properties = df_prop[df_prop['Status'] == 'DEED']
vacant_deeded = deeded_properties[deeded_properties['property_code'] == '905 - VAC-RES-LOT']
print ((float(len(deeded_properties))/len(df_prop))*100, 'Percent Deeded')
print (float(len(vacant_deeded))/len(deeded_properties)*100, 'percent deeded vacant lots')
print (float(len(vacant_deeded))/len(vacant_lots)*100, 'Percent vacant deeded')


'Print lat longitude of deeded properties'
df_latlong = df_prop[df_prop['latitude'].notnull()]
deeded_lat = df_latlong[df_latlong['Status'] == 'DEED']
other_lat = df_latlong[df_latlong['Status'] != 'DEED']


plt.figure(figsize=(12,12))
graph = sns.jointplot(x=deeded_lat.latitude.values, y=deeded_lat.longitude.values, color='r', size=10)
graph.x = other_lat.latitude.values
graph.y = other_lat.longitude.values
graph.plot_joint(plt.scatter, c='b', marker='x')

plt.ylabel('Longitude', fontsize=12)
plt.xlabel('Latitude', fontsize=12)
plt.show()
