# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import MySQLdb
import time

class SpiderScrapyLianjiaPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(host='127.0.0.1',port=3306,user='root',passwd='123456', charset='utf8')
        self.conn.autocommit(True)
        self.conn.select_db('lianjia')
    def process_item(self, item, spider):
        cursor=self.conn.cursor()
        data = []
        date_time = time.strftime("%Y-%m-%d", time.localtime())
        if spider.name == 'lianjiaspider':
            data.append(item['xiaoqu_id'])
            data.append(item['house_id'])
            data.append(item['title'])
            data.append(item['price'])
            data.append(item['view_count'])
            data.append(date_time)
            cursor.execute('replace into t_ershoufang_house (xiaoqu_id, house_id, title, price, view_count, spider_date) values (%s, %s, %s, %s, %s, %s)', data)
        elif spider.name == 'chenshi_count_spider':
            data.append(item['chenshi_name'])
            data.append(item['avg_price'])
            data.append(item['onsale_count'])
            data.append(item['sold_last_month'])
            data.append(item['view_last_day'])
            data.append(date_time)
            cursor.execute('replace into t_ershoufang_chenshi (chenshi_name, avg_price, onsale_count, sold_last_month, view_last_day, spider_date) values (%s, %s, %s, %s, %s, %s)', data)

        cursor.close()
        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.conn.close()
