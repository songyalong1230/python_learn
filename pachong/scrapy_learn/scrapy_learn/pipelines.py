# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScrapyLearnPipeline:
    fp = None
    #重写父类的一个方法，该方法只会在爬虫开始后被执行一次
    def open_spider(self, spider):
        self.fp = open('./duanzi_chijiuhua.csv', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        #将接收到的itme对象写入文件或者数据库
        title = item['title']
        content = item['content']
        self.fp.write(title + ':' + content+ '\n')
        return item

    #重写父类的一个方法，该方法只会在爬虫结束时被执行一次
    def close_spider(self, spider):
        self.fp.close()
