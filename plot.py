import pandas as pd
import MySQLdb
import matplotlib.pyplot as plt

mysql_cn = MySQLdb.connect(host='localhost', port=3306,user='root', passwd='root',db="lianjia")
df = pd.read_sql('select * from sold', con=mysql_cn)

a = df.groupby(['sold_time']).count()
a["count"] = a.id

b = a[["count"]]

b.plot(legend=False)
# b.plot()
plt.show()



#===============================================
import pandas as pd
import MySQLdb
import matplotlib.pyplot as plt

mysql_cn= MySQLdb.connect(host='localhost', port=3306,user='root', passwd='root',db="lianjia")

df = pd.read_sql('select * from sold', con=mysql_cn)
a = df.groupby(['sold_time'])

a.sold_price.mean().plot()
plt.show()
