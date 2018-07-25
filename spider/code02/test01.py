import requests,re
import json
from tools.parseurl import parse_url
headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}


# 测试requests.utils.dict_from_cookiejar方法,响应中的cookie和字典相互转换
def test1():

    headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}

    response = requests.get("https://movie.douban.com/",headers=headers)

    cookies = response.cookies
    print(cookies)
    print(type(cookies))
    cookies = requests.utils.dict_from_cookiejar(cookies)
    print(cookies)
    print(type(cookies))
    cookies = requests.utils.cookiejar_from_dict(cookies)
    print(cookies)
    print(type(cookies))


# 测试requests.utils中unquote和quote方法，url的编解码功能
def test2():
    liyi = "%e6%9d%8e%e6%af%85"
    liyi = requests.utils.unquote(liyi)
    print(liyi)
    liyi = requests.utils.quote(liyi)
    print(liyi)


# 处理ssl证书问题
def test3():
    url = "http://www.12306.cn/mormhweb/"
    ret_str = requests.get(url,headers=headers,verify=False)
    print(ret_str.content.decode())


ret = re.sub(r"\xa0",",",'1.\xa0老婆做了一个特别特别特别特别特别的')
print(ret)







