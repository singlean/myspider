# -*- coding: utf-8 -*-
import scrapy
import re
from urllib.parse import urljoin


class TbSpider(scrapy.Spider):
    name = 'tb'
    allowed_domains = ['tieba.baidu.com']
    start_urls = ['https://tieba.baidu.com/mo/q---C0143C6B306C1DC9E47E62DE5798A4FA%3AFG%3D1--1-3-0----wapp_1530331985676_337/m?kw=%E5%9B%BE%E7%89%87&lp=5011&lm=&pinf=1_2_200&pn=0']

    def parse(self, response):

        div_list = response.xpath("//div[contains(@class,'i')]")

        for div in div_list:
            item = {}
            item["detail_img"] = []
            item["href"] = div.xpath("./a/@href").extract_first()
            item["title"] = div.xpath("./a/text()").extract_first()
            item["title"] = re.sub(r"\xa0","",item["title"])

            if item["href"]:
                item["href"] = urljoin(response.url,item["href"])
                # print(item["href"])
                yield scrapy.Request(
                    item["href"],
                    callback = self.parse_detail,
                    meta = {"item":item}
                )

        next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_url is not None:
            next_url = urljoin(response.url,next_url)
            # print(next_url)
            # print(next_url)
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )

    def parse_detail(self,response):
        item = response.meta["item"]
        img_list = response.xpath("//div[@class='d']/div[@class='i']/a[text()='图']/@href").extract()
        for img in img_list:
            if img:
                item["detail_img"].append(img.split("?")[0])

        next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_url is not None:
            next_url = urljoin(response.url,next_url)
            yield scrapy.Request(
                next_url,
                callback = self.parse_detail,
                meta = {"item":item}
            )

        if not next_url:
            yield item

















