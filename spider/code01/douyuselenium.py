from selenium import webdriver
import json
import time

class DouyuSpider:

    # 初始化
    def __init__(self):
        # 创建一个浏览器对象
        self.driver = webdriver.Chrome()
        # 请求的url
        self.url = "https://www.douyu.com/directory/game/yz"

    # 发送请求，获取html响应
    def get_html_str(self):
        self.driver.get(self.url)

    # 获取数据
    def get_content(self):
        # 将单个房间分组
        li_list = self.driver.find_elements_by_xpath("//ul[@id='live-list-contentbox']/li")
        content_list = []
        # 获取房间信息
        for li in li_list:
            item = {}
            item["author_name"] = li.find_element_by_xpath(".//span[@class='dy-name ellipsis fl']").text
            item["img_src"] = li.find_element_by_xpath(".//span[@class='imgbox']/img").get_attribute("src")
            item["watch_number"] = li.find_element_by_xpath(".//span[@class='dy-num fr']").text
            item["room_cate"] = li.find_element_by_xpath(".//span[@class='tag ellipsis']").text
            content_list.append(item)
        # 返回需要保存的数据列表
        return content_list

    # 保存数据
    def save_content(self,content_list):
        with open("./demo/douyu.json","w") as f:
            f.write(json.dumps(content_list,ensure_ascii=False,indent=2))

    def run(self):
        # 准备url
        # 发送请求，获取响应
        self.get_html_str()
        # 提取数据
        content_list = self.get_content()
        # 保存数据
        self.save_content(content_list)
        # 关闭浏览器对象
        self.driver.quit()


douyu = DouyuSpider()
douyu.run()


