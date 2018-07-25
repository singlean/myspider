import requests,re,json
from lxml import etree


class JDJotterSpider:
    """京东笔记本电脑信息爬虫"""

    def __init__(self,result):
        self.result = result
        self.url = "https://search.jd.com/Search?keyword=" + result + "&enc=utf-8&page={}"
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"}

    def get_url(self):
        return [self.url.format(i) for i in range(1,200) if i%2 == 1]

    def get_html_str(self,url):
        print(url)
        return requests.get(url,headers=self.headers).content

    def get_goods_url(self,url):
        html_str = self.get_html_str(url)
        html = etree.HTML(html_str)
        li_list = html.xpath("//ul[@class='gl-warp clearfix']/li")
        goods_url_list = []
        for i in li_list:
            item = {}
            item["goods_model"] = i.xpath(".//div[@class='p-name p-name-type-2']//em/text()")[0]
            goods_url = i.xpath(".//div[@class='p-name p-name-type-2']/a/@href")[0]
            ret = re.match(r"(^https:)", goods_url)
            if ret is None:
                goods_url = "https:" + goods_url
            item["goods_url"] = goods_url
            goods_url_list.append(item)

        return goods_url_list

    def get_goods_content_list(self,goods_url_dict):
        url = goods_url_dict["goods_url"]
        html_str = self.get_html_str(url)
        html = etree.HTML(html_str)
        li_list = html.xpath("//ul[@class='parameter2 p-parameter-list']/li")
        items = {}
        item = {}

        items["goods_sku_name"] = html.xpath("//div[@class='sku-name']/text()")[0]
        items["goods_sku_name"] = re.sub(r" |\n","",items["goods_sku_name"])
        items["goods_price"] = html.xpath("//div[@class='summary-price J-summary-price']//span[@class='p-price']//del/text()")[0] if len(html.xpath("//div[@class='summary-price J-summary-price']//span[@class='p-price']//del/text()")) else None
        items["goods_url"] = goods_url_dict["goods_url"]
        goods_img = []
        img_list = html.xpath("//div[@class='spec-items']//li/img/@src")
        for img in img_list:
            img = "https:" + img
            goods_img.append(img)

        items["goods_img"] = goods_img
        for li in li_list:
            li = li.xpath("./text()")[0]
            li = str(li).split("：")
            item[li[0]] = li[1]

        items["goods_detail"] = item

        return items

    def save_content(self,goods_content_list,page_num):
        with open("./demo/{}第{}页.json".format(self.result,page_num),"w") as f:
            f.write(json.dumps(goods_content_list,ensure_ascii=False,indent=2))

    def run(self):
        # url列表准备
        url_list = self.get_url()
        # 发送请求，获取响应
        for url in url_list:
            # 提取单个商品的url列表
            goods_content_list = []
            goods_url_list = self.get_goods_url(url)
            for goods_url_dict in goods_url_list:
                # 获取商品信息列表
                goods_content = self.get_goods_content_list(goods_url_dict)
                goods_content_list.append(goods_content)
                # 保存数据
            self.save_content(goods_content_list,(url_list.index(url)+1))


jd = JDJotterSpider("笔记本")
jd.run()













