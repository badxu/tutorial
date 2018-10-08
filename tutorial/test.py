


##Test chromedriver
#  from selenium import webdriver
# import time
# option = webdriver.ChromeOptions()
# option = webdriver.ChromeOptions()
# option.add_argument('headless')
# driver = webdriver.Chrome(chrome_options=option)
# # driver = webdriver.Chrome()
# # driver = webdriver.PhantomJS()
# driver.get('https://www.baidu.com/')
# print('打开浏览器')
# print(driver.title)
# driver.find_element_by_id('kw').send_keys('测试')
# print('关闭')
# driver.quit()
# print('测试完成')
#
# # def main():
# #     b = webdriver.Chrome()
# #     b.get('http://www.baidu.com')
# #     time.sleep(5)
# #     b.quit()
# # if __name__=='__main__':
# #     main()
# ##################################################
import re

url = re.compile(r'\/maszbw/infodetail/\?.*')

url_list = ['/maszbw/jygg/028001/028001001',
 '/maszbw/jygg/028001/028001002',
 '/maszbw/jygg/028001/028001003',
 '/maszbw/jygg/028001/028001004',
 '/maszbw/jygg/028001/028001005',
 '/maszbw/jygg/028002/028002001',
 '/maszbw/jygg/028002/028002002',
 '/maszbw/jygg/028002/028002003',
 '/maszbw/jygg/028002/028002004',
 '/maszbw/jygg/028002/028002005',
 '/maszbw/jygg/028003/028003001',
 '/maszbw/jygg/028003/028003002',
 '/maszbw/jygg/028004/028004001',
 '/maszbw/jygg/028004/028004002',
 '/maszbw/jygg/028005/028005001',
 '/maszbw/jygg/028005/028005002',
 '/maszbw/jygg/028007/028007001',
 '/maszbw/jygg/028007/028007002',
 '/maszbw/jygg/028007/028007003',
 '/maszbw/jygg/028007/028007004',
 '/maszbw/',
 '/maszbw/jygg',
 '/maszbw/jygg/028001',
 '/maszbw/jygg/028001/028001001',
 '/maszbw/jygg/028001/028001001/028001001001',
 '/maszbw/infodetail/?infoid=1b869da8-f129-43d3-8843-f8355404b211&categoryNum=028001001001',
 '/maszbw/infodetail/?infoid=a6c41f63-0847-4949-96d7-b6d8d76fc2e1&categoryNum=028001001001',
 '/maszbw/infodetail/?infoid=05d12c3e-f7c3-49cb-a15b-e2f12303ea05&categoryNum=028001001001',
 '/maszbw/infodetail/?infoid=d371a913-379b-4d60-a154-71387a4c980f&categoryNum=028001001001',
 '/maszbw/infodetail/?infoid=7750c8e2-0eeb-4df8-af86-a7967d72a48c&categoryNum=028001001001',
 '/maszbw/infodetail/?infoid=6cfb1ff8-73db-47e9-b72a-87639bb2c8eb&categoryNum=028001001001',
 '/maszbw/infodetail/?infoid=045e6230-f0c8-475e-9796-ba58691e2415&categoryNum=028001001001',
 '/maszbw/infodetail/?infoid=5d6a91ca-ab30-47b9-93d5-50303333e921&categoryNum=028001001001',
 '/maszbw/infodetail/?infoid=8bfac8a8-f606-43d1-b445-c0b138375d00&categoryNum=028001001001',
 '/maszbw/infodetail/?infoid=646d20c1-8a9f-43c5-998c-c9590f025f9d&categoryNum=028001001001',
 '/maszbw/infodetail/?infoid=bf900715-a737-44c7-8359-9c7a9c2a52d5&categoryNum=028001001001',
 '/maszbw/infodetail/?infoid=faad716b-baa7-41b2-9854-cbc517dc65d3&categoryNum=028001001001',
 '/maszbw/infodetail/?infoid=85dc2755-c9e8-436b-9341-07184308c51e&categoryNum=028001001001',
 '/maszbw/infodetail/?infoid=5ec522c1-46d3-4e4f-b955-083f937cea8a&categoryNum=028001001001',
 '/maszbw/infodetail/?infoid=5ec945f5-5bad-4ef5-90d1-a2becf122849&categoryNum=028001001001',
 '/maszbw/infodetail/?infoid=e6790b7d-7303-418d-8c3b-d489cd3b443d&categoryNum=028001001001',
 '/maszbw/infodetail/?infoid=df5808e8-0579-471d-85b4-b293a85f16d9&categoryNum=028001001001',
 '/maszbw/infodetail/?infoid=75e4bbae-2bbe-4116-81ab-361299f0dfd5&categoryNum=028001001001',
 '/maszbw/infodetail/?infoid=85a075c8-c7e5-4f7c-b325-54fe5d5638d4&categoryNum=028001001001',
 '/maszbw/infodetail/?infoid=048a3d92-ca0f-4e7c-bfcb-8c0b68da1321&categoryNum=028001001001',
 "javascript:__doPostBack('MoreInfoList1$Pager','2')",
 "javascript:__doPostBack('MoreInfoList1$Pager','3')",
 "javascript:__doPostBack('MoreInfoList1$Pager','4')",
 "javascript:__doPostBack('MoreInfoList1$Pager','5')",
 "javascript:__doPostBack('MoreInfoList1$Pager','6')",
 "javascript:__doPostBack('MoreInfoList1$Pager','7')",
 "javascript:__doPostBack('MoreInfoList1$Pager','8')",
 "javascript:__doPostBack('MoreInfoList1$Pager','9')",
 "javascript:__doPostBack('MoreInfoList1$Pager','10')",
 "javascript:__doPostBack('MoreInfoList1$Pager','11')",
 "javascript:__doPostBack('MoreInfoList1$Pager','2')",
 "javascript:__doPostBack('MoreInfoList1$Pager','208')"]
url_filter = [element for element in url_list if url.match(element)!= None]
for i in url_filter:
    print(i)