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
        url_list = [] #define detail url list
        pronumber_list = [] #define pronumber list
        proreleasetime_list = []# define release time list

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
        '''
        判断是否是表格型数据
        '''
        is_table = response.xpath('//table[@id="tblInfo"]//table/tbody/tr').extract()
        if len(is_table) > 0:
            '''
            get tr generate a list
            '''
            tr_name_list = []
            for i in range(len(is_table)):
                i+=1
                table_tr = response.xpath(
                    '//table[@id="tblInfo"]//table/tbody/tr[%s]//td[1]//span/text()' % str(i)).extract()
                tr_name_list += [''.join(table_tr)]

            #get pro_area
            sel_area_keys = ['建设地点', '供货地点', '供货安装地点'] #define area search keys
            sel_period_keys = ['工期','检测服务期','设计服务期','计划工期','监理服务期'] #define period search keys

            def sel_listname(l):
                for sel in l:
                    try:
                        tr_name_list.index(sel)
                    except:
                        return_value = "has no this item"
                    else:
                        subscript_pro_area = tr_name_list.index(sel) + 1
                        return_value = response.xpath(
                            '//table[@id="tblInfo"]//table/tbody/tr[%s]//td[2]//span/text()' % str(
                                subscript_pro_area)).extract()
                        break
                return return_value

            pro_area_value = [''.join(sel_listname(sel_area_keys))]
            pro_period_value = [''.join(sel_listname(sel_period_keys))]

        else:
            pro_area_value = "this data is not table data!!"
            pro_period_value = "this data is not table data!!"




        yield {
            'pro_number': response.meta['pro_number'],
            'pro_releasetime': response.meta['pro_releasetime'],
            'pro_area': pro_area_value,
            'pro_period': pro_period_value

        }
