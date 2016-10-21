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
        data.append(item['xiaoqu_id'])
        data.append(item['house_id'])
        data.append(item['title'])
        data.append(item['price'])
        data.append(item['view_count'])
        date = time.strftime("%Y-%m-%d", time.localtime())
        data.append(date)

        #cursor.execute('insert into t_ershoufang_house (xiaoqu_id, house_id, title, price, view_count) values (%s, %s, %s, %s, %s)', data)
        cursor.execute('replace into t_ershoufang_house (xiaoqu_id, house_id, title, price, view_count, spider_date) values (%s, %s, %s, %s, %s, %s)', data)
        cursor.close()
        #return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.conn.close()
