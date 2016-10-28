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

from spider_scrapy_lianjia.items import SpiderChenshiItem

class chenshi_spider(CrawlSpider):
    # 爬虫的识别名称，必须是唯一的，在不同的爬虫中你必须定义不同的名字
    name = "chenshi_count_spider"    # 设置爬虫名称

    # 搜索的域名范围，也就是爬虫的约束区域，规定爬虫只爬取这个域名下的网页
    allowed_domains = ["lianjia.com"] # 设置允许的域名

    # 爬取的url列表，爬虫从这里开始抓取数据，所以，第一次下载的数据将会从这些urls开始，其他子url将会从这些起始url中继承性生成
    start_urls = [
        # 成都
        'http://cd.lianjia.com/fangjia/',
        # 重庆
        'http://cq.lianjia.com/fangjia/',
        # 厦门
        'http://xm.lianjia.com/fangjia/',
        # 深圳
        'http://sz.lianjia.com/fangjia/',
        # 南京
        'http://nj.lianjia.com/fangjia/',
        # 武汉
        'http://wh.lianjia.com/fangjia/',
        # 广州
        'http://gz.lianjia.com/fangjia/',
        # 北京
        'http://bj.lianjia.com/fangjia/',
        # 杭州
        'http://hz.lianjia.com/fangjia/',
    ]

    # 解析的方法，调用的时候传入从每一个url传回的response对象作为唯一参数，负责解析并获取抓取的数据(解析为item)，跟踪更多的url
    def parse(self, response):
        url = response.url
        sel = Selector(response)
        item = SpiderChenshiItem()
        if url == 'http://cd.lianjia.com/fangjia/':
            item['chenshi_name'] = sel.xpath('//div[@class="view-con"]/div[@class="region"]/text()').extract()[0]
            # avg_price
            item['avg_price'] = sel.xpath('//div[@class="semid"]/div[@class="last"]/span[@class="style03"]/text()').extract()[0]
            # onsale_count
            x1 = sel.xpath('//div[@class="semid"]/div[@class="last"]/div[@class="nearday"]/p')
            x2 = x1[0].xpath('a/text()').extract()[0]
            # 提取x2中的数字
            x3 = re.findall("\d+", x2)
            item['onsale_count'] = x3[0]
            # sold_last_month
            item['sold_last_month'] = sel.xpath('//div[@class="bottom"]/div[@class="second fl"]/span/text()').extract()[0]
            # view_last_day
            item['view_last_day'] = sel.xpath('//div[@class="bottom"]/div[@class="third fl"]/span/text()').extract()[0]
        elif url == 'http://cq.lianjia.com/fangjia/' or url == 'http://xm.lianjia.com/fangjia/':
            item['chenshi_name'] = sel.xpath('//div[@class="view"]/div[@class="bg"]/div[@class="view-con"]/div/text()').extract()[0]
            # avg_price
            item['avg_price'] = sel.xpath('//div[@class="semid"]/div[@class="last"]/span[@class="style03"]/text()').extract()[0]
            # onsale_count
            x1 = sel.xpath('//div[@class="semid"]/div[@class="last"]/div[@class="nearday"]/p')
            x2 = x1[0].xpath('a/text()').extract()[0]
            # 提取x2中的数字
            x3 = re.findall("\d+", x2)
            item['onsale_count'] = x3[0]
            # sold_last_month
            item['sold_last_month'] = sel.xpath('//div[@class="bottom"]/div[@class="second fl"]/span/text()').extract()[0]
            # view_last_day
            item['view_last_day'] = sel.xpath('//div[@class="bottom"]/div[@class="third fl"]/span/text()').extract()[0]
        else:
            item['chenshi_name'] = sel.xpath('//div[@class="box-l-t"]/div[@class="shuju"]/div[@class="title"]/div[@class="tit"]/text()').extract()[0]

            # avg_price
            item['avg_price'] = sel.xpath('//div[@class="box-l-t"]/div[@class="qushi"]/div[@class="qushi-2"]/span[@class="num"]/text()').extract()[0]
            # onsale_count
            x1 = sel.xpath('//div[@class="box-l-t"]/div[@class="qushi"]/div[@class="qushi-2"]/span')
            x2 = x1[3].xpath('a')
            x3 = x2[0].xpath('text()').extract()[0]
            # 提取x3中的数字
            x4 = re.findall("\d+", x3)
            item['onsale_count'] = x4[0]
            # sold_last_month
            x1 = sel.xpath('//div[@class="box-l-b"]/div')
            if url == 'http://gz.lianjia.com/fangjia/':
                x2 = x1[1].xpath('div[@class="num"]/span')
                x3 = x2[0].xpath('text()').extract()[0]
                item['sold_last_month'] = x3
            else:
                x2 = x1[1].xpath('div[@class="num"]/span/text()').extract()[0]
                item['sold_last_month'] = x2
            # view_last_day
            x1 = sel.xpath('//div[@class="box-l-b"]/div')
            x2 = x1[2].xpath('div[@class="num"]/span/text()').extract()[0]
            item['view_last_day'] = x2

        return item


