# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # Construction biding item setting
    pro_type = scrapy.Field()#类型  招标/中标
    pro_address = scrapy.Field()#区域
    data_type = scrapy.Field()
    pro_name  = scrapy.Field()#项目名称
    pro_number = scrapy.Field()##项目编号
    pro_releasetime = scrapy.Field()#发布时间
    pro_area  = scrapy.Field()#建设地址
    pro_period = scrapy.Field()#建设周期
    pro_blockprice = scrapy.Field()#拦标价
    pro_blockprice_num = scrapy.Field()
    pro_section = scrapy.Field()  # 标段划分
    pro_range = scrapy.Field()  # 招标范围
    pro_qulifieldre = scrapy.Field()#资格要求
    pro_applytime = scrapy.Field()#报名时间
    pro_fileapplytime = scrapy.Field()#投标文件截止时间
    pro_url = scrapy.Field()

    pro_section_num = scrapy.Field() # 中标 标段编号
    pass
