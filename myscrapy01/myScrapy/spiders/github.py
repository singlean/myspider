# -*- coding: utf-8 -*-
import scrapy


class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']
    start_urls = ['https://kyfw.12306.cn/otn/login/init']

    def parse(self, response):
        验证码 = "https://kyfw.12306.cn/passport/captcha/captcha-check"
        响应地址 = "https://kyfw.12306.cn/passport/web/login"


print(dir("a"))


