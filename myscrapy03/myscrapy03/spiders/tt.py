# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TtSpider(CrawlSpider):
    name = 'tt'
    allowed_domains = ['tencent.com']
    start_urls = ['https://hr.tencent.com/position.php']

    rules = (
        # 正则匹配url，callback指定处理函数，follow控制是否需要对抓取到的url返回的响应继续抓取url
        Rule(LinkExtractor(allow=r'position_detail\.php\?id=\d+&keywords=&tid=0&lid=0'), callback='parse_item'),
        Rule(LinkExtractor(allow=r'position\.php\?&start=\d+#a'),follow=True)
    )

    def parse_item(self, response):
        item = {}
        item["addr"] = response.xpath("//tr[@class='c bottomline']/td[1]/text()").extract_first()
        item["num"] = response.xpath("//tr[@class='c bottomline']/td[3]/text()").extract_first()
        item["duty"] = response.xpath("//ul[@class='squareli']/li/text()").extract()[0]
        item["demand"] = response.xpath("//ul[@class='squareli']/li/text()").extract()[1]

        print(item)
