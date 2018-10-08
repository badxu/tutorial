import scrapy
from selenium import webdriver
import time
import re

option = webdriver.ChromeOptions()
driver = webdriver.Chrome(chrome_options=option)

re_url = re.compile('.*\/maszbw/infodetail/\?.*')

class Myspider(scrapy.Spider):
    name = "biding"
    start_urls = [
        'http://zbcg.mas.gov.cn/maszbw/jygg/028001/028001001/028001001001/MoreInfo.aspx?CategoryNum=028001001001'
    ]


    def parse(self, response):
        url_set = set()
        driver.get(response.url)
        for i in range(1):
            sel_list = driver.find_elements_by_xpath('//a')
            url_list = [sel.get_attribute("href") for sel in sel_list]
            #filter url
            url_filter = [element for element in url_list if re_url.match(element)!= None]
            url_set |= set(url_filter)
            try:
                next_page = driver.find_element_by_xpath('//img[@src="/maszbw/images/page/nextn.gif"]/parent::a')
                next_page.click()
                time.sleep(2)
            except:
                print("####the last page####")
                break

        with open('url_list.txt',mode = 'w') as f:
            f.write(repr(url_set))#'repr()' return str to write txt
        for url in url_set:
            yield scrapy.Request(response.urljoin(url),callback=self.parse_detail)

    def parse_detail(self,response):
        yield {
            'id': response.css('span::text').re(r'\w{3}\-\d{2}\-\d{4}\-\d{4}')
        }
