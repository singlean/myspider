import os
import requests


class TBHtml():
    """获取贴吧分页数据"""

    # 初始化,准备必要的数据
    def __init__(self, tb_name):
        # 贴吧分页url的格式
        self.url = 'https://tieba.baidu.com/f?kw=' + tb_name + '&ie=utf-8&pn={}'
        self.ta_name = tb_name  # 设置爬去的贴吧名称，下面会用
        # 身份信息
        self.headers = {
            "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        # 保存的路径
        self.path = '/home/python/Desktop/pycharm/' + tb_name
        # 创建文件夹保存数据
        try:
            self.files = os.mkdir(self.path)
        except Exception as e:
            print(e)
            pass

    # 生成url列表
    def url_list(self):
        urls = [self.url.format(i * 50) for i in range(3)]
        return urls

    # 将数据保存到本地
    def save_html(self, str_html, page_num):
        # 拼接文件名打开文件并写入数据
        with open(self.path + "/" + self.ta_name + "-第{}页.html".format(page_num), "w") as f:
            f.write(str_html)

    def run(self):
        # url列表,heads(身份信息)
        urls = self.url_list()
        # 请求网页,获取响应
        for url in urls:
            # print(url)
            rsn_html = requests.get(url, headers=self.headers)
            # 保存html
            self.save_html(rsn_html.content.decode(), urls.index(url) + 1)


liyi = TBHtml("lol")
liyi.run()
