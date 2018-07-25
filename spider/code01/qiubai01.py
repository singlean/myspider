from lxml import etree
import requests
import json

class QiubaiSpider:

    def __init__(self):
        self.url = "https://www.qiushibaike.com/8hr/page/{}/"
        self.headers = {"user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}

    # 生产url列表
    def get_url_list(self):
        url_list = [self.url.format(i) for i in range(1,14)]
        return url_list

    # 发送请求，获取响应
    def get_result(self,url):
        response = requests.get(url,headers=self.headers)
        return response.content

    # 获取需要保存的内容
    def get_content(self,html_str):
        # 转换为etree对象
        html = etree.HTML(html_str)
        # 分组，获取段子的分组列表
        div_list = html.xpath("//div[@id='content-left']/div")
        content_list = []
        # 循环每一个段子获取数据
        for div in div_list:
            item = {}
            # 获取数据
            item["author_name"] = div.xpath("./div/a[2]/h2/text()")[0] if len(div.xpath("./div/a[2]/h2/text()")) else None
            item["author_sex"] = div.xpath(".//div[@class='author clearfix']/div/@class")
            item["author_sex"] = item["author_sex"][0].split(" ")[-1] if len(item["author_sex"]) else None
            item["author_sex"] = "男" if "manIcon" == item["author_sex"] else "女"
            item["author_img"] = "https:" + div.xpath("./div/a[1]/img/@src")[0] if len(div.xpath("./div/a[1]/img/@src")) else None
            item["content"] = div.xpath(".//div[@class='content']/span/text()")
            item["content_img"] = div.xpath(".//div[@class='thumb']/a/img/@src")[0] if len(div.xpath(".//div[@class='thumb']/a/img/@src")) else None

            # 添加到content列表中
            content_list.append(item)
        # 返回需要保存的数据
        return content_list

    # 保存数据
    def save_content(self,content_list,page_num):
        # 保存为json
        with open("./joke/qiubai第" + str(page_num) + "页.json",'w') as f:
            f.write(json.dumps(content_list,ensure_ascii=False,indent=2))

    # 实现主要逻辑
    def run(self):
        # 获取url
        url_list = self.get_url_list()
        for url in url_list:
            print(url)
            # 发送请求，获取响应
            html_str = self.get_result(url)
            # 提取数据
            content_list = self.get_content(html_str)
            # 保存数据
            self.save_content(content_list,(url_list.index(url)+1))

qiubai = QiubaiSpider()
qiubai.run()


