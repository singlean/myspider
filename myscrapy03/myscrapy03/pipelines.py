# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

class Myscrapy03Pipeline(object):

    def open_spider(self,spider):
        # 创建一个mongo客户端对象
        client = MongoClient()
        # 创建一个集合保存数据
        self.collection = client["spider"]["jdbook"]

    def process_item(self, item, spider):
        if spider.name == "jdbook":
            # 像集合中添加数据
            self.collection.insert(dict(item))
            print("保存成功")
        return item


# 当当网图书爬虫
class MyDangDangPipeline(object):

    def open_spider(self,spider):
        # 创建一个mongo客户端对象
        client = MongoClient()
        # 创建一个集合保存数据
        self.collection = client["spider"]["dangdang"]

    def process_item(self, item, spider):
        if spider.name == "dangdang":
            # 像集合中添加数据
            self.collection.insert(dict(item))
            print("保存成功")
        return item


# 当当网图书爬虫
class MyAmazonPipeline(object):

    def open_spider(self,spider):
        # 创建一个mongo客户端对象
        client = MongoClient()
        # 创建一个集合保存数据
        self.collection = client["spider"]["amazon"]

    def process_item(self, item, spider):
        if spider.name == "amazon":
            # 像集合中添加数据
            self.collection.insert(dict(item))
            print("保存成功")
        return item




