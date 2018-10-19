from .sql import Sql
from tutorial.tutorial.items import TutorialItem

class TutorialPipeline(object):
    def process_item(self,item,spider):
        if isinstance(item,TutorialItem):
            pro_number = item['pro_number']
            ret = Sql.select_pronumber(pro_number)
            if ret[0] == 1:
                print('have exist!!')
                pass
            else:
                # pro_type = item['pro_type']
                # pro_address = item['pro_address']
                # data_type = item['data_type']
                # pro_name = item['pro_name']
                pro_number = item['pro_number']
                # pro_releasetime = item['pro_releasetime']
                # pro_area = item['pro_area']
                # pro_period = item['pro_period']
                # pro_blockprice = item['pro_blockprice']
                # pro_blockprice_num = item['pro_blockprice_num']
                Sql.insert_bid_crawl(pro_number)