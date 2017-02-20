#encoding=utf8
import re
import time
import json
import hashlib
import requests
from pyquery import PyQuery as jQuery
from in2mysql import MySQL_API

connect_info = {
	"host": "127.0.0.1",
	"user": "root",
	"pass": "root",
	"db": "lianjia",
}
mysql = MySQL_API(connect_info=connect_info)

headers = {
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Accept-Encoding": "gzip, deflate, sdch",
	"Accept-Language": "zh-CN,zh;q=0.8,ja;q=0.6,zh-TW;q=0.4,be;q=0.2,en;q=0.2",
	"Cache-Control": "max-age=0",
	"Connection": "keep-alive",
	"Cookie": "lianjia_uuid=1561c3e5-d96d-4db5-b9ca-43f8cbea784e; select_city=510100; gr_user_id=9734e092-5ac9-4b60-85dc-fca0ea08ee76; logger_session=e357483141aaf7325449152e37b334fa; _smt_uid=58aa5ea7.2616f3a4; _gat=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1; CNZZDATA1256144579=779727538-1487565778-http%253A%252F%252Fcd.lianjia.com%252F%7C1487572911; CNZZDATA1254525948=1423487015-1487567886-http%253A%252F%252Fcd.lianjia.com%252F%7C1487567886; CNZZDATA1255633284=439117336-1487568653-http%253A%252F%252Fcd.lianjia.com%252F%7C1487568961; CNZZDATA1255604082=1719047957-1487566134-http%253A%252F%252Fcd.lianjia.com%252F%7C1487569538; _ga=GA1.2.1412978853.1487560361; lianjia_ssid=07772c66-faca-4ec5-b96e-d963318044f5; gr_session_id_a1a50f141657a94e=ead7ee2c-ebee-4a56-9419-3f246b2d77a5",
	"Upgrade-Insecure-Requests": "1",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
}

def crawl_chengjiao():
	base_url = "http://cd.lianjia.com/chengjiao/"
	for room in range(1, 4+1):
		for page in range(1, 100+1):
			# http://cd.lianjia.com/chengjiao/pg3l2/
			url = base_url + "pg%dl%d/" %(page, room)
			print url
			data = requests.get(url, headers=headers).content
			# print data
			DOM = jQuery(data.decode("utf8"))
			li_list = DOM("ul.listContent li")
			# print li_list
			params = []
			for i in range(len(li_list)):
				try:
					li_html = li_list.eq(i).html()
					li_dom = jQuery(li_html)

					title_elements = li_dom("div.title a")
					title_element = title_elements.eq(0)
					home_url = title_element.attr("href").encode("utf8")
					home_id = home_url.split("/")[-1].split(".")[0]
					home_desc = title_element.text().encode("utf8")

					chao_xiang = li_dom("div.houseInfo").eq(0).text().encode("utf8")
					lou_ceng_build_desc = li_dom("div.positionInfo").eq(0).text().encode("utf8").split()
					lou_ceng_build_desc.append("")
					lou_ceng, build_desc = lou_ceng_build_desc[: 2]
					addtion_desc = li_dom("div.dealHouseInfo").eq(0).text().encode("utf8")
					sold_time = li_dom("div.dealDate").eq(0).text().encode("utf8")
					sold_price = li_dom("div.unitPrice span").eq(0).text().encode("utf8")
					sold_total_price = li_dom("div.totalPrice span").eq(0).text().encode("utf8")

					values = (
						home_id, sold_time, sold_price, sold_total_price,
						home_desc, chao_xiang, lou_ceng, build_desc, addtion_desc
					)
					params.append(values)

					sql = "INSERT INTO sold (home_id, sold_time, sold_price, sold_total_price," \
						  "home_desc, chao_xiang, lou_ceng, build_desc, addtion_desc) VALUES " \
						  "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(values)
					# mysql.write_items(sql, print_error=True)
					mysql.write_items(sql, print_error=False)
					# print sql
					print home_id
				except:
					pass
			time.sleep(0.1)

