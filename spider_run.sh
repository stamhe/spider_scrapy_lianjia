#!/bin/bash
# @hequan
# 批量启动爬虫
workdir=/root/hequan/spider_scrapy_lianjia/spider_scrapy_lianjia
cd ${workdir}
#/usr/bin/python /usr/local/python/bin/scrapy crawl lianjia_house_spider
#/usr/bin/python /usr/local/python/bin/scrapy crawl chenshi_count_spider
#/usr/bin/python /usr/local/bin/scrapy crawl dianping_gym_spider
/usr/bin/python /usr/local/bin/scrapy crawl dianping_xmt_baby_spider
/usr/bin/python /usr/local/bin/scrapy crawl dianping_xmt_spider


