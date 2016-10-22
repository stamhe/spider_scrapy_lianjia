# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class SpiderScrapyLianjiaItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    xiaoqu_id   = Field()       # 小区id
    house_id    = Field()       # 链家房源编号
    title       = Field()       # 标题
    price       = Field()       # 价格
    #size        = Field()       # 面积
    view_count  = Field()       # 带看次数

class SpiderChenshiItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    chenshi_name    = Field()       # 城市名
    avg_price       = Field()       # 城市均价
    onsale_count    = Field()       # 在售套数
    sold_last_month = Field()       # 上个月成交套数
    view_last_day   = Field()       # 昨日带看次数
