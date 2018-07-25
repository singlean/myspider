from lxml import etree
import requests
import json
from queue import Queue
import threading

class QiubaiSpider:

    def __init__(self):
        self.url = "https://www.qiushibaike.com/8hr/page/{}/"
        self.headers = {"user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
        self.url_queue = Queue()  # url 的queue池
        self.html_str_queue = Queue()  # html_str 的queue池
        self.json_str_queue = Queue()  # json_str 的queue池

    # 生产url列表
    def get_url_list(self):
        url_list = [self.url.format(i) for i in range(1,14)]
        for url in url_list:
            # 将url添加到url的queue池中
            self.url_queue.put(url)

    # 发送请求，获取响应
    def get_result(self):
        # 循环获取url发送请求并将结果添加到html_str的queue池中
        while True:
            url = self.url_queue.get()
            print(url)
            response = requests.get(url,headers=self.headers)
            self.html_str_queue.put(response.content)
            # 将queue池中的计数减一
            self.url_queue.task_done()

    # 获取需要保存的数据
    def get_content(self):
        # 循环获取响应的内容并将提取的数据添加到json_str的queue池中
        while True:
            html_str = self.html_str_queue.get()
            # 转换为etree对象
            html = etree.HTML(html_str)
            # 分组
            div_list = html.xpath("//div[@id='content-left']/div")
            content_list = []
            # 获取每一个段子分组中的数据
            for div in div_list:
                item = {}
                item["author_name"] = div.xpath("./div/a[2]/h2/text()")[0] if len(div.xpath("./div/a[2]/h2/text()")) else None
                item["author_sex"] = div.xpath(".//div[@class='author clearfix']/div/@class")
                item["author_sex"] = item["author_sex"][0].split(" ")[-1] if len(item["author_sex"]) else None
                item["author_sex"] = "男" if "manIcon" == item["author_sex"] else "女"
                item["author_img"] = "https:" + div.xpath("./div/a[1]/img/@src")[0] if len(div.xpath("./div/a[1]/img/@src")) else None
                item["content"] = div.xpath(".//div[@class='content']/span/text()")
                item["content_img"] = div.xpath(".//div[@class='thumb']/a/img/@src")[0] if len(div.xpath(".//div[@class='thumb']/a/img/@src")) else None

                content_list.append(item)
            self.json_str_queue.put(content_list)
            # 将queue池中的计数减一
            self.html_str_queue.task_done()
            # print("self.html_str_queue.empty()==" + str(self.html_str_queue.empty()))

    # 保存数据
    def save_content(self):
        # 循环获取需要保存的数据并写入文件
        while True:
            content_list = self.json_str_queue.get()
            with open("./joke/qiubai多线程.txt",'a') as f:
                for content in content_list:
                    f.write(str(content))
                    f.write("\n")
            # 将queue池中的计数减一
            self.json_str_queue.task_done()
            # print("self.json_str_queue.empty()==" + str(self.json_str_queue.empty()))

    def run(self):
        # 获取url
        self.get_url_list()
        thread_list = []

        # 发送请求，获取响应
        for i in range(3):
            t_get_ret = threading.Thread(target=self.get_result)
            thread_list.append(t_get_ret)

        # 提取数据
        for i in range(3):
            t_get_con = threading.Thread(target=self.get_content)
            thread_list.append(t_get_con)

        # 保存数据
        t_save_con = threading.Thread(target=self.save_content)
        thread_list.append(t_save_con)

        # 开启多线程
        for t in thread_list:
            # 设为守护线程,主线程结束就结束
            t.setDaemon(True)
            t.start()

        # 阻塞主线程，让主线程等待队列任务完成之后主线程再结束
        for q in [self.url_queue,self.html_str_queue,self.json_str_queue]:
            q.join()

        print("主线程结束")

qiubai = QiubaiSpider()
qiubai.run()


