# -*- coding: utf-8 -*-
import scrapy,re


class RenrenSpider(scrapy.Spider):
    name = 'renren'
    allowed_domains = ['renren.com']
    start_urls = ['http://www.renren.com/']

    # 重写start_requests方法，自定义初始网址的请求过程
    # def start_requests(self):
    #     cookies = "ick_login=49a16c9b-7ccf-48fc-9f73-4a82667dc19b; anonymid=jiye4t4tmbhrvp; _de=154198F99314A01332B6AB0A4B67A9B4; ick=c6f4449c-5d2c-4670-83bc-4b0299b6b7b8; __utma=151146938.285495103.1530180943.1530180943.1530180943.1; __utmc=151146938; __utmz=151146938.1530180943.1.1.utmcsr=renren.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt=1; __utmb=151146938.4.10.1530180943; p=cdac66e64b60146c0187c803af0ff9df5; first_login_flag=1; ln_uact=13972749880; ln_hurl=http://head.xiaonei.com/photos/0/0/women_main.gif; t=1b2790711d836fc2c5b96ac5dffb43dd5; societyguester=1b2790711d836fc2c5b96ac5dffb43dd5; id=831149315; xnsid=ba1a157c; loginfrom=syshome; JSESSIONID=abcDhaFWNZxUG776E5frw; jebe_key=6d2a477f-5537-47fb-ac45-b8b311da3a46%7C7aa80c80f70ce0a3bcfd81b17aa9bf53%7C1530181058081%7C1%7C1530181063523; wp_fold=0; XNESSESSIONID=dffe5fc62e1a"
    #     cookies = {i.split("=")[0]:i.split("=")[1] for i in cookies.split(";")}
          # 请求的登陆后的界面，cookies接受一个cookie字典
    #     yield scrapy.Request(
    #         self.start_urls[0],
    #         callback = self.parse,
    #         cookies = cookies
    #         )

    def parse(self, response):
        # print(re.findall("祁晴",response.body.decode()))

        # 将需要携带的数据组成一个字典
        post_data = dict(
            email="13972749880",
            password="qq110625"
        )
        # 发送post请求,formdata接受一个字典
        yield scrapy.FormRequest(
            "http://www.renren.com/PLogin.do",
            callback = self.parse_login,
            formdata=post_data
        )

    def parse_login(self,response):
        print(re.findall("祁晴",response.body.decode()))





























