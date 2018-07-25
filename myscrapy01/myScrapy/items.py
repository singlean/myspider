# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# yg爬虫的item类，
class YGItem(scrapy.Item):

    # define the fields for your item here like:
    title = scrapy.Field()  # 标题
    href = scrapy.Field()  # 帖子的url
    publish_data = scrapy.Field()  # 时间
    content = scrapy.Field()  # 文本内容
    content_img = scrapy.Field()  # 文本中的图片

# 苏宁爬虫的item类
class SNItem(scrapy.Item):

    second_type = scrapy.Field()  # 大分类
    three_type_url = scrapy.Field()  # 小分类url
    three_type_name = scrapy.Field()  # 小分类标题
    book_title = scrapy.Field()  # 书名
    book_img = scrapy.Field()  # 图书图片
    book_url = scrapy.Field()  # 图书url
    book_author = scrapy.Field()  # 作者
    book_synopsis = scrapy.Field()  # 图书简介
    book_publish = scrapy.Field()  # 出版社
    book_price = scrapy.Field()  # 价格
















