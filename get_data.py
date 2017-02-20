#encoding=utf8
import time
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

headers = {
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Accept-Encoding": "gzip, deflate, sdch",
	"Accept-Language": "zh-CN,zh;q=0.8,ja;q=0.6,zh-TW;q=0.4,be;q=0.2,en;q=0.2",
	"Cache-Control": "max-age=0",
	"Connection": "keep-alive",
	"Cookie": "all-lj=144beda729446a2e2a6860f39454058b; lianjia_uuid=1561c3e5-d96d-4db5-b9ca-43f8cbea784e; select_city=510100; gr_user_id=9734e092-5ac9-4b60-85dc-fca0ea08ee76; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1; Hm_lvt_660aa6a6cb0f1e8dd21b9a17f866726d=1487558275,1487560359,1487560373; Hm_lpvt_660aa6a6cb0f1e8dd21b9a17f866726d=1487560373; gr_session_id_a1a50f141657a94e=2b6c5d60-cb5c-43dc-a7ed-968047b83865; _smt_uid=58aa5ea7.2616f3a4; CNZZDATA1253492306=916267771-1487553074-%7C1487556128; CNZZDATA1254525948=296251920-1487556744-%7C1487556744; CNZZDATA1255633284=2061915351-1487558161-%7C1487558161; CNZZDATA1255604082=1796196791-1487553337-%7C1487555334; _ga=GA1.2.1412978853.1487560361; lianjia_ssid=db6fc639-5f0c-4a8d-96c8-e07c0d73c66c",
	"Host": "cd.lianjia.com",
	"Referer": "http://cd.lianjia.com/chengjiao/l1/",
	"Upgrade-Insecure-Requests": "1",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
}

def crawl():
	# http://cd.lianjia.com/chengjiao/pg3l2/
	for page in range(1, 101):
		for floor in range(1, 4+1):
			url = base_url + "pg%dl%d/" %(page, floor)
			print url
			data = requests.get(url, headers=headers).content
			# print data
			DOM = jQuery(data.decode("utf8"))
			li_list = DOM("ul.listContent li")
			# print li_list
			params = []
			for i in range(len(li_list)):
				try:
					li_text = li_list.eq(i).text()
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
					mysql.write_items(sql, print_error=True)
					# print sql
					print home_id
				except:
					pass
			time.sleep(0.5)

if __name__=="__main__":
	crawl()