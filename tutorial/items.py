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
    # Construction tender item setting
    pro_type = scrapy.Field()
    pro_address = scrapy.Field()
    data_type = scrapy.Field()
    pro_name = scrapy.Field()
    pro_number = scrapy.Field()
    pro_releasetime = scrapy.Field()
    pro_url = scrapy.Field()
    pro_section = scrapy.Field()
    pro_firstwinning = scrapy.Field()
    pro_tenderprice = scrapy.Field()
    # Construction entpq item setting
    ent_name = scrapy.Field()
    a_area = scrapy.Field()
    q_name = scrapy.Field()
    eq_url = scrapy.Field()
