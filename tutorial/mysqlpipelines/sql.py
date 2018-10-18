import mysql.connector
from tutorial.tutorial import settings

MYSQL_HOSTS = settings.MYSQL_HOSTS
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DB = settings.MYSQL_DB

cnx = mysql.connector.connect(user=MYSQL_USER,password = MYSQL_PASSWORD,host=MYSQL_HOSTS,database = MYSQL_DB)
cur = cnx.cursor(buffered=True)

class Sql:
    @classmethod
    def inser_bid_crawl(cls,pro_type,pro_address,data_type,pro_name,pro_number,pro_releasetime,pro_area,pro_period,pro_blockprice,pro_blockprice_num):
        sql = 'INSERT INTO bid_crawl('pro_type','pro_address','data_type','pro_name','pro_number',\
                'pro_releasetime','pro_area','pro_period','pro_blockprice','pro_blockprice_num')\
                    VALUES (%(pro_type)s,%(pro_address)s,%(data_type)s,%(pro_name)s,%(pro_number)s \
                        ,%(pro_releasetime)s,%(pro_area)s,%(pro_period)s,%(pro_blockprice)s,%(pro_blockprice_num)s)'
        value = {
            'pro_type': pro_type,
            'pro_address':pro_address,
            'data_type': data_type,
            'pro_name': pro_name,
            'pro_number': pro_number,
            'pro_releasetime': pro_releasetime,
            'pro_area': pro_area,
            'pro_period': pro_period,
            'pro_blockprice': pro_blockprice,
            'pro_blockprice_num': pro_blockprice_num
        }
        cur.execute(sql,value)
        cnx.commit()

    @classmethod
    def select_pronumber(cls,pro_number):
        sql = "SELECT EXISTS(SELECT 1 FROM bid_crawl WHERE pro_number=%(pro_number)s)"
        value = {
            'pro_number': pro_number
        }
        cur.execute(sql,value)
        return cur.fetchall()[0]