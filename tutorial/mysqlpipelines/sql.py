import mysql.connector
from scrapy.conf import settings

host = settings['MYSQL_HOSTS']
user = settings['MYSQL_USER']
psd = settings['MYSQL_PASSWORD']
db = settings['MYSQL_DB']
c = settings['CHARSET']
port = settings['MYSQL_PORT']

cnx = mysql.connector.connect(user=user,password = psd,host=host,database = db,port=port,charset=c)
cur = cnx.cursor(buffered=True)

class Sql:
    @classmethod
    def insert_bid_crawl(cls,pro_number):
        sql = 'INSERT INTO bid_info(`pro_number`)\
                    VALUES (%(pro_number)s)'
        value = {

            'pro_number': pro_number,

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