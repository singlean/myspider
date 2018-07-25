# -*- coding: utf-8 -*-
import scrapy,re
from myScrapy.items import SNItem
from copy import deepcopy


class SnbookSpider(scrapy.Spider):
    name = 'snbook'
    allowed_domains = ['suning.com']
    start_urls = ['https://snbook.suning.com/web/trd-fl/999999/0.htm']

    # 首页解析函数，获取所有大分类名字，小分类名字和url地址
    def parse(self, response):
        # 获取分组
        li_list = response.xpath("//ul[@class='ulwrap']/li")
        for li in li_list:
            # 创建一个item对象
            items = SNItem()
            # 大分类名
            items["second_type"] = li.xpath("./div[1]/a/text()").extract_first()
            # 小分类列表
            a_list = li.xpath("./div[2]/a")
            for a in a_list:
                # 小分类url
                items["three_type_url"] = a.xpath("./@href").extract_first()
                items["three_type_url"] = "https://snbook.suning.com" + items["three_type_url"]
                # 小分类名
                items["three_type_name"] = a.xpath("./text()").extract_first()

                # 请求小分类中图书的信息
                yield scrapy.Request(
                    items["three_type_url"],
                    callback = self.parse_book_type,
                    meta = {"items":deepcopy(items)}
                )

    # 获取小分类中的图书信息
    def parse_book_type(self,response):
        # 获取分类名及url
        items = response.meta["items"]
        # 获取分组
        li_list = response.xpath("//div[@class='filtrate-books list-filtrate-books']/ul/li")
        for li in li_list:
            # 图书url，书名，作者，出版社，简介
            items["book_url"] = li.xpath("./div[@class='book-img']/a/@href").extract_first()
            # items["book_img"] = li.xpath("./div[@class='book-img']/a/img/@src").extract_first()
            items["book_title"] = li.xpath("./div[@class='book-img']/a/img/@alt").extract_first()
            items["book_author"] = li.xpath(".//div[@class='book-author']/a/text()").extract_first()
            items["book_publish"] = li.xpath(".//div[@class='book-publish']/a/text()").extract_first()
            items["book_synopsis"] = li.xpath(".//div[@class='book-descrip c6']/text()").extract_first()

            # 获取图书信息
            yield scrapy.Request(
                items["book_url"],
                callback = self.parse_book_detail,
                meta = {"items":deepcopy(items)}
            )

        # 下一页url地址
        next_url = items["three_type_url"] + "?pageNumber={}"
        # 总页数和当前页
        page_count = int(re.findall(r"var pagecount=(\d+);",response.body.decode())[0])
        current_page = int(re.findall(r"var currentPage=(\d+);",response.body.decode())[0])

        # 判断是否有下一页，有就继续请求
        if current_page < page_count:
            yield scrapy.Request(
                next_url.format(current_page+1),
                callback=self.parse,
                meta = {"items":items}  # 传递这个分类的大小分类名和小分类url地址
            )

    # 去详情页获取图片和价格信息
    def parse_book_detail(self,response):
        items = response.meta["items"]
        items["book_img"] = response.xpath("//dl[@class='brief-img fl']/dt/img/@src").extract_first()
        items["book_price"] = re.findall(r"\"bp\":'(.+)',",response.body.decode())[0]

        yield items


















