# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class HouseSpiderPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = "127.0.0.1:27017"
        self.mongo_db = "house"

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection_name = item.__class__.__name__
        print("****************************************")
        if (self.db[collection_name].find({"link": item["link"]}).count()):
            print(1)
            self.db[collection_name].update({"link": item["link"]}, dict(item))
        else:
            print(2)
            self.db[collection_name].insert(dict(item))
        # self.db[collection_name].insert(dict(item))
        return item