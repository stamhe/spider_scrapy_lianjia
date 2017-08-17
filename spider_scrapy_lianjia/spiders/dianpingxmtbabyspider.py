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

class dianping_xmt_baby_spider(CrawlSpider):
    # 爬虫的识别名称，必须是唯一的，在不同的爬虫中你必须定义不同的名字
    name = "dianping_xmt_baby_spider"    # 设置爬虫名称

    # 搜索的域名范围，也就是爬虫的约束区域，规定爬虫只爬取这个域名下的网页
    allowed_domains = ["dianping.com"] # 设置允许的域名

    # 爬取的url列表，爬虫从这里开始抓取数据，所以，第一次下载的数据将会从这些urls开始，其他子url将会从这些起始url中继承性生成
    start_urls = [
        # 早教中心
        'http://www.dianping.com/search/category/1/70/g27761', # 所有的早教
    ]

    city_map = {
        "1"     : "021", # 上海
        "2"     : "010", # 北京
        "4"     : "020", # 广州
        "7"     : "0755", # 深圳
        "8"     : "028", # 成都

        "267"     : "0871", # 昆明
        "206"     : "0756", # 珠海
        "134"     : "0791", # 南昌
        "219"     : "0769", # 东莞
        "213"     : "0752", # 惠州
        "345"     : "0899", # 三亚
        "23"     : "0898", # 海口
        "101"     : "0577", # 温州
        "224"     : "0771", # 南宁
        "148"     : "0535", # 烟台
        "152"     : "0631", # 威海
        "94"     : "0513", # 南通
        "11"     : "0574", # 宁波
        "110"     : "0551", # 合肥
        "35"     : "0351", # 太原
        "24"     : "0311", # 石家庄
        "70"     : "0431", # 长春
        "18"    : "024", # 沈阳
        "19"     : "0411", # 大连
        "344"     : "0731", # 长沙
        "160"     : "0371", # 郑州
        "17"     : "029", # 西安
        "16"     : "027", # 武汉
        "21"     : "0532", # 青岛
        "22"     : "0531", # 济南
        "13"    : "0510", # 无锡
        "6"     : "0512", # 苏州
        "9"     : "023", # 重庆
        "10"    : "022", # 天津
        "3"     : "0571", # 杭州
        "14"    : "0591", # 福州
        "15"    : "0592", # 厦门
        "5"     : "025", # 南京
    }

    shop_type_map = {
        # 幼儿教育
        'g188'   : 110000,
        # 其他亲子服务
        'g27769' : 91000,
        # 亲子旅游
        'g33808' : 80001,
        # 亲子游乐
        'g161' : 71000,

        # 婴儿游泳
        'g27767' : 60001,

        # 托班/托儿所
        'g20009' : 51000,
        # 幼儿园
        'g189' : 41000,

        # 幼儿才艺
        'g27763' : 31000,

        # 幼儿外语
        'g27762' : 21000,

        # 早教中心
        'g27761' : 11000,
    }

    def parse(self, response):
        sel = Selector(response)
        for bianhao,city_id in self.city_map.items():
            for cat_id,shop_type in self.shop_type_map.items():
                cat_url = 'http://www.dianping.com/search/category/' + bianhao + '/70/' + cat_id
                yield scrapy.Request(cat_url, callback=self.parse_category, meta={'shop_type':shop_type, 'city_id' : city_id})

    def parse_category(self, response):
        self.log("=================================================")
        sel = Selector(response)
        shop_type = response.meta['shop_type']
        city_id = response.meta['city_id']

        cat_url = response.url
        http_status = response.status
        self.log("http_url = %s" % cat_url)
        self.log("http_status = %s proxy = %s" % (http_status, response.meta['proxy']))

        self.log("shop_type = %s" % shop_type)
        items = []
        shop_list = sel.xpath('//li[@class="t-item-box t-district J_li"]/div[@class="t-item"]/div[@class="t-list"]/ul/li')
	self.log("shop_list_len = %d" % len(shop_list))
        for shop in shop_list:
            uri = shop.xpath('a/@href').extract()[0]
            self.log("page_uri = %s" % uri)
            yield scrapy.Request('http://www.dianping.com' + uri, callback=self.parse_list, meta={'shop_type':shop_type, 'cat_url' : cat_url, 'city_id' : city_id})

    def parse_list(self, response):
        self.log("=================================================")
        sel = Selector(response)

        shop_type = response.meta['shop_type']
        cat_url = response.meta['cat_url']
        city_id = response.meta['city_id']

        http_status = response.status

        self.log("http_url = %s" % cat_url)
        self.log("http_status = %s proxy = %s" % (http_status, response.meta['proxy']))

        self.log("shop_type = %s" % shop_type)
        items = []
        shop_list = sel.xpath('//ul[@class="shop-list"]/li')
        for shop in shop_list:
            uri = shop.xpath('div/p/a[@class="shopname"]/@href').extract()[0]
            self.log("shop_uri = %s" % uri)
            yield scrapy.Request('http://www.dianping.com' + uri, callback=self.parse_content, meta={'shop_type':shop_type, 'cat_url' : cat_url, 'city_id' : city_id})

        ### 是否还有下一页，如果有，则继续
        next_page = sel.xpath('//a[@class="NextPage"]')
        if len(next_page) <= 0:
            return

        next_page = sel.xpath('//a[@class="NextPage"]/@href').extract()[0].strip()
        self.log("next_page = %s" % next_page)
        if next_page:
            self.log("next_page_uri = %s" % next_page)
            yield scrapy.Request('http://www.dianping.com' + next_page, callback=self.parse_list, meta={'shop_type' : shop_type, 'cat_url' : cat_url,  'city_id' : city_id})

    # 解析的方法，调用的时候传入从每一个url传回的response对象作为唯一参数，负责解析并获取抓取的数据(解析为item)，跟踪更多的url
    def parse_content(self, response):
        self.log("=================================================")
        self.log("cat_url = %s proxy = %s" % (response.meta['cat_url'], response.meta['proxy']))
        chenshi_name= response.meta['city_id']
        sel = Selector(response)

        item = SpiderDianpingXmtItem()

        shop_type   = response.meta['shop_type']
        shop_url    = response.url
        http_status = response.status

        self.log("chenshi_name = %s" % chenshi_name)
        self.log("shop_url = %s" % shop_url)
        self.log("shop_type = %s" % shop_type)
        self.log("http_status = %s" % http_status)

	x = sel.xpath('//div[@class="block shop-info"]')
        if len(x) > 0:
            shop_name   = sel.xpath('//div[@class="block shop-info"]/div/div[@class="shop-name"]/h1[@class="shop-title"]/text()').extract()[0].strip()

            shop_addr   = x[0].xpath('div/div[@class="desc-list"]/dl[@class="shopDeal-Info-address"]/dd[@class="shop-info-content"]/span[@itemprop="street-address"]/text()').extract()[0].strip()

            # shop_mobile
            x2 = x[0].xpath('div/div[@class="desc-list"]/dl/dd[@class="shop-info-content"]/a[@id="J-showPhoneNumber"]')
            if len(x2) > 0:
                shop_mobile = x2[0].xpath('@data-real').extract()[0].strip()
            else:
                shop_mobile = ""

            # shop_intro
            shop_intro  = ""
        else:
            shop_name   = sel.xpath('//div[@class="shop-info"]/div[@class="shop-name"]/h1[@class="shop-title"]/text()').extract()[0].strip()
            shop_addr   = sel.xpath('//div[@class="shop-info"]/div[@class="shop-addr"]/span/@title').extract()[0].strip()

            # shop_mobile
            x = sel.xpath('//div[@class="shop-info"]/div[@class="shopinfor"]/p/span')
            if len(x) == 0:
                shop_mobile = ""
            else:
                shop_mobile = x[0].xpath('text()').extract()[0].strip()

            # shop_intro 
            x = sel.xpath('//div[@class="block_all"]/div[@class="block_right"]/span')
            if len(x) < 2:
                shop_intro=""
            else:
                shop_intro = x[0].xpath('text()').extract()[0].strip()


        self.log("shop_name = %s" % shop_name)
        self.log("shop_addr = %s" % shop_addr)
        self.log("shop_mobile = %s" % shop_mobile)
        self.log("shop_intro = %s" % shop_intro)

        item['chenshi_name']    = chenshi_name
        item['shop_type']       = shop_type
        item['shop_url']        = shop_url
        item['shop_name']       = shop_name
        item['shop_addr']       = shop_addr
        item['shop_mobile']     = shop_mobile
        item['shop_intro']      = shop_intro

        return item


