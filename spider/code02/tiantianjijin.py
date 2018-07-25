import requests
import json,re


class TTJiJinSpider:


    def __init__(self):
        self.url = "http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&sc=zzf&st=desc&sd=2017-06-24&ed=2018-06-24&qdii=&tabSubtype=,,,,,&pi=1&pn=3&dx=1"
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"}

    def get_url(self):
        return self.url

    def get_html_str(self,url):
        return requests.get(url,headers=self.headers).content.decode()

    def get_content(self,content):
        print(content)
        ret = re.findall(r"(\[.*\])",content)
        ret = json.loads(ret[0])
        for twig in ret:
            twig = ret.split(",")
            print(twig)
            print("*"*50)
        # with open("txt.json","w") as f:
        #     f.write(json.dumps(ret2,ensure_ascii=False,indent=2))


    def save_content(self,content):
        pass

    def run(self):
        # url准备
        url = self.get_url()
        # 发送请求，获取响应
        html_str = self.get_html_str(url)
        # 提取数据
        content = self.get_content(html_str)
        # 保存数据
        self.save_content(content)





# tt = TTJiJinSpider()
# tt.run()



