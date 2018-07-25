# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider


class AmazonSpider(RedisCrawlSpider):
    name = 'amazon'
    allowed_domains = ['amazon.cn']
    # start_urls = ['https://www.amazon.cn/图书/b/ref=sd_allcat_books_l1?ie=UTF8&node=658390051']
    redis_key = "amazon"

    rules = (
        Rule(LinkExtractor(restrict_xpaths=["//ul[@class='a-unordered-list a-nostyle a-vertical s-ref-indent-one']/div/li"]), follow=True),
        Rule(LinkExtractor(restrict_xpaths=["//ul[@class='a-unordered-list a-nostyle a-vertical s-ref-indent-two']/div/li"]), callback="parse_item" ),
        Rule(LinkExtractor(restrict_xpaths=["//span[@class='pagnLink']"]), follow=True),
    )

    def parse_item(self, response):
        item = {}
        li_list = response.xpath("//div[@class='a-row s-result-list-parent-container']/ul/li")
        for li in li_list:
            item["cate_url"] = response.url
            item["book_name"] = li.xpath(".//div[@class='a-row a-spacing-none']/a/h2/text()").extract_first()
            item["book_img"] = li.xpath(".//div[@class='a-column a-span12 a-text-center']/a/img/@src").extract_first()
            item["book_author"] = li.xpath(".//div[@class='a-row a-spacing-small']/div[2]/span/text()").extract()
            item["book_price"] = li.xpath(".//div[@class='a-column a-span7']/div[2]/a/span/text()").extract_first()
            item["book_url"] = li.xpath(".//div[@class='a-row a-spacing-none']/a/@href").extract_first()

            yield item












