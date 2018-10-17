import scrapy
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import data_washing
import re


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
        proname_list = [] #define project name
        pronumber_list = [] #define pronumber list
        proreleasetime_list = []# define release time list

        driver.get(response.url)

        for i in range(1):
            '''
            get four items from project list
            pro_name/pro_number/pro_releasetime/pro_detailurl
            '''
            ## wait page load done!
            # wait = WebDriverWait(driver, 60)
            # wait.until(
            #     lambda driver: driver.find_element_by_xpath('//a'))

            #get pro_number in biding list
            sel_pronum = driver.find_elements_by_xpath('//table[@id="MoreInfoList1_DataGrid1"]//tr//a')
            pronum_list = [sel.get_attribute("textContent") for sel in sel_pronum]
            filter_pronum = data_washing.pronumber_filter(pronum_list)
            pronumber_list += filter_pronum

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
                print("####the last page####")
                break

        with open('url_list.txt',mode = 'w') as f:
            f.write(repr(url_list))#'repr()' return str to write txt
        for url in url_list:
            p = url_list.index(url)
            yield scrapy.Request(url=url,callback=self.parse_detail,meta={
            'pro_name':  proname_list[p],
            'pro_number': pronumber_list[p],
            'pro_releasetime': proreleasetime_list[p]})

    def parse_detail(self,response):
        #define search keys
        sel_area_keys = ['建设地点', '供货地点', '供货安装地点'] #define area search keys
        sel_period_keys = ['工期','检测服务期','设计服务期','计划工期','监理服务期','勘察服务期','供货期'] #define period search keys
        sel_blockprice_keys = ['最高投标限价（人民币）','招标控制价','最高投标限价','施工最高投标限价（人民币）']


        is_table = response.xpath('//table[@id="tblInfo"]//table/tbody/tr').extract()
        if len(is_table) > 0:#is table data!!!
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
                        #optimize select  add normalize-space  and  string(.)
                        return_value = response.xpath(
                            'normalize-space(string(//table[@id="tblInfo"]//table/tbody/tr[%s]//td[2]))' % str(
                                subscript_pro_area)).extract()
                        break
                return return_value
            #combine the value to one value
            pro_area_value = [''.join(sel_listname(sel_area_keys))]
            pro_period_value = [''.join(sel_listname(sel_period_keys))]
            pro_blockprice_value = [''.join(sel_listname(sel_blockprice_keys))]

        else:
            nottable_data = response.xpath('//table[@id="tblInfo"]//tr[3]//span/text()').extract() #not table all data
            #get list subscript with keys（fuzzy search use re）
            def sel_subsptBykey(l1):
                for ele in l1:
                    re_keys = re.compile(r'.*%s.*'%str(ele))
                    match_list = [element for element in nottable_data if re_keys.match(element) != None]
                    if match_list:
                        sel_index = [i for i, x in enumerate(nottable_data) if x == str(match_list[0])]
                        index_value = int(str(sel_index[0]))
                        return_value = nottable_data[index_value: index_value + 3]  # get the sel location follow 5 values
                        break
                    else:
                        return_value = "has no this item!"
                return return_value
            pro_area_value = [''.join(sel_subsptBykey(sel_area_keys))]
            pro_period_value = [''.join(sel_subsptBykey(sel_period_keys))]
            pro_blockprice_value = [''.join(sel_subsptBykey(sel_blockprice_keys))]



        yield {
            'pro_name': response.meta['pro_name'],
            'pro_number': response.meta['pro_number'],
            'pro_releasetime': response.meta['pro_releasetime'],
            'pro_area': pro_area_value,
            'pro_period': pro_period_value,
            'pro_blockprice': pro_blockprice_value

        }
