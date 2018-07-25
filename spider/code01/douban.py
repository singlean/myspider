import requests
import json


# url = "https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_domestic_hot/items?os=ios&start={}&count={}"
# headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
#            "Referer": "https://m.douban.com/tv/chinese"}
#
# response = requests.get(url,headers=headers)
#
# ret_str = response.content.decode()
# ret_str = json.loads(ret_str)
# total = ret_str["total"]
# print(total)

# with open("./douban.json","w") as f:
#     f.write(json.dumps(ret_str,ensure_ascii=False,indent=2))


class Douban:
    "爬取豆瓣电视剧信息"

    def __init__(self,tv_type):
        self.start = 0
        self.count = 49
        self.cease = False
        # 国产０、动漫１、韩剧２
        self.type = tv_type
        self.headers = [
            {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
            "Referer": "https://m.douban.com/tv/chinese"},
            {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
            "Referer": "https://m.douban.com/tv/animation"},
            {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
            "Referer": "https://m.douban.com/tv/korean"},
        ]

    def get_url(self):
        # 设置url地址
        url = ["https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_domestic_hot/items?os=ios&start={}&count={}&loc_id=108288".format(self.start, self.count),
               "https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_animation_hot/items?os=ios&start={}&count={}&loc_id=108288".format(self.start, self.count),
               "https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_korean_drama_hot/items?os=ios&start={}&count={}&loc_id=108288".format(self.start, self.count)]

        return url

    def page_handle(self, url):
        # 获取请求，返回响应
        response = requests.get(url, headers=self.headers[self.type])
        ret_str = response.content.decode()
        ret_str = json.loads(ret_str)
        # 判断总共有多少条数据
        total = ret_str["total"]

        if self.start < total:
            self.start += 18
        else:
            self.cease = True
        return ret_str

    def preserve_json(self, str):
        if self.type == 0:
            tv = "国产剧"
        elif self.type == 1:
            tv = "动漫"
        elif self.type == 2:
            tv = "韩剧"
        else:
            tv = "电视剧"
        with open("./tv/{}－第{}页.json".format(tv,self.start // 18), "w") as f:
            f.write(json.dumps(str, ensure_ascii=False, indent=2))

    def run(self):
        # 发送请求
        while not self.cease:
            # 获取url
            url = self.get_url()
            # 发送请求，获取响应
            ret_str = self.page_handle(url[self.type])
            # 保存到本地
            self.preserve_json(ret_str)


class DoubanSpider:

    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"}
        self.url_list = [
            {"url_temp": "https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_domestic_hot/items?start={}&count=50&loc_id=108288",
             "Referer": "https://m.douban.com/tv/chinese",
             "type": "国产剧"},
            {"url_temp": "https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_animation_hot/items?start={}&count=50&loc_id=108288",
             "Referer": "https://m.douban.com/tv/animation",
             "type": "动漫"},
            {"url_temp":"https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_korean_drama_hot/items?start={}&count=50&loc_id=108288",
             "Referer": "https://m.douban.com/tv/korean",
             "type": "韩剧"}
            ]

    # 获取每一次的url地址
    def get_url(self,start,url_dict):
        url = url_dict["url_temp"].format(start)
        return url

    # 发送请求获取响应
    def get_ret(self,url,url_dict):
        referer = url_dict["Referer"]
        self.headers["Referer"] = referer
        response = requests.get(url,headers=self.headers)
        return response.content.decode()

    # 获取需要保存的数据
    def get_items(self,str):
        dict_str = json.loads(str)  # 转换为ｐｙ格式的字符串
        total = dict_str["total"]  # 电影总条数
        dict_items = dict_str["subject_collection_items"]  # 需要保存的电影条数内容
        return total,dict_items

    # 保存到本地
    def preserve_json(self, dict_items,start,url_dict):
        tv_type = url_dict["type"]
        with open("./tv/{}－第{}页.json".format(tv_type,(start+18) // 18), "w") as f:
            f.write(json.dumps(dict_items, ensure_ascii=False,indent=2))

    # 实现主要逻辑
    def run(self):
        # url准备
        for url_dict in self.url_list:
            start = 0 # 设置开始页码
            while True:  # 无线循环
                url = self.get_url(start,url_dict)  # 获取每一次的url地址
                str = self.get_ret(url,url_dict)  # 发送请求，获取响应
                total,dict_items = self.get_items(str)  # 提取数据，总数和需要保存的电影条数
                self.preserve_json(dict_items,start,url_dict)  # 保存数据
                start += 18  # 页码加１
                if len(dict_items) < 50:  # 判断数据长度确定是否继续循环，电影条数小于18结束循环
                    break


douban = DoubanSpider()
douban.run()

























