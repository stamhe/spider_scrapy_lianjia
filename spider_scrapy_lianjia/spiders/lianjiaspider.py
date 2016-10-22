#!/usr/bin/python
#coding=utf-8
# @hequan

from scrapy.spiders import Spider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
import re
from scrapy.spiders import CrawlSpider

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from spider_scrapy_lianjia.items import SpiderScrapyLianjiaItem

class lianjia_spider(CrawlSpider):
    # 爬虫的识别名称，必须是唯一的，在不同的爬虫中你必须定义不同的名字
    name = "lianjia_house_spider"    # 设置爬虫名称

    # 搜索的域名范围，也就是爬虫的约束区域，规定爬虫只爬取这个域名下的网页
    allowed_domains = ["lianjia.com"] # 设置允许的域名

    # 爬取的url列表，爬虫从这里开始抓取数据，所以，第一次下载的数据将会从这些urls开始，其他子url将会从这些起始url中继承性生成
    start_urls = [
        # 新里维多利亚 1611043078432
        'http://cd.lianjia.com/ershoufang/pg1c1611043078432/',
        'http://cd.lianjia.com/ershoufang/pg2c1611043078432/',
        # 英郡一期 3011055403435
        'http://cd.lianjia.com/ershoufang/pg1c3011055403435/',
        'http://cd.lianjia.com/ershoufang/pg2c3011055403435/',
        # 英郡三期 3011055400648
        'http://cd.lianjia.com/ershoufang/c3011055400648/',
        # 英郡二期
        'http://cd.lianjia.com/ershoufang/c3011055399653/',
        # 华润二十四城一期
        'http://cd.lianjia.com/ershoufang/pg1c3011054427433/',
        'http://cd.lianjia.com/ershoufang/pg2c3011054427433/',
        'http://cd.lianjia.com/ershoufang/pg3c3011054427433/',
        # 华润二十四城二期
        'http://cd.lianjia.com/ershoufang/pg1c3011055110938/',
        'http://cd.lianjia.com/ershoufang/pg2c3011055110938/',
        'http://cd.lianjia.com/ershoufang/pg3c3011055110938/',
        'http://cd.lianjia.com/ershoufang/pg4c3011055110938/',
        # 华润二十四城三期
        'http://cd.lianjia.com/ershoufang/pg1c3011055107784/',
        'http://cd.lianjia.com/ershoufang/pg2c3011055107784/',
        # 桐梓林壹号
        'http://cd.lianjia.com/ershoufang/c1611051173541/',
        # 中德英伦联邦A区
        'http://cd.lianjia.com/ershoufang/pg1c1611059031041/',
        'http://cd.lianjia.com/ershoufang/pg2c1611059031041/',

        # 中德英伦联邦B区
        'http://cd.lianjia.com/ershoufang/c1611061209751/',
        # 仁和春天国际花园
        'http://cd.lianjia.com/ershoufang/c1611047388205',
        # 时代晶科名苑
        'http://cd.lianjia.com/ershoufang/c1611043113553/',
        # 中海龙湾半岛
        'http://cd.lianjia.com/ershoufang/pg1c1611041535394/',
        'http://cd.lianjia.com/ershoufang/pg2c1611041535394/',
        'http://cd.lianjia.com/ershoufang/pg3c1611041535394/',
        'http://cd.lianjia.com/ershoufang/pg4c1611041535394/',
        # 中铁西子香荷
        'http://cd.lianjia.com/ershoufang/c1611041555455/',
        # 朗基龙堂
        'http://cd.lianjia.com/ershoufang/pg1c1611041619788/',
        'http://cd.lianjia.com/ershoufang/pg2c1611041619788/',
        # 南城都汇汇翠园一期
        'http://cd.lianjia.com/ershoufang/pg1c1611047102608/',
        'http://cd.lianjia.com/ershoufang/pg2c1611047102608/',
        # 南城都汇汇雅园二期
        'http://cd.lianjia.com/ershoufang/pg1c1611043169737/',
        'http://cd.lianjia.com/ershoufang/pg2c1611043169737/',
        # 南城都汇汇馨园三期
        'http://cd.lianjia.com/ershoufang/c1611047199429/',
        # 南城都汇汇尚园四期
        'http://cd.lianjia.com/ershoufang/c1611047199430/',
        # 中海兰庭
        'http://cd.lianjia.com/ershoufang/c1611047737374/',
    ]

    # 解析的方法，调用的时候传入从每一个url传回的response对象作为唯一参数，负责解析并获取抓取的数据(解析为item)，跟踪更多的url
    def parse(self, response):
        sel = Selector(response)
        xiaoqu_uri = sel.xpath('//span[@class="title"]/a/@href').extract()[0]
        xiaoqu_list = xiaoqu_uri.split('/')
        xiaoqu_id   = xiaoqu_list[2]
        items = []
        house_lists = sel.xpath('//div[@class="list-wrap"]/ul[@class="house-lst"]/li')
        for house in house_lists:
            item = SpiderScrapyLianjiaItem()
            item['xiaoqu_id']   = xiaoqu_id
            item['house_id']    = house.xpath('@data-id').extract()[0]
            item['title']       = house.xpath('div[@class="info-panel"]/h2/a/text()').extract()[0]
            item['price']       = house.xpath('div[@class="info-panel"]/div[@class="col-3"]/div[@class="price"]/span/text()').extract()[0]
            item['view_count']  = house.xpath('div[@class="info-panel"]/div[@class="col-2"]/div[@class="square"]/div/span/text()').extract()[0]
            #item['size']        = house.xpath('div[@class="info-panel"]/div[@class="col-1"]/div[@class="where"]/span/text()').extract()
            items.append(item)

        return items


