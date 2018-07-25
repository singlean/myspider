import requests
from selenium import webdriver
import json,re
from lxml import etree
from queue import Queue
from threading import Thread


class WangYiYunSpider:

    # 初始化
    def __init__(self):
        # 网易url
        self.url = "https://music.163.com/"
        # 实例化浏览器
        self.driver = webdriver.Chrome()
        self.lyrics = webdriver.Chrome()

    # 发送请求，获取html字符串
    def get_html(self):
        self.driver.get(self.url)

    def get_url_list(self):
        # 发送请求，获取html字符串
        self.get_html()
        # 切换到iframe下获取url列表信息
        self.driver.switch_to_frame("g_iframe")
        # 分组，获取url所在的节点
        a_list = self.driver.find_elements_by_xpath(".//div[@class='tit']")
        # 循环获取每个url信息
        url_list = []
        for a in a_list:
            item = {}
            # 标题和url
            item["title"] = a.find_element_by_xpath("./a").text
            item["url"] = a.find_element_by_xpath("./a").get_attribute("href")
            url_list.append(item)
        # 返回包含url信息的列表
        return url_list

    # 获取数据信息
    def get_content_list(self,url_dict):
        # 获取url，发送请求，获取响应内容
        url = url_dict["url"]
        self.driver.get(url)
        # 切换到需要获取信息的iframe中
        self.driver.switch_to_frame("g_iframe")
        #　分组，对每一组进行处理
        tr_list = self.driver.find_elements_by_xpath(".//table[@class='m-table m-table-rank']/tbody/tr")
        # 需要保存的信息列表
        content_list = []
        # 使用xpath循环获取信息
        for tr in tr_list:
            item = {}
            item["rank_num"] = tr.find_element_by_xpath(".//span[@class='num']").text
            item["title"] = tr.find_element_by_xpath(".//span[@class='txt']/a/b").get_attribute("title")
            item["time"] = tr.find_element_by_xpath(".//span[@class='u-dur ']").text
            item["author_name"] = tr.find_element_by_xpath("./td[4]/div[@class='text']").get_attribute("title")
            item["music"] = tr.find_element_by_xpath(".//span[@class='txt']/a").get_attribute("href")
            item["author_musics"] = tr.find_element_by_xpath("./td[4]/div[@class='text']//a").get_attribute("href")
            item["lyrics"] = self.get_lyrics(item["music"])
            content_list.append(item)
        #　返回数据内容
        return content_list

    # 获取歌词，未完成
    def get_lyrics(self,url):
        self.lyrics.get(url)
        self.lyrics.switch_to_frame("g_iframe")
        lyrics = self.lyrics.find_element_by_xpath(".//div[@id='lyric-content']").text
        # # self.lyrics.find_element_by_id("flag_ctrl").click()
        # lyrics1 = self.lyrics.find_element_by_xpath(".//div[@id='lyric-content']/div[@id='flag_more']").text

        return lyrics

    # 保存数据
    def save_content_list(self,content_list,url_dict):
        title = url_dict["title"]
        with open("./demo/{}.json".format(title),"w") as f:
            f.write(json.dumps(content_list,ensure_ascii=False,indent=2))

    def run(self):
        # 获取url列表
        url_list = self.get_url_list()
        #　循环获取数据
        for url_dict in url_list:
            # 将每个页面单独保存
            content_list = self.get_content_list(url_dict)
            self.save_content_list(content_list,url_dict)
        # 关闭浏览器
        self.driver.quit()
        self.lyrics.quit()


