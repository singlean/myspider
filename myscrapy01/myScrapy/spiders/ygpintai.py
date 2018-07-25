# -*- coding: utf-8 -*-
import scrapy
from myScrapy.items import YGItem


class YGPinTaiSpider(scrapy.Spider):
    name = 'yg'
    allowed_domains = ['sun0769.com']
    start_urls = ['http://wz.sun0769.com/index.php/question/questionType?type=4&page=0']

    # 解析函数，提取数据
    def parse(self, response):
        tr_list = response.xpath("//div[@class='greyframe']/table[2]/tr/td/table/tr")
        for tr in tr_list:
            item = YGItem()
            item["title"] = tr.xpath("./td[2]/a[@class='news14']/text()").extract_first()
            item["href"] = tr.xpath("./td[2]/a[@class='news14']/@href").extract_first()
            item["publish_data"] = tr.xpath("./td[@class='t12wh']/text()").extract_first()

            # 去详情页获取需要的数据
            yield scrapy.Request(
                item["href"],
                callback = self.parse_detail,
                meta = {"item":item}
            )

        # 判断是否有下一页决定是否继续发送请求
        next_url = response.xpath("//a[text()='>']/@href").extract_first()
        if next_url is not None:
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )

    # 详情页解析函数，获取详情页数据
    def parse_detail(self,response):
        item = response.meta["item"]
        item["content"] = response.xpath("//div[@class='c1 text14_2']/text()").extract()
        item["content_img"] = response.xpath("//div[@class='c1 text14_2']/div[@class='textpic']/img/@src").extract()
        item["content_img"] = ["http://wz.sun0769.com" + i for i in item["content_img"]]

        yield item
























