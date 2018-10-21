import scrapy
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import data_washing
import re
from items import TutorialItem

option = webdriver.ChromeOptions()
# option.add_argument('headless')  # the next page click is invalid when headless is true by macos
driver = webdriver.Chrome(chrome_options=option)

class Myspider(scrapy.Spider):
    name = "tender"
    start_urls = [
        'http://zbcg.mas.gov.cn/maszbw/jygg/028001/028001003/028001003001/MoreInfo.aspx?CategoryNum=028001003001'
    ]


    def parse(self, response):
        if response.url == self.start_urls[0]:
            pro_type = 'tender'
            pro_address = 'city center'
        elif response.url == self.start_urls[1]:
            pro_type = 'tender'
            pro_address = 'hanshan'
        elif response.url == self.start_urls[2]:
            pro_type = 'tender'
            pro_address = 'hexian'
        elif response.url == self.start_urls[3]:
            pro_type = 'tender'
            pro_address = 'dangtu'


        url_list = [] #define detail url list
        proname_list = [] #define project name
        proreleasetime_list = []# define release time list

        driver.get(response.url)

        for i in range(2):
            '''
            get four items from project list
            pro_name/pro_number/pro_releasetime/pro_detailurl
            '''
            ## wait page load done!
            # wait = WebDriverWait(driver, 60)
            # wait.until(
            #     lambda driver: driver.find_element_by_xpath('//a'))

            #get project name
            sel_proname = driver.find_elements_by_xpath('//table[@id="MoreInfoList1_DataGrid1"]//tr//a')
            pron_list = [sel.get_attribute("textContent") for sel in sel_proname]
            proname_list += pron_list

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

            ##click “next page" button!
            try:
                # wait = WebDriverWait(driver,10)
                # wait.until(lambda driver:driver.find_element_by_xpath('//img[@src="/maszbw/images/page/nextn.gif"]/parent::a'))
                next_page = driver.find_element_by_xpath('//img[@src="/maszbw/images/page/nextn.gif"]/parent::a')
                next_page.click()
                time.sleep(2)
                i += 1
            except:
                print("####click error!####")
                break

        with open('url_list.txt',mode = 'w') as f:
            f.write(repr(url_list))#'repr()' return str to write txt
        for url in url_list:
            p = url_list.index(url)
            yield scrapy.Request(url=url,callback=self.parse_detail,meta={
            'pro_type': pro_type,
            'pro_address': pro_address,
            'pro_name':  proname_list[p],
            'pro_releasetime': proreleasetime_list[p],
            'pro_url': url})


    def parse_detail(self,response):
        item = TutorialItem()
        #define search keys
        sel_pronumber = ['项目编号']
        sel_section_number = ['标段编号']
        sel_firstwinning = ['第一中标候选人','中标候选人']
        sel_tenderprice = ['投标价(元)/费率（%）']



        is_table = response.xpath('//table[@id="tblInfo"]//table/tbody/tr').extract()
        if len(is_table) > 0:#is table data!!!
            data_type = 1    #define data type 1: table  2: not table
            #get tr generate a list
            tr_name_list = []
            for i in range(len(is_table)):
                i+=1
                table_tr = response.xpath(
                    '//table[@id="tblInfo"]//table/tbody/tr[%s]//td[1]//span/text()' % str(i)).extract()
                tr_name_list += [''.join(table_tr)]
            #get the value by select keys（exact search）
            def sel_listname(l):
                for sel in l:
                    try:
                        tr_name_list.index(sel)
                    except:
                        return_value = "has no this item"
                    else:
                        subscript_pro_area = tr_name_list.index(sel) + 1
                        if l == sel_firstwinning:
                            return_value = response.xpath(
                                'normalize-space(string(//table[@id="tblInfo"]//table/tbody/tr[%s]//td[3]))' % str(
                                    subscript_pro_area)).extract()
                        else:
                            return_value = response.xpath(
                                'normalize-space(string(//table[@id="tblInfo"]//table/tbody/tr[%s]//td[2]))' % str(
                                    subscript_pro_area)).extract()
                        break
                return return_value
            #combine the value to one value
            pro_pronumber_value = [''.join(sel_listname(sel_pronumber))]
            pro_section_value = [''.join(sel_listname(sel_section_number))]
            pro_firstwinning_value = [''.join(sel_listname(sel_firstwinning))]
            pro_tenderprice_value = [''.join(sel_listname(sel_tenderprice)[0])]


        else:
            data_type = 2
            pro_pronumber_value = 'waiting get......'
            pro_section_value = 'waiting get ......'
            pro_firstwinning_value = 'waiting get ......'
            pro_tenderprice_value = 'waiting get ......'




        yield {
            'pro_type': response.meta['pro_type'],
            'pro_address': response.meta['pro_address'],
            'data_type': data_type,
            'pro_name': response.meta['pro_name'],
            'pro_number': pro_pronumber_value,
            'pro_releasetime': response.meta['pro_releasetime'],
            'pro_url': response.meta['pro_url'],
            'pro_section': pro_section_value,
            'pro_firstwinning': pro_firstwinning_value,
            'pro_tenderprice': pro_tenderprice_value

        }