class WYYSpider:
    # TODO 未完成

    def __init__(self):
        self.url = "https://music.163.com/discover/playlist/"
        self.head_url = "https://music.163.com"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36"}
        self.type_url_queue = Queue()
        self.song_url_queue = Queue()
        self.content_list_queue = Queue()



    def get_html_str(self,url):
        return requests.get(url,headers=self.headers).content.decode()

    def get_type_url(self):
        html_str = self.get_html_str(self.url)

        html = etree.HTML(html_str)
        type_url_list = []
        dl_list = html.xpath("//dl[@class='f-cb']")
        for dl in dl_list:
            types = dl.xpath("./dt/text()")[0]
            a_list = dl.xpath(".//a")
            for a in a_list:
                item = {}
                item["music_type"] = a.xpath("text()")[0]
                item["type_url"] = self.head_url + a.xpath("@href")[0]
                item["types"] = types

                type_url_list.append(item)
        self.type_url_queue.put(type_url_list)
        # return type_url_list

    def get_song_list_url(self):
        while True:
            type_url_list = self.type_url_queue.get()
            for url_dict in type_url_list:
                url = url_dict["type_url"]
                html_str = self.get_html_str(url)
                html = etree.HTML(html_str)
                li_list = html.xpath("//ul[@id='m-pl-container']/li")
                song_list_list = []
                for li in  li_list:
                    item = {}
                    item["song_list_url"] = self.head_url + li.xpath(".//a[@class='msk']/@href")[0]
                    item["song_list_title"] = li.xpath(".//a[@class='msk']/@title")[0]
                    song_list_list.append(item)
                self.song_url_queue.put(song_list_list)
            self.type_url_queue.task_done()
                # return song_list_list

    def get_content(self):
        # 创建一个无界面谷歌浏览器
        opt = webdriver.ChromeOptions()
        opt.add_argument('--headless')
        opt.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=opt)
        while True:
            song_url_list = self.song_url_queue.get()
            for url_dict in song_url_list:
                url = url_dict["song_list_url"]
                # 获取url，发送请求，获取响应内容
                print(url)
                driver.get(url)
                # 切换到需要获取信息的iframe中
                driver.switch_to_frame("g_iframe")
                #　分组，对每一组进行处理
                tr_list = driver.find_elements_by_xpath(".//table[@class='m-table ']/tbody/tr")
                # 需要保存的信息
                content_list = []
                page_info = {}
                page_info["page_title"] = url_dict["song_list_title"]
                try:
                    page_info["introduce"] = driver.find_element_by_xpath(".//div[@class='cntc']/p[@class='intr f-brk']").text
                except:
                    page_info["introduce"] = None
                page_info["song_list_collect"] = driver.find_element_by_xpath(".//a[@class='u-btni u-btni-fav ']").get_attribute("data-count")
                i_list = driver.find_elements_by_xpath(".//div[@class='tags f-cb']/a[@class='u-tag']")
                desc = []
                for i in i_list:
                    i = i.find_element_by_xpath("./i").text
                    desc.append(i)
                page_info["song_list_label"] = desc
                page_info["play-count"] = driver.find_element_by_xpath(".//strong[@id='play-count']").text
                page_info["song_count"] = driver.find_element_by_xpath(".//span[@class='sub s-fc3']/span[@id='playlist-track-count']").text

                content_list.append(page_info)
                # 使用xpath循环获取信息
                for tr in tr_list:
                    item = {}
                    item["rank_num"] = tr.find_element_by_xpath(".//span[@class='num']").text
                    item["title"] = tr.find_element_by_xpath(".//span[@class='txt']/a/b").get_attribute("title")
                    item["time"] = tr.find_element_by_xpath(".//span[@class='u-dur ']").text
                    item["author_name"] = tr.find_element_by_xpath(".//div[@class='text']").get_attribute("title")
                    item["music"] = tr.find_element_by_xpath(".//span[@class='txt']/a").get_attribute("href")
                    item["author_musics"] = tr.find_element_by_xpath(".//a[@hidefocus='true']").get_attribute("href")
                    content_list.append(item)
                #　返回数据内容
                self.content_list_queue.put(content_list)
            self.song_url_queue.task_done()

    def save_content(self):
        while True:
            content_list = self.content_list_queue.get()
            title = content_list[0]["page_title"]
            title = re.sub(r"/", ":", title)
            with open("/home/python/Desktop/musicdata/" + title+".json","w")as f:
                f.write(json.dumps(content_list,ensure_ascii=False,indent=2))
            print("保存成功")
            self.content_list_queue.task_done()

    def run(self):
        # 获取所有分类的url地址
        self.get_type_url()
        # 获取所有歌单的url地址
        thread_list = []
        for i in range(3):
            t_song_url = Thread(target=self.get_song_list_url)
            thread_list.append(t_song_url)
        # 获取每个歌单的数据
        for i in range(5):
            t_content = Thread(target=self.get_content)
            thread_list.append(t_content)
        # 保存获取到底数据
        for i in range(3):
            t_save = Thread(target=self.save_content)
            thread_list.append(t_save)

        for t in thread_list:
            t.setDaemon(True)
            t.start()

        for q in [self.type_url_queue,self.song_url_queue,self.content_list_queue]:
            q.join()

        print("{}程序完成{}".format("*"*10,"*"*10))


wyy = WYYSpider()
wyy.run()











