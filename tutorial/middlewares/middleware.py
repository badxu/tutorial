from selenium import webdriver
from scrapy.http import HtmlResponse
import time
from selenium.webdriver.chrome.options import Options

option = webdriver.ChromeOptions()
# option.add_argument('headless')

driver = webdriver.Chrome(chrome_options=option)

#chrome_options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'

class JavaScriptMiddleware(object):
    @classmethod
    def process_request(self, request, spider):
        if spider.name == "biding":
            print("ChromeHeadless is starting...")
            # driver = webdriver.PhantomJS() #指定使用的浏览器
            # driver = webdriver.Chrome()
            driver.get(request.url)
            time.sleep(1)
            # js = "var q=document.documentElement.scrollTop=10000"
            # driver.execute_script(js) #可执行js，模仿用户操作。此处为将页面拉至最底端。
            driver.find_element_by_xpath('//img[@src="/maszbw/images/page/nextn.gif"]/parent::a').click()
            time.sleep(2)
            body = driver.page_source
            print("访问" + request.url)
            return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)



        #
        # if 'Chrome' in request.meta:
        #     print ("ChromeHeadless is starting...")
        #     # driver = webdriver.PhantomJS() #指定使用的浏览器
        #     # driver = webdriver.Chrome()
        #     driver.get(request.url)
        #     time.sleep(1)
        #     #js = "var q=document.documentElement.scrollTop=10000"
        #     #driver.execute_script(js) #可执行js，模仿用户操作。此处为将页面拉至最底端。
        #     driver.find_element_by_xpath('//img[@src="/maszbw/images/page/nextn.gif"]/parent::a').click()
        #     time.sleep(2)
        #     body = driver.page_source
        #     print ("访问"+request.url)
        #     return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
        # else:
        #     # driver.get(request.url)
        #     # time.sleep(2)
        #     # body = driver.page_source
        #     # print("访问" + request.url)
        #     # return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
        #     return None
        #

