import requests
from retrying import retry

headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}


@retry(stop_max_attempt_number=3)
def _parse_url(url,method,headers,post_data={},proxies={}):

    if method == "GET":
        response = requests.get(url,headers=headers,proxies=proxies,timeout=3)
    else:
        response = requests.post(url,headers=headers,data=post_data,proxies=proxies,timeout=3)

    response = response.content.decode()
    return response


def parse_url(url,method,headers=headers,post_data={},proxies={}):
    try:
        ret_str = _parse_url(url,method,headers,post_data={},proxies={})
    except:
        ret_str = None

    return ret_str


