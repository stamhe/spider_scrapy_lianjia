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

class dianping_xmt_spider(CrawlSpider):
    # 爬虫的识别名称，必须是唯一的，在不同的爬虫中你必须定义不同的名字
    name = "dianping_xmt_spider"    # 设置爬虫名称

    # 搜索的域名范围，也就是爬虫的约束区域，规定爬虫只爬取这个域名下的网页
    allowed_domains = ["dianping.com"] # 设置允许的域名

    # 爬取的url列表，爬虫从这里开始抓取数据，所以，第一次下载的数据将会从这些urls开始，其他子url将会从这些起始url中继承性生成
    start_urls = [
        'http://www.dianping.com/search/category/1/75/g2878', # 兴趣生活 shop_type = 1
        #'http://www.dianping.com/search/category/1/75/g2872', # 外语培训 shop_type = 2
        #'http://www.dianping.com/search/category/1/75/g2873', # 音乐培训 shop_type = 3
        #'http://www.dianping.com/search/category/1/75/g2876', # 升学辅导shop_type = 4
        #'http://www.dianping.com/search/category/1/75/g2874', # 美术培训shop_type = 5
        #'http://www.dianping.com/search/category/1/75/g32722', # 留学 shop_type = 6
        #'http://www.dianping.com/search/category/1/75/g2882', # 其他 shop_type = 7
    ]

    shop_type_map = {
            'http://www.dianping.com/search/category/1/75/g2878' : 1, # 兴趣生活 shop_type = 1
            #'http://www.dianping.com/search/category/1/75/g2872' : 2, # 外语培训 shop_type = 2
            #'http://www.dianping.com/search/category/1/75/g2873' : 3, # 音乐培训 shop_type = 3
            #'http://www.dianping.com/search/category/1/75/g2876' : 4, # 升学辅导shop_type = 4
            #'http://www.dianping.com/search/category/1/75/g2874' : 5, # 美术培训shop_type = 5
            #'http://www.dianping.com/search/category/1/75/g32722': 6, # 留学 shop_type = 6
            #"http://www.dianping.com/search/category/1/75/g2882" : 7, # 其他
    }


    def parse(self, response):
        sel = Selector(response)
        if response.meta.has_key("shop_type"):
            shop_type = response.meta['shop_type']
        else:
            shop_type = self.shop_type_map[response.url]

        cat_url = response.url
        http_status = response.status
        self.log("http_status = %s proxy = %s" % (http_status, response.meta['proxy']))
        if http_status != 200:
            self.log("repeat>>>>>")
            yield scrapy.Request(cat_url, callback=self.parse, meta={'shop_type' : shop_type})
            return

        self.log("shop_type = %s" % shop_type)
        items = []
        shop_list = sel.xpath('//div[@class="txt"]/div[@class="tit"]/a[@data-hippo-type="shop"]')
        shop_count = len(shop_list)
        for shop in shop_list:
            uri = shop.xpath('@href').extract()[0]
            self.log("shop_uri = %s" % uri)
            yield scrapy.Request('http://www.dianping.com' + uri, callback=self.parse_content, meta={'shop_type':shop_type, 'cat_url' : cat_url, 'shop_count' : shop_count})

        ### 是否还有下一页，如果有，则继续
        next_page = sel.xpath('//a[@class="next"]/@href').extract()[0].strip()
        self.log("next_page = %s" % next_page)
        if next_page:
            self.log("next_page_uri = %s" % next_page)
            yield scrapy.Request('http://www.dianping.com' + next_page, callback=self.parse, meta={'shop_type' : shop_type})



    # 解析的方法，调用的时候传入从每一个url传回的response对象作为唯一参数，负责解析并获取抓取的数据(解析为item)，跟踪更多的url
    def parse_content(self, response):
        self.log("=================================================")
        self.log("cat_url = %s proxy = %s shop_count = %d" % (response.meta['cat_url'], response.meta['proxy'], response.meta['shop_count']))
        chenshi_name= '上海'
        sel = Selector(response)

        item = SpiderDianpingXmtItem()

        shop_type   = response.meta['shop_type']
        shop_url    = response.url
        cat_url     = response.meta['cat_url']
        shop_count  = response.meta['shop_count']
        http_status = response.status

        self.log("shop_url = %s" % shop_url)
        self.log("shop_type = %s" % shop_type)
        self.log("http_status = %s" % http_status)
        if http_status != 200:
            self.log("repeat>>>>")    
            #yield scrapy.Request(shop_url, callback=self.parse_content, meta={'shop_type' : shop_type, 'cat_url' : cat_url, 'shop_count' : shop_count})

        shop_name   = sel.xpath('//div[@class="shop-name"]/h1/text()').extract()[0].strip()
        self.log("shop_name = %s" % shop_name)

        shop_addr   = sel.xpath('//div[@class="address"]/text()').extract()[1].strip()
        self.log("shop_addr = %s" % shop_addr)

        x = sel.xpath('//div[@class="phone"]/span')
        if len(x) == 0:
            shop_mobile=""
        else:
            shop_mobile = x[0].xpath('@data-phone').extract()[0]

        self.log("shop_mobile = %s" % shop_mobile)

        x = sel.xpath('//div[@class="mod shop-info"]/ul/li')
        if len(x) < 2:
            shop_intro=""
        else:
            shop_intro = x[1].xpath('text()').extract()[1].strip()

        self.log("shop_intro = %s" % shop_intro)

        item['chenshi_name']    = chenshi_name
        item['shop_type']       = shop_type
        item['shop_url']        = shop_url
        item['shop_name']       = shop_name
        item['shop_addr']       = shop_addr
        item['shop_mobile']     = shop_mobile
        item['shop_intro']      = shop_intro

        return item


