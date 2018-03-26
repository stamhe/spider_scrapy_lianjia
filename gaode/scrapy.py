#!/usr/bin/python
#coding=utf-8

# http://restapi.amap.com/v3/place/text?key=b5f6ef7fda144987417023ec3732d24c&city=%E4%B8%8A%E6%B5%B7&output=json&keywords=健身&page=1&offset=100

import sys
from telnetlib import RSP
reload(sys)
sys.setdefaultencoding('utf8')

import MySQLdb

import base64
import requests
import simplejson
import redis
import time

conn = MySQLdb.connect(host='localhost',port=3306,user='root',passwd='123456', charset='utf8')
conn.autocommit(True)
conn.select_db('db_dianping_xmt')

data = []
date_time = time.strftime("%Y-%m-%d", time.localtime())


citylist = ('上海', '北京', '深圳', '广州', '成都', '南京', '厦门', '福州', '天津', '重庆', '苏州', '无锡', '济南', '青岛', '武汉', '西安', '郑州', '长沙', '大连', '沈阳', '长春', '石家庄', '太原', '合肥', '宁波', '南通', '威海', '烟台', '南宁', '温州', '海口', '三亚', '惠州', '东莞', '昆明', '南昌', '珠海')

for city_name in citylist:
    #city_name = '上海'
    offset = 50
    page = 1
    
    while True:
        params = {
            'key'   : 'b5f6ef7fda144987417023ec3732d24c',
            'output' : 'json',
            'page' : page,
            'offset' : offset,
            'keywords' : '健身',
            'city' : city_name
        }
        
        rsp = requests.get("http://restapi.amap.com/v3/place/text", params = params)
        if rsp.status_code != 200:
            break
        
        rsp_data = simplejson.loads(rsp.text)
        
        if rsp_data['status'] == 0:
            break
        
        for  item1 in rsp_data['pois']:
            cursor=conn.cursor()
            print "page = %d offset = %d city_name = %s address = %s" % (page, offset, item1['cityname'], item1['address'])
            if item1['address']:
                addr = item1['address']
            else:
                addr = ""
            
            shop_addr = item1['pname'] + item1['cityname'] + item1['adname'] + addr
            shop_mobile = ""
            if item1['tel']:
                shop_mobile = item1['tel']
            else:
                shop_mobile = ""
                
            item = {
                "chenshi_name" : city_name,
                "shop_type" : "10001", 
                "shop_url" : shop_addr,
                "shop_name" : item1['name'],
                "shop_addr" : shop_addr,
                "shop_mobile" : shop_mobile,
                "shop_intro" : item1['name'],
            }
            
            data = []
            data.append(item['chenshi_name'])
            data.append(item['shop_type'])
            data.append(item['shop_url'])
            data.append(item['shop_name'])
            data.append(item['shop_addr'])
            data.append(item['shop_mobile'])
            data.append(item['shop_intro'])
            data.append(date_time)
            cursor.execute('replace into t_dianping_gym_spider (chenshi_name, shop_type, shop_url, shop_name, shop_addr, shop_mobile, shop_intro, spider_date) values (%s, %s, %s, %s, %s, %s, %s, %s)', data)
            cursor.close()
          
          # 翻页
        page = page + 1
        time.sleep(3)