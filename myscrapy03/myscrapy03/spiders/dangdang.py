# -*- coding: utf-8 -*-
import scrapy,re
from scrapy_redis.spiders import RedisSpider
from copy import deepcopy
from urllib.parse import urljoin
from pprint import pprint


# 继承redisspider类，让爬虫实现分布式功能
class DangdangSpider(RedisSpider):
    name = 'dangdang'
    allowed_domains = ["category.dangdang.com","book.dangdang.com","product.dangdang.com"]
    # start_urls = ['http://book.dangdang.com/']
    # 在redis中获取start_urls，未获取到就等待
    redis_key = "dangdang"

    def parse(self, response):
        # 一级分类列表
        div_list = response.xpath("//div[@class='con flq_body']/div[@class='level_one ']")
        for div in div_list:
            items = {}
            items["level_one"] = div.xpath("./dl/dt//text()").extract()
            items["level_one"] = [i.strip() for i in items["level_one"] if len(i.strip())]
            # 二级分类列表
            dl_list = div.xpath("./div//dl[@class='inner_dl']")
            for dl in dl_list:
                items["level_two"] = dl.xpath("./dt//text()").extract()
                items["level_two"] = [i.strip() for i in items["level_two"] if len(i.strip())]
                # 三级分类列表
                a_list = dl.xpath("./dd/a")
                for a in a_list:
                    items["level_three"] = a.xpath("./text()").extract_first().strip()
                    items["level_three_href"] = a.xpath("./@href").extract_first()

                    # 根据域名决定调用那个方法
                    book = re.findall(r"(book\.dangdang\.com)",str(items["level_three_href"]))
                    category = re.findall(r"(category\.dangdang\.com)",str(items["level_three_href"]))
                    if book:
                        callfunc = self.parse_book_list
                    elif category:
                        callfunc = self.parse_category_list
                    else:
                        continue
                    # 请求图书列表页
                    yield scrapy.Request(
                        url=items["level_three_href"],
                        callback=callfunc,
                        meta = {"items":deepcopy(items)}
                    )

    def parse_book_list(self,response):
        items = response.meta["items"]
        # 图书分类
        li_list = response.xpath("//ul[@class='list_aa ']/li")
        for li in li_list:
            items["book_img"] = li.xpath("./a[@class='img']/img/@data-original").extract_first()
            items["book_url"] = li.xpath("./p[@class='name']/a/@href").extract_first()

            yield scrapy.Request(
                url=items["book_url"],
                callback=self.parse_book_detail,
                meta={"items":deepcopy(items)}
            )

    def parse_book_detail(self,response):
        items = response.meta["items"]
        items["book_name"] = response.xpath("//div[@class='name_info']/h1/@title").extract_first()
        items["book_price"] = response.xpath("//p[@id='dd-price']/text()").extract()
        items["book_price"] = [i.strip() for i in items["book_price"] if len(i.strip())]
        items["book_author"] = response.xpath("//span[@id='author']/a/text()").extract_first()
        items["book_press"] = response.xpath("//a[@dd_name='出版社']/text()").extract_first()
        items["book_publish_date"] = response.xpath("//div[@class='messbox_info']/span[3]/text()").extract_first()

        yield items

    def parse_category_list(self,response):
        items = response.meta["items"]
        # 图书分类
        li_list = response.xpath("//ul[@class='bigimg']/li")
        for li in li_list:
            items["book_img"] = li.xpath("./a[@class='pic']/img/@data-original").extract_first()
            items["book_url"] = li.xpath("./p[@class='name']/a/@href").extract_first()
            items["book_name"] = li.xpath("./p[@class='name']/a/text()").extract_first()
            items["book_detail"] = li.xpath("./p[@class='detail']/text()").extract()
            items["book_price"] = li.xpath(".//span[@class='search_now_price']/text()").extract_first()
            items["book_author"] = li.xpath("./p[@class='search_book_author']/span[1]/a/text()").extract()
            items["book_press"] = li.xpath("./p[@class='search_book_author']/span[3]/a/text()").extract_first()
            items["book_publish_date"] = li.xpath("./p[@class='search_book_author']/span[2]/text()").extract_first()

        yield items








