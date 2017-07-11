import pandas as pd
import matplotlib as mpl
mpl.use('TkAgg')
import seaborn as sns

df_all = pd.read_csv('./data/data-all.csv')

df_all = df_all[df_all['lat'] > 32.0]
deeded_lat = df_all[df_all['Status'] == 'DEED']
other_lat = df_all[df_all['Status'] != 'DEED']


mpl.pyplot.figure(figsize=(12, 12))
graph = sns.jointplot(x=deeded_lat.lat.values, y=deeded_lat.lng.values, color='r', size=10)
graph.x = other_lat.lat.values
graph.y = other_lat.lng.values
graph.plot_joint(mpl.pyplot.scatter, c='b', marker='x')

mpl.pyplot.ylabel('Longitude', fontsize=12)
mpl.pyplot.xlabel('Latitude', fontsize=12)
mpl.pyplot.show()
