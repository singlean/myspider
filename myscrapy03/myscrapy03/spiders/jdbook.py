# -*- coding: utf-8 -*-
import scrapy,re
import json
from copy import deepcopy
from pprint import pprint
from urllib.parse import urljoin


class JdbookSpider(scrapy.Spider):
    name = 'jdbook'
    allowed_domains = ['list.jd.com','p.3.cn']
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):

        dt_list = response.xpath("//div[@class='mc']/dl/dt")
        for dt in dt_list:
            item = {}
            item["s_cate"] = dt.xpath("./a/text()").extract_first()
            em_list = dt.xpath("./following-sibling::dd[1]/em")

            for em in em_list:
                item["b_cate"] = em.xpath("./a/text()").extract_first()
                item["b_href"] = "https:" + em.xpath("./a/@href").extract_first()

                yield scrapy.Request(
                    item["b_href"],
                    callback = self.parse_book_list,
                    meta = {"item":deepcopy(item)}
                )

    def parse_book_list(self,response):
        item = response.meta["item"]
        li_list = response.xpath("//li[@class='gl-item']")
        for li in li_list:
            item["book_img"] = li.xpath(".//div[@class='p-img']//img/@src").extract_first()
            if item["book_img"] is None:
                item["book_img"] = li.xpath(".//div[@class='p-img']/a/img/@data-lazy-img").extract_first()
            item["book_img"] = "https:" + item["book_img"]
            item["book_url"] = "https:" + li.xpath(".//div[@class='p-img']/a/@href").extract_first() if len(li.xpath(".//div[@class='p-img']/a/@href").extract_first()) else None
            item["book_name"] = li.xpath(".//div[@class='p-name']//em/text()").extract_first().strip()
            item["publish"] = li.xpath(".//span[@class='p-bi-store']/a/text()").extract_first()
            item["pud_date"] = li.xpath(".//span[@class='p-bi-date']/text()").extract_first().strip()
            item["book_sku"] = re.findall(r"(\d+)",item["book_url"])[0]

            detail_url = "https://p.3.cn/prices/mgets?skuIds=J_{}".format(item["book_sku"])
            yield scrapy.Request(
                detail_url,
                self.parse_book_price,
                meta = {"item":deepcopy(item)}
            )

        next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_url is not None:
            next_url = urljoin(response.url,next_url)
            print(next_url)
            yield scrapy.Request(
                next_url,
                callback=self.parse_book_list,
                meta={"item":item}
            )


    def parse_book_price(self,response):
        item = response.meta["item"]
        price = json.loads(response.body.decode())
        item["book_price"] = price[0]["op"]


        yield item


































