import scrapy
from selenium import webdriver
import time
import data_washing


option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome(chrome_options=option)

class Myspider(scrapy.Spider):
    name = "biding"
    start_urls = [
        'http://zbcg.mas.gov.cn/maszbw/jygg/028001/028001001/028001001001/MoreInfo.aspx?CategoryNum=028001001001'
    ]


    def parse(self, response):
        url_list = [] #define detail url set(集合)
        pronumber_list = [] #define pronumber set
        proreleasetime_list = []# define release time set

        driver.get(response.url)

        for i in range(1):
            #get pro_number in biding list
            sel_pronum = driver.find_elements_by_xpath('//table[@id="MoreInfoList1_DataGrid1"]//tr//a')
            pronum_list = [sel.get_attribute("textContent") for sel in sel_pronum]
            filter_pronum = data_washing.pronumber_filter(pronum_list)
            pronumber_list += filter_pronum

            #get releasetime
            sel_proretime = driver.find_elements_by_xpath('//table[@id="MoreInfoList1_DataGrid1"]//tr/td[3]')
            proretime = [sel.get_attribute("textContent") for sel in sel_proretime]
            filter_proretime = data_washing.proretime_filter(proretime)
            proreleasetime_list += filter_proretime

            #get detail url
            sel_list = driver.find_elements_by_xpath('//a')
            urlall_list = [sel.get_attribute("href") for sel in sel_list]
            ####filter url
            url_filter = data_washing.prourl_filter(urlall_list)
            url_list += url_filter
            try:
                next_page = driver.find_element_by_xpath('//img[@src="/maszbw/images/page/nextn.gif"]/parent::a')
                next_page.click()
                time.sleep(2)
                i += 1
            except:
                print("####the last page####")
                break

        with open('url_list.txt',mode = 'w') as f:
            f.write(repr(url_list))#'repr()' return str to write txt
        for url in url_list:
            p = url_list.index(url)
            yield scrapy.Request(url=url,callback=self.parse_detail,meta={
            'pro_number': pronumber_list[p],
            'pro_releasetime': proreleasetime_list[p]})

    def parse_detail(self,response):
        yield {
            'pro_number': response.meta['pro_number'],
            'pro_releasetime': response.meta['pro_releasetime'],
            'pro_area': response.xpath('//table[@id="tblInfo"]//span[contains(text(),"建设地点")]/ancestor::tr[1]//span/text()').extract()[1:]
        }
