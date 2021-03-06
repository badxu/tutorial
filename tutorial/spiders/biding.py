import scrapy
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import data_washing
import re
from items import TutorialItem

option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome(chrome_options=option)

class Myspider(scrapy.Spider):
    name = "biding"
    start_urls = [
        'http://zbcg.mas.gov.cn/maszbw/jygg/028001/028001001/028001001001/MoreInfo.aspx?CategoryNum=028001001001',
        'http://zbcg.mas.gov.cn/maszbw/jygg/028001/028001001/028001001002/MoreInfo.aspx?CategoryNum=028001001002',
        'http://zbcg.mas.gov.cn/maszbw/jygg/028001/028001001/028001001003/MoreInfo.aspx?CategoryNum=028001001003',
        'http://zbcg.mas.gov.cn/maszbw/jygg/028001/028001001/028001001004/MoreInfo.aspx?CategoryNum=028001001004'
    ]


    def parse(self, response):
        if response.url == self.start_urls[0]:
            pro_type = 'bid'
            pro_address = 'city center'
        elif response.url == self.start_urls[1]:
            pro_type = 'bid'
            pro_address = 'hanshan'
        elif response.url == self.start_urls[2]:
            pro_type = 'bid'
            pro_address = 'hexian'
        elif response.url == self.start_urls[3]:
            pro_type = 'bid'
            pro_address = 'dangtu'


        url_list = [] #define detail url list
        proname_list = [] #define project name
        pronumber_list = [] #define pronumber list
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

        # with open('url_list.txt',mode = 'w') as f:
        #     f.write(repr(url_list))#'repr()' return str to write txt
        for url in url_list:
            p = url_list.index(url)
            yield scrapy.Request(url=url,callback=self.parse_detail,meta={
            'pro_type': pro_type,
            'pro_address': pro_address,
            'pro_name':  proname_list[p],
            'pro_number': pronumber_list[p],
            'pro_releasetime': proreleasetime_list[p],
            'pro_url': url})


    def parse_detail(self,response):
        item = TutorialItem()
        #define search keys
        sel_area_keys = ['建设地点', '供货地点', '供货安装地点'] #define area search keys
        sel_period_keys = ['工期','检测服务期','设计服务期','计划工期','监理服务期','勘察服务期','供货期'] #define period search keys
        sel_blockprice_keys = ['明标价','最高投标限价(人民币)','项目投资','最高投标限价（人民币）','招标控制价','固定报价（人民币）',
                               '招标预算价','最高投标限价','施工最高投标限价（人民币）','项目控制价','监理最高限价','监理最高限价/费率','工程施工监理投资估算价']

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
            data_type = 2
            ##Have a danger is tag u  to  express numric price!!!!
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


        def get_blockprice_num(l_bp):
            re_delblank = re.compile(r'\s+')
            re_getnum = re.compile(r'\d+\s?[.]?\d?\d?')
            re_getw = re.compile(r'万')
            re_gety = re.compile(r'亿')
            unit_w = re_getw.findall(l_bp[0])
            unit_y = re_gety.findall(l_bp[0])
            price = re_getnum.findall(l_bp[0])
            for i in range(len(price)):
                price_f = float(re.sub(re_delblank, '', price[i]))
                if unit_w:
                    res = price_f * 10000
                    price[i] = str(res)
                elif unit_y:
                    res = price_f * 100000000
                    price[i] = str(res)
                else:
                    res = price_f
            return price

        item['pro_type'] = response.meta['pro_type']
        item['pro_address'] = response.meta['pro_address']
        item['data_type'] = data_type
        item['pro_name'] = response.meta['pro_name']
        item['pro_number'] = response.meta['pro_number']
        item['pro_releasetime'] = response.meta['pro_releasetime']
        # item['pro_area'] = pro_area_value
        # item['pro_period'] = pro_period_value
        item['pro_blockprice'] = pro_blockprice_value
        item['pro_blockprice_num'] = '/'.join(get_blockprice_num(pro_blockprice_value))
        item['pro_url'] = response.meta['pro_url']
        yield item
        # yield {
        #     'pro_type': response.meta['pro_type'],
        #     'pro_address': response.meta['pro_address'],
        #     'data_type': data_type,
        #     'pro_name': response.meta['pro_name'],
        #     'pro_number': response.meta['pro_number'],
        #     'pro_releasetime': response.meta['pro_releasetime'],
        #     'pro_area': pro_area_value,
        #     'pro_period': pro_period_value,
        #     'pro_blockprice': pro_blockprice_value,
        #     'pro_blockprice_num': get_blockprice_num(pro_blockprice_value)
        #
        # }
