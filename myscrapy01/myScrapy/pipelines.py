# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
from myScrapy.items import YGItem,SNItem
from pymongo import MongoClient

class MyscrapyPipeline(object):

    # 爬虫开启运行的函数
    def open_spider(self,spider):

        # 创建一个mongodb的链接
        client = MongoClient()
        self.collection = client["spider"]["ygpntai"]

    def process_item(self, item, spider):
        # 判断item的来源，是这个类的实例才做处理
        if isinstance(item,YGItem):
            content = item["content"]
            item["content"] = self.head_content(content)
            # item不是一个python的字典，保存需要进行数据类型转换
            self.collection.insert(dict(item))
            print("保存成功")

        return item

    # 对文本内容进行处理
    def head_content(self,content):
        contents = [re.sub(r"\xa0|\s","",i) for i in content]
        contents = [i for i in contents if len(i)]

        return contents


class MyscrapyPipelineSN(object):

    # 爬虫开启运行的函数
    def open_spider(self,spider):
        pass

    def process_item(self, item, spider):
        # 判断item的来源，是这个类的实例才做处理
        if isinstance(item,SNItem):
            # print(item)
            with open("./tet.txt","a") as f:
                f.write(str(item))
                f.write("\n")
                f.write("\n")
                print("保存成功")








