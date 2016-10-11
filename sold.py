#encoding=utf8
import urllib2
import requests
from pyquery  import PyQuery as jQuery
from in2mysql import MySQL_API

base_url = "http://cd.lianjia.com/chengjiao/"
connect_info = {
	"host" : "127.0.0.1",
	"user" : "root",
	"pass" : "root",
	"db"   : "lianjia",
}
mysql = MySQL_API(connect_info=connect_info)

def crawl():
	# http://cd.lianjia.com/chengjiao/pg3l2/
	for page in range(1, 101):
		for floor in range(1, 4+1):
			url = base_url + "pg%dl%d" %(page, floor)
			data = requests.get(url).content
			DOM = jQuery(data.decode("utf8"))
			li_list = DOM("div.info-panel")
			params = []
			for i in range(len(li_list)):
				text = li_list.eq(i).text()
				# print text
				text = text.encode("utf8")
				'''
				时代晶科名苑 2室2厅 111平米 北 / 高楼层(共20层) / 2013塔楼 距1号线高新521米
				查看同户型成交记录 2016.08.30 链家网签约 14174 元/平 签约单价 157 万 签约总价
				'''
				text_list = text.split()
				desc = " ".join(text_list[:3])
				chao_xiang = text_list[3]
				lou_ceng = text_list[5]
				build_desc = text_list[7]
				addtion_desc = " ".join(text_list[8:-9])

				sold_time = text_list[-8]
				sold_price = text_list[-6]
				sold_total_price = text_list[-3]

				home_id = li_list.eq(i).html().encode("utf8")
				home_id = home_id.split('http://cd.lianjia.com/chengjiao/')[1]
				home_id = home_id.split('.html" target="_blank">')[0]

				values = (home_id, sold_time, sold_price, sold_total_price,
							   desc, chao_xiang, lou_ceng, build_desc, addtion_desc)
				params.append(values)

				sql  = "INSERT INTO sold (home_id, sold_time, sold_price, sold_total_price," \
					   "home_desc, chao_xiang, lou_ceng, build_desc, addtion_desc) VALUES " \
					   "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(values)
				mysql.write_items(sql, print_error=True)
				# print sql
				print home_id

			# sql = "INSERT INTO sold (home_id, sold_time, sold_price, sold_total_price, " \
			# 	  "home_desc, chao_xiang, lou_ceng, build_desc, addtion_desc) VALUES " \
			# 	  "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
			# mysql.write_items(sql, params, print_error=True)

if __name__=="__main__":
	crawl()