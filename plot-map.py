import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import MySQLdb

# plt.figure(figsize=(15, 15))
plt.figure()

'''
llcrnrlon : longitude of lower left hand corner of the selected map domain.
llcrnrlat : latitude of lower left hand corner of the selected map domain.
urcrnrlon : longitude of upper right hand corner of the selected map domain.
urcrnrlat : latitude of upper right hand corner of the  selected map domain.
'''

map = Basemap(
	projection = 'merc',
	llcrnrlon  = 70,
	llcrnrlat  = 15,
	urcrnrlon  = 140,
	urcrnrlat  = 55,
	lat_0 = 15,
	lon_0 = 95,
	resolution ='l'
)

map.drawcoastlines()
map.drawstates()	# color='b'
map.drawcountries() # linewidth=2
map.drawmapboundary(fill_color='#689CD2')
map.fillcontinents(color='#BF9E30',lake_color='#689CD2',zorder=0)

xs = []
ys = []
z = []

mysql_cn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='root', db="lianjia")
com_data = pd.read_sql('select * from sold where lat is not null limit 20', con=mysql_cn)

for i in com_data.index:
	xpt, ypt = map( float(com_data.ix[i]["lng"]), float(com_data.ix[i]["lat"]) )
	print xpt, ypt
	xs.append(xpt)
	ys.append(ypt)
	z.append(com_data.ix[i]["sold_price"])

map.scatter(xs, ys, c=z)
c = plt.colorbar(orientation='horizontal')

plt.title("housing price")
plt.show()