import scrapy
from selenium import webdriver

option = webdriver.ChromeOptions()
option.add_argument('headless')  # the next page click is invalid when headless is true by macos
driver = webdriver.Chrome(chrome_options=option)


class Myspider(scrapy.Spider):
    name = "entpq"
    start_urls = [
        'http://app.ahgcjs.com.cn:3318/pub/query/comp/showCompInfo/130901181900705825'
    ]

    def parse(self, response):
        driver.get(response.url)

        # driver.switch_to.default_content()
        sell = driver.find_elements_by_xpath('//title')[0]
        text_2 = sell.get_attribute("textContent")
        driver.switch_to.frame("bodyFrame")  # insert iframe
        sel = driver.find_elements_by_xpath('//title')
        text_1 = sel[0].get_attribute("textContent")
        driver.switch_to.default_content()  # out iframe

        yield {
            'text_1': text_1,
            'text_2': text_2
        }




