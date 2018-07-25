# -*- coding: utf-8 -*-
import random,scrapy
from selenium import webdriver
import time


class RandomUserAgent(object):

    def process_request(self, request, spider):
        if spider.name == "tb":
            useragent_list = ["Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36",
                       "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36",
                       "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
                       "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"]
            ua = random.choice(useragent_list)
            request.headers["User-Agent"] = ua


class ShowUserAgent(object):

    def process_response(self,request,response,spider):
        pass
        print("身份标示为：",request.headers["User-Agent"])
        return  response


class StartUrlsSelenium(object):

    def process_request(self,request,spider):

        if request.url == "http://www.renren.com/":
            # opt = webdriver.ChromeOptions()
            # opt.add_argument('--headless')
            # opt.add_argument('--disable-gpu')
            # driver = webdriver.Chrome(chrome_options=opt)
            driver = webdriver.Chrome()
            driver.get(request.url)
            driver.find_element_by_id("email").send_keys("13972749880")
            driver.find_element_by_id("password").send_keys("qq110625")
            driver.find_element_by_id("login").click()

            return spider.parse(driver.page_source)





