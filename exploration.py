import pandas as pd
import matplotlib as mpl
mpl.use('TkAgg')
import seaborn as sns
import numpy as np



fileNames = ['data-2012.csv', 'data-2013.csv', 'data-2014.csv']
'Print Columns'

data_2012 = pd.read_csv('./data/data-2012.csv')
data_2013 = pd.read_csv('./data/data-2013.csv')
frames = [data_2012, data_2013]
df_prop = pd.concat(frames)
print df_prop.columns
'Percent Total Deeded'
vacant_lots = df_prop[df_prop['Property Class Code']=='905 - VAC-RES-LOT']
deeded_properties = df_prop[df_prop['Status'] == 'DEED']
vacant_deeded = deeded_properties[deeded_properties['Property Class Code'] == '905 - VAC-RES-LOT']
print ((float(len(deeded_properties))/len(df_prop))*100, 'Percent Deeded')
print (float(len(vacant_deeded))/len(deeded_properties)*100, 'percent deeded vacant lots')
print (float(len(vacant_deeded))/len(vacant_lots)*100, 'Percent vacant deeded')


'Print lat longitude of deeded properties'
df_latlong = df_prop[df_prop['lat'].notnull()]
df_latlong = df_latlong[df_latlong['lat'] < 34.0]
deeded_lat = df_latlong[df_latlong['Status'] == 'DEED']
other_lat = df_latlong[df_latlong['Status'] != 'DEED']


mpl.pyplot.figure(figsize=(12,12))
graph = sns.jointplot(x=deeded_lat.lat.values, y=deeded_lat.lng.values, color='r', size=10)
# graph.x = other_lat.lat.values
# graph.y = other_lat.lng.values
# graph.plot_joint(mpl.pyplot.scatter, c='b', marker='x')

mpl.pyplot.ylabel('Longitude', fontsize=12)
mpl.pyplot.xlabel('Latitude', fontsize=12)
mpl.pyplot.show()
