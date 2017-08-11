#!/usr/bin/python
#coding=utf-8
# @hequan


import scrapy

from scrapy.spiders import Spider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
import re
from scrapy.spiders import CrawlSpider

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from spider_scrapy_lianjia.items import SpiderDianpingXmtItem

class baidu_spider(CrawlSpider):
    # 爬虫的识别名称，必须是唯一的，在不同的爬虫中你必须定义不同的名字
    name = "baidu_spider"    # 设置爬虫名称

    # 搜索的域名范围，也就是爬虫的约束区域，规定爬虫只爬取这个域名下的网页
    allowed_domains = ["baidu.com"] # 设置允许的域名

    # 爬取的url列表，爬虫从这里开始抓取数据，所以，第一次下载的数据将会从这些urls开始，其他子url将会从这些起始url中继承性生成
    start_urls = [
        'https://www.baidu.com',
    ]

    def parse(self, response):
        sel = Selector(response)

        cat_url = response.url
        http_status = response.status
        self.log("http_url = %s" % cat_url)
        self.log("http_status = %s proxy = %s" % (http_status, response.meta['proxy']))

        item = SpiderDianpingXmtItem()
        item['chenshi_name']    = "" 
        item['shop_type']       = 0
        item['shop_url']        = ""
        item['shop_name']       = ""
        item['shop_addr']       = ""
        item['shop_mobile']     = ""
        item['shop_intro']      = ""

        return item


