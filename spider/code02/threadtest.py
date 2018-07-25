from selenium import webdriver
from queue import Queue
from threading import Thread
import time

url_queue = Queue()

url1 = "https://music.163.com/song?id=484614805"
url2 = "https://music.163.com/song?id=537407937"
url3 = "https://music.163.com/song?id=524191679"
url_queue.put(url1)
url_queue.put(url2)
url_queue.put(url3)


def test():
    dri = webdriver.Chrome()
    url = url_queue.get()
    dri.get(url)
    print(dri)
    # url_queue.task_done()

li_list = []
for i in range(3):
    t = Thread(target=test)
    li_list.append(t)

for t in li_list:
    t.start()

time.sleep(5)



