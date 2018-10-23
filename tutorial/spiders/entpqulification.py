import scrapy
from selenium import webdriver
import re
import data_washing
import time

option = webdriver.ChromeOptions()
option.add_argument('headless')  # the next page click is invalid when headless is true by macos
driver = webdriver.Chrome(chrome_options=option)


class Myspider(scrapy.Spider):
    name = "entpq"
    start_urls = [
        'http://app.ahgcjs.com.cn:3318/pub/query/app/appPubList/1/1'
    ]

    def parse(self, response):
        driver.get(response.url)
        dturl_list = []
        for i in range(2):
            sel_list = driver.find_elements_by_xpath('//form[@class="grid-form"]/table[3]//tr//a')
            urlall_list = [sel.get_attribute("href") for sel in sel_list]
            url_filter = data_washing.entqlurl_filter(urlall_list)
            dturl_list += url_filter
            ##click “next page" button!
            try:
                next_page = driver.find_element_by_xpath('//a[@class="nxt"')
                next_page.click()
                time.sleep(2)
                i += 1
            except:
                print("####the last page####")
                break

    def parse_detail(self, response):
        driver.get(response.url)

        driver.switch_to.default_content()
        driver.switch_to.frame("bodyFrame")  # insert iframe
        row_count = len(driver.find_elements_by_xpath('//div[@class="inquiry_listcont"]/table[1]/tbody/tr'))
        q_number = []
        for r in range(int(row_count/5)):
            raw_value = driver.find_element_by_xpath('//div[@class="inquiry_listcont"]/table[1]/tbody/tr[2+5*%d]/td[2]'%r).get_attribute("textContent")
            f_value = re.sub(r'\n?\t+\s+',"",raw_value)
            q_number += [f_value]

        driver.switch_to.default_content()  # out iframe

        yield {
            'q_number': q_number
        }




