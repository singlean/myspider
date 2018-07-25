import requests,re
from lxml import etree
import json


class Blblspider:

    def __init__(self):
        # 哔哩哔哩首页url
        self.start_url = "https://www.bilibili.com/"
        self.url = "https://www.bilibili.com/video/av25261467/"
        self.dm_url = "https://api.bilibili.com/x/v1/dm/list.so?oid={}"
        self.headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}

    def get_url(self):
        return self.url

    def get_result(self,url):
        print(url)
        return requests.get(url,headers=self.headers).content.decode()

    def get_content(self,cid):
        ret_str = self.get_result(self.dm_url.format(cid))
        ret_html = etree.HTML(ret_str.encode())
        d_list = ret_html.xpath("//d")
        items = {}
        for d in d_list:
            con = d.xpath("./text()")
            items[d_list.index(d)] = con[0]

        return items

    def save_content(self,items):
        with open("bibi.json","w") as f:
            f.write(json.dumps(items,ensure_ascii=False,indent=2))

    def run(self):
        # 准备url
        url = self.get_url()
        # 发送请求，获取响应
        html_str = self.get_result(url)
        # 提取数据
        cid = re.findall(r"cid=(\d+)",html_str)[1]
        items = self.get_content(cid)
        # 保存数据
        self.save_content(items)


class BlbiPageSpider:
    """未完成的哔哩哔哩爬虫"""

    # 初始化
    def __init__(self):
        # 哔哩哔哩首页url
        self.start_url = "https://www.bilibili.com/"
        # 弹幕url
        self.danmu_url = "https://api.bilibili.com/x/v1/dm/list.so?oid={}"
        # 需要拼接的url头
        self.url_head = "https://www.bilibili.com"
        # 身份信息
        self.headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}

    # 获取响应的html字符串
    def get_html(self, url):
        print(url)
        return requests.get(url, headers=self.headers).content.decode()

    # 获取url列表
    def get_url_list(self):
        # 发送请求，获取首页的html字符串信息
        html_str = self.get_html(self.start_url)
        # 转换为etree对象，并将每一个页面分组
        html = etree.HTML(html_str)
        li_list = html.xpath("//div[@id='primary_menu']/ul/li")
        # 设置url列表
        url_list = []
        # 对分组循环，获取每一个页面的信息
        for li in li_list:
            item = {}
            # 拼接出完整的页面url并获取页面的标题
            item["href"] = "https:" + li.xpath("./a/@href")[0]
            item["title"] = li.xpath(".//div/text()")[0] if len(li.xpath(".//div/text()")) else None
            print(item["title"])
            url_list.append(item)
        # 返回页面的url列表
        return url_list

    # 获取每一页的视频url列表
    def get_page_tv_list(self,url_dict):
        # 请求每一个页面，获取页面html响应
        url = url_dict["href"]
        html_str = self.get_html(url)
        # 获取页面标题
        page_title = url_dict["title"]
        # 转换为etree对象
        html = etree.HTML(html_str)

        # 判断市那个页面而觉得怎样获取分组
        if page_title == "首页":
            div_list = html.xpath("//div[@class='groom-module home-card']")
        elif page_title == "动画":
            div_list = html.xpath("//div[@class='groom-module']")
        else:
            return []
        # 每一页的视频列表
        page_tv_list = []
        # 获取单个视频的信息
        for div in div_list:
            item = {}
            item["title"] = div.xpath("./a/@title")[0]  # 视频标题
            item["author"] = div.xpath(".//p[@class='author']/text()")[0]  # 视频作者
            item["play"] = div.xpath(".//p[@class='play']/text()")[0]  # 点击数
            item["href"] = self.url_head + div.xpath("./a/@href")[0]  # 完整的视频url
            item["page_title"] = page_title  # 那个页面的视频
            page_tv_list.append(item)  # 页面视频列表
        # 返回每一页的视频信息列表
        return page_tv_list

    # 获取单个视频的弹幕信息
    def get_content_dict(self,page_tv_dict):
        # 获取单个视频的响应
        html_str = self.get_html(page_tv_dict["href"])
        # 获取cid
        cid = re.findall(r"cid=(\d+)",html_str)[1]
        # 获取弹幕响应
        ret_html = self.get_html(self.danmu_url.format(cid))
        # 转换为etree对象并对每一弹幕节点分组
        dm_html = etree.HTML(ret_html.encode())
        d_list = dm_html.xpath("//d")
        # 将单个视频的弹幕信息保存到一个字典中
        items = {}
        # 获取每一条弹幕
        for d in d_list:
            con = d.xpath("./text()")
            items[d_list.index(d)] = con[0]
        # 添加视频的标题，作者，点击数，ｕｒｌ，页面信息
        items["title"] =page_tv_dict["title"]
        items["author"] = page_tv_dict["author"]
        items["play"] = page_tv_dict["play"]
        items["url"] = page_tv_dict["href"]
        items["page_title"] = page_tv_dict["page_title"]

        return items

    # 保存单个页面的所有视频弹幕信息
    def save_content_list(self,content_list):
        # 获取页面标题
        if content_list:
            page_title = content_list[0]["page_title"]
        else:
            return
        # 保存为json文件
        with open("./demo/bibi"+page_title + ".json","w") as f:
            f.write(json.dumps(content_list,ensure_ascii=False,indent=2))

    def run(self):
        # 准备url列表
        url_list = self.get_url_list()
        # 循环每一个url列表获取每一个包含url信息的字典
        for url_dict in url_list:
            # 发送请求，获取每页下的弹幕视频的url列表
            page_tv_list = self.get_page_tv_list(url_dict)
            # 将每一页的弹幕信息都保存到一个列表中
            page_tv_danmu_list = []
            # 发送请求，获取弹幕信息
            for page_tv_dict in page_tv_list:
                # 获取每一个视频的弹幕信息
                content_dict = self.get_content_dict(page_tv_dict)
                # 添加到此页面的弹幕列表中
                page_tv_danmu_list.append(content_dict)
            # 将每一页的弹幕写入到本地
            self.save_content_list(page_tv_danmu_list)


bibi = BlbiPageSpider()
bibi.run()








































