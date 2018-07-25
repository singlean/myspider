import requests

# 将cookie放入headers中
# headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
#            "Cookie":"anonymid=jiek2obg-j9ds2m; ick=5287e1e1-a98c-404c-8754-58c970ee70ef; __utma=151146938.660906960.1528981481.1528981481.1528981481.1; __utmc=151146938; __utmz=151146938.1528981481.1.1.utmcsr=renren.com|utmccn=(referral)|utmcmd=referral|utmcct=/; JSESSIONID=abcxk6OtXUT8v-Eq5z_pw; jebe_key=eab48339-c666-4df1-b9d0-75a0d83c2dad%7C7aa80c80f70ce0a3bcfd81b17aa9bf53%7C1528981599473%7C1%7C1528981602383; XNESSESSIONID=d7de89f50506; depovince=HUB; jebecookies=746e0678-e332-486d-b62b-0f2ab5de0b96|||||; _r01_=1; ick_login=0f0fe84c-7466-4b9b-b8bf-0942aad7a504; _de=154198F99314A01332B6AB0A4B67A9B4; p=fe25ee677fd4dc4041669b5336dca9da5; first_login_flag=1; ln_uact=13972749880; ln_hurl=http://head.xiaonei.com/photos/0/0/women_main.gif; t=47a9edb1f9830c05932928e6f62abcac5; societyguester=47a9edb1f9830c05932928e6f62abcac5; id=831149315; xnsid=1700322; loginfrom=syshome; wp_fold=0; BAIDU_SSP_lcr=https://www.baidu.com/link?url=y2-4ozylK36m_LKx890MaeI7vuE43krJ6zXAbAh78ZG&wd=&eqid=a23cfada0003eb82000000025b2267bb; ch_id=10050"}

url = "http://www.renren.com/PLogin.do"
headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
pase_data = {"email":13972749880,"password":"qiqing1105"}
cookies = "anonymid=jiek2obg-j9ds2m; ick=5287e1e1-a98c-404c-8754-58c970ee70ef; __utma=151146938.660906960.1528981481.1528981481.1528981481.1; __utmc=151146938; __utmz=151146938.1528981481.1.1.utmcsr=renren.com|utmccn=(referral)|utmcmd=referral|utmcct=/; JSESSIONID=abcxk6OtXUT8v-Eq5z_pw; jebe_key=eab48339-c666-4df1-b9d0-75a0d83c2dad%7C7aa80c80f70ce0a3bcfd81b17aa9bf53%7C1528981599473%7C1%7C1528981602383; XNESSESSIONID=d7de89f50506; depovince=HUB; jebecookies=746e0678-e332-486d-b62b-0f2ab5de0b96|||||; _r01_=1; ick_login=0f0fe84c-7466-4b9b-b8bf-0942aad7a504; _de=154198F99314A01332B6AB0A4B67A9B4; p=fe25ee677fd4dc4041669b5336dca9da5; first_login_flag=1; ln_uact=13972749880; ln_hurl=http://head.xiaonei.com/photos/0/0/women_main.gif; t=47a9edb1f9830c05932928e6f62abcac5; societyguester=47a9edb1f9830c05932928e6f62abcac5; id=831149315; xnsid=1700322; loginfrom=syshome; wp_fold=0; BAIDU_SSP_lcr=https://www.baidu.com/link?url=y2-4ozylK36m_LKx890MaeI7vuE43krJ6zXAbAh78ZG&wd=&eqid=a23cfada0003eb82000000025b2267bb; ch_id=10050"
# 切片并使用字典生成式
cookies = {i.split("=")[0]: i.split("=")[1] for i in cookies.split("; ")}

# 使用requests中的session函数完成cookie的保存
# session = requests.session()
# session.post(url,headers=headers,data=pase_data)
# rsn = session.get(url,headers=headers)

# 将cookie放入headers中直接发送get请求
# rsn = requests.get(url,headers=headers,data=pase_data)


rsn = requests.get(url,headers=headers,data=pase_data,cookies=cookies)

with open("./renren3.html",'w') as f:
    f.write(rsn.content.decode())









