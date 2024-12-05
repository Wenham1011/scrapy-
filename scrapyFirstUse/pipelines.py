# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

# 存储到本地txt文件夹的管道类
class ScrapyfirstusePipeline:
    # 重写父类方法：只会在爬虫开始时被执行一次
    def open_spider(self,spider):
        self.fp = open('古诗文网.txt','w',encoding='utf-8')

    # 这个方法用来接收爬虫文件提交过来的item对象（一次只能接收一个）
    # item: 即接收的item对象
    # spider:
    def process_item(self, item, spider):
        title = item['title']
        author = item['author']
        content = item['content']
        self.fp.write(title+author+content+'\n')
        return item

    # 重写重写父类方法：只会在爬虫结束时被执行一次
    def close_spider(self,spider):
        self.fp.close()

# 存储到mysql的管道类
class MysqlPipeline(object):
    conn = None
    cursor = None
    def open_spider(self,spider):
        self.conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='2285',db='gushiwen',charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        title = item['title']
        author = item['author']
        content = item['content']
        try:
            sql = 'insert into gushiwen(title,author,content) values("%s","%s","%s")'%(title,author,content)
            self.cursor.execute(sql)
            self.conn.commit()
            print("insert successful")
        except Exception as e:
            print(e)
            self.conn.rollback()
        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()
