import requests,re
from lxml import etree


class TiebaSpider2:

    def __init__(self,tieba_name):
        # 初始url
        self.start_url = "http://tieba.baidu.com/mo/q----,sz@320_240-1-3---/m?kw=" + tieba_name + "&lp=5011&pn=0"
        self.headers = {"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"}
        # 需要拼接的url请求头
        self.url_head = "http://tieba.baidu.com/mo/q----,sz@320_240-1-3---"

    # 发送请求，获取响应
    def get_ret(self,url):
        response = requests.get(url,headers=self.headers)
        return response.content

    # 提取数据
    def get_content_list(self,html_str):
        # 获取etree对象
        html = etree.HTML(html_str)
        # 获取所有div下class包含"i”的节点
        div_list = html.xpath("//div[contains(@class,'i')]")
        # 需要返回的列表和下一页url地址
        content_list = []
        next_url = self.url_head + html.xpath("//a[text()='下一页']/@href")[0] if html.xpath("//a[text()='下一页']/@href") else None
        # 循环获取帖子的标题和url地址
        for div in div_list:
            item = {}
            item["title"] = div.xpath(".//a/text()")[0] if len(div.xpath(".//a/text()")) else None
            item["title"] = re.sub(r"[\.]?\xa0",",",item["title"])
            item["href"] = self.url_head + div.xpath(".//a/@href")[0] if len(div.xpath(".//a/@href")) else None
            # 调用函数获取每个帖子的图片地址
            item["image"] = self.get_image_list(item["href"])
            content_list.append(item)
        # 返回下一页url和需要保存的数据
        return next_url, content_list

    def get_image_list(self,url):
        detail_url = url
        img_list = []
        while detail_url is not None:
            # 发送请求，获取响应
            detail_html_str = self.get_ret(detail_url)
            # 转换为etree对象
            detail_html = etree.HTML(detail_html_str)
            # 获取所有图片对象
            detail_img_list = detail_html.xpath("//div[@class='i']/a[@href]")
            # 循环所有图片对象获取每个图片的url地址
            for img in detail_img_list:
                img = img.xpath("./@href")[0]
                img = re.sub(r"\?(.*)","",img)
                img_list.append(img)
            # 更改详情页的url地址，没有就结束循环
            detail_url = detail_html.xpath("//a[text()='下一页']/@href")[0] if len(detail_html.xpath("//a[text()='下一页']/@href")) else None
        return img_list

    # 保存数据
    def save_content_list(self,content_list):
        with open("./demo/tiebademo01.txt","a") as f:
            for content in content_list:
                f.write(str(content))
                f.write("\n")

    def run(self):
        next_url = self.start_url
        while next_url is not None:
            print(next_url)
            # 获取url
            # 发送请求，获取响应
            html_str = self.get_ret(next_url)
            # 提取数据
            next_url, content_list = self.get_content_list(html_str)
            # 保存数据
            self.save_content_list(content_list)

t1 = TiebaSpider2("做头发")
t1.run()


