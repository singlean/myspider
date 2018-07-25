import requests

url = "https://www.baidu.com"
headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
proxies = {"http":"http://47.98.234.177:3128"}
# proxies = {"http":"http://163.177.151.23:80"}

rsn = requests.get(url,proxies=proxies,headers=headers)
print(rsn.url)
print(rsn.request.url)

# print(rsn.content.decode())

