import requests


def p_rsn():
    rsn = requests.get("http://docs.python-requests.org/en/latest/_static/requests-sidebar.png")
    print(rsn.content)
    with open("./res.png","wb") as f:
        f.write(rsn.content)


def xl_rsn():
    rsn = requests.get("http://www.sina.com.cn/")

    print(rsn.text)
    print("*"*50)
    print(rsn.content.decode())


def du_rsn():
    rsn = requests.get("https://tieba.baidu.com/")
    file = open("./tieba.html", "w")
    for cont in rsn.content.decode():
        file.write(cont)


file_1 = open("./tieba.html","r")
file_2 = open("./tieba_ce.txt","a")

a = file_1.readline()
for i in a:
    file_2.write(i)


file_2.close()
file_1.close()
