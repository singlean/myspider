# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class Myscrapy02Pipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'tb':
            with open("./tb.txt","a") as f:
                # print(item)
                f.write(str(item))
                f.write("\n")
                f.write("\n")
                # print("保存成功")
        return item