def crawl_new_house():
	base_url = "http://cd.fang.lianjia.com/loupan/"
	for room in range(1, 4 + 1):
		page_num = 5
		page = 0
		while page < page_num:
			page += 1
			# http://cd.fang.lianjia.com/loupan/pg3l1/
			url = base_url + "pg%dl%d/" % (page, room)
			print url
			data = requests.get(url, headers=headers).content
			# print data
			DOM = jQuery(data.decode("utf8"))
			page_num = DOM("div.page-box.house-lst-page-box").eq(0).attr("page-data")
			page_num = json.loads(page_num)["totalPage"]
			print page_num
			li_list = DOM("ul.house-lst li")
			params = []
			for i in range(len(li_list)):
				try:
					li_html = li_list.eq(i).html()
					li_dom = jQuery(li_html)

					title_elements = li_dom("div.col-1 h2 a")
					title_element = title_elements.eq(0)
					url = title_element.attr("href").encode("utf8")
					# http://cd.fang.lianjia.com/loupan/p_ztrjhzxaalow/
					url = "http://cd.fang.lianjia.com" + url
					name = title_element.text().encode("utf8")
					region = li_dom("span.region").eq(0).text().encode("utf8")
					space = li_dom("div.area").eq(0).text().encode("utf8")
					space = re.sub("\s+", " ", space)
					other_desc = li_dom("div.other").eq(0).text().encode("utf8")
					state = li_dom("div.type").eq(0).text().encode("utf8")
					price = li_dom("div.average span").eq(0).text().encode("utf8")

					values = (
						url, name, region, space,
						other_desc, state, price
					)
					params.append(values)

					sql = "INSERT INTO new_house (url, name, region, space, other_desc, state, price) VALUES " \
						  "('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (values)
					# mysql.write_items(sql, print_error=True)
					mysql.write_items(sql, print_error=False)
					# print sql
					print name
				except:
					pass

			time.sleep(0.1)

def crawl_comment():
	# http://cd.fang.lianjia.com/loupan/p_hlctaapyl/
	# http://cd.fang.lianjia.com/loupan/p_hlctaapyl/pinglun/pg3
	rows = mysql.query("select id, url, name from new_house")
	for row in rows:
		id = row[0]
		url = row[1]
		name = row[2]
		print url
		page = 0
		page_num = 1
		while page < page_num:
			page += 1
			url_full = url + "pinglun/pg%d" %page
			data = requests.get(url_full, headers=headers).content
			# print data
			DOM = jQuery(data.decode("utf8"))
			if "nocomment" in data:
				break
			try:
				page_num = DOM("div.page-box.comment-lst-page-box").eq(0).attr("page-data")
				# print page_num
				page_num = json.loads(page_num)["totalPage"]
			except:
				print data
				break
			li_list = DOM("ul.list li")
			params = []
			for i in range(len(li_list)):
				try:
					li_html = li_list.eq(i).html()
					li_dom = jQuery(li_html)

					user_user_days = li_dom("div.l_userpic div.info").eq(0).text().encode("utf8").split()
					user_user_days.append("")
					user, user_days = user_user_days[: 2]
					star = li_dom("div.star_info").eq(0).attr("style").encode("utf8")# width: 100%
					star = star.split()[-1][:-1]
					date_time = li_dom("div.time").eq(0).text().encode("utf8")
					comment = li_dom("div.words").eq(0).text().encode("utf8")
					m = hashlib.md5()
					m.update(url+date_time+comment)
					md5 = m.hexdigest()

					values = (
						url, user, user_days, star, comment,
						date_time, md5
					)
					params.append(values)

					sql = "INSERT INTO new_house_comment (url, user, user_days, star, comment, date_time, md5) VALUES " \
						  "('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (values)
					# mysql.write_items(sql, print_error=True)
					mysql.write_items(sql, print_error=False)
					# print sql
					# print url
				except Exception as e:
					print e

if __name__=="__main__":

	# crawl_chengjiao()
	# crawl_new_house()
	crawl_comment()