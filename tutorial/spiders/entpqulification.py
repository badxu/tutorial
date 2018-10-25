import scrapy
from selenium import webdriver
import re
import data_washing
import time
from scrapy_splash import SplashRequest
from items import TutorialItem

option = webdriver.ChromeOptions()
option.add_argument('headless')  # the next page click is invalid when headless is true by macos
driver = webdriver.Chrome(chrome_options=option)


class Myspider(scrapy.Spider):
    name = "entpq"
    start_urls = [
        'http://app.ahgcjs.com.cn:3318/pub/query/app/appPubList/1/1'
    ]
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url,self.parse,args={'wait':0.5})

    def parse(self, response):
        driver.get(response.url)
        dturl_list = []
        for i in range(2):
            sel_list = driver.find_elements_by_xpath('//form[@class="grid-form"]/table[3]//tr/td[2]//a')
            urlall_list = [sel.get_attribute("href") for sel in sel_list]
            url_filter = data_washing.entqlurl_filter(urlall_list)
            dturl_list += url_filter
            ##click “next page" button!
            try:
                next_page = driver.find_element_by_xpath('//a[@class="nxt"]')
                next_page.click()
                time.sleep(2)
                i += 1
            except:
                print("####the last page####")
                break

        for url in dturl_list:
            # yield SplashRequest(url,self.parse_detail,meta={'pro_url': url})
            yield scrapy.Request(url=url, callback=self.parse_detail, meta={'pro_url': url})

    def parse_detail(self, response):
        item = TutorialItem()
        driver.get(response.url)

        driver.switch_to.default_content()
        ent_name_raw = driver.find_elements_by_xpath('//div[@class="inquiry_listcont"]/table//tr[2]/td[2]')
        ent_name_list = [ele.get_attribute("textContent") for ele in ent_name_raw]
        ent_name = re.sub(r'\n?\t+\s+',"",ent_name_list[0])

        apply_area_raw = driver.find_elements_by_xpath('//div[@class="inquiry_listcont"]/table//tr/td[2]')
        apply_area_list = [ele.get_attribute("textContent") for ele in apply_area_raw]
        apply_area_list_wash = [re.sub(r'\r?\n?\t+\s+',"",ele) for ele in apply_area_list]
        apply_area = data_washing.applyarea_filter(apply_area_list_wash)
        if apply_area:
            apply_area_value = apply_area
        else:
            apply_area_value = 'error search!!'

        driver.switch_to.frame("bodyFrame")  # insert iframe

        row_count = len(driver.find_elements_by_xpath('//div[@class="inquiry_listcont"]/table[1]/tbody/tr'))
        if row_count:
            q_name = []
            for r in range(int(row_count/5)):
                raw_value = driver.find_element_by_xpath('//div[@class="inquiry_listcont"]/table[1]/tbody/tr[5+5*%d]/td[2]'%r).get_attribute("textContent")
                f_value = re.sub(r'\n?\t+\s+',"",raw_value)
                q_name += [f_value]
        else:
            q_name = "该企业无资质！"

        driver.switch_to.default_content()  # out iframe

        item['ent_name'] = ent_name
        item['a_area'] = apply_area_value
        item['q_name'] = ''.join(q_name)
        item['eq_url'] = response.meta['pro_url']
        yield item

        #
        # yield {
        #     'ent_name': ent_name,
        #     'a_area': apply_area_value,
        #     'q_name': q_name,
        #     'eq_url': response.meta['pro_url']
        # }
        #





