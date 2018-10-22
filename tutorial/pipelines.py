# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.conf import settings

class TutorialPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'biding':
            host = settings['MYSQL_HOSTS']
            user = settings['MYSQL_USER']
            psd = settings['MYSQL_PASSWORD']
            db = settings['MYSQL_DB']
            c = settings['CHARSET']
            port = settings['MYSQL_PORT']
            con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c,port=port)
            cue = con.cursor()
            print('mysql connect success!')

            try:
                cue.execute("insert into bid_info (pro_type,pro_address,data_type,pro_name,pro_number,pro_releasetime,pro_blockprice,pro_blockprice_num,pro_url) "
                            "values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            [ item['pro_type'],item['pro_address'],item['data_type'],item['pro_name'],item['pro_number'],item['pro_releasetime'],item['pro_blockprice'],item['pro_blockprice_num'],item['pro_url']])
                print("insert success")
            except Exception as e:
                print('Insert error:',e)
                con.rollback()
            else:
                con.commit()
            con.close()
        else:
            pass

        return item

