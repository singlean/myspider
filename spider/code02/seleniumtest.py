from selenium import webdriver
import time,re


# drive = webdriver.Chrome()
# drive.get("https://www.baidu.com")
# try:
#     drive.find_element_by_id("kw").send_keys("世界杯")
#     drive.find_element_by_id("su").click()
#
#     cookies = drive.get_cookies()
#     # print(cookies)
#     cookies = {i["name"]:i["value"] for i in cookies}
#     print(cookies)
#
#     # 服务器的响应信息，加载完js和css之后的页面
#     # print(drive.page_source)
#
#     time.sleep(1)
#     drive.save_screenshot("./baidu.png")
#
#     drive.quit()
# except Exception as e:
#     print(e)
#     drive.quit()


url = "https://music.163.com/discover/playlist/?cat=00%E5%90%8E"



