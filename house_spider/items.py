# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DmozItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()

class FangddItem(DmozItem):
	price = scrapy.Field()
	address = scrapy.Field()
	region = scrapy.Field()
	style = scrapy.Field()
	time_open = scrapy.Field()
	time_end = scrapy.Field()
	areaList = scrapy.Field()
	decoration = scrapy.Field()