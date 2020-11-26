import scrapy
from scrapy_learn.items import ScrapyLearnItem

class DuanziSpider(scrapy.Spider):
    name = 'duanzi'
    # allowed_domains = ['www.baidu.com']
    start_urls = ['https://ishuo.cn/xiaozhishi']

    # def parse(self, response):
    #     # 解析段子的内容
    #     # response.xpath跟tree.xpath不一样
    #     # 但使用基本一样，只是response.xpath返回的是一个selector的对象，
    #     all_data = [] #生成一个存放所有数据的列表
    #     li_list = response.xpath('//*[@id="list"]/ul/li')
    #     for li in li_list:
    #         #把返回的selector对象转换成字符串
    #         # content = li.xpath('./div[1]/text()')[0].extract()
    #         #跟上面的一样效果
    #         content = li.xpath('./div[1]/text()').extract_first()
    #         # 多个元素用extract
    #         title = li.xpath('./div[2]/a/text()').extract()[0]
    #         dict_data = {
    #             'content': content,
    #             'title': title
    #         }
    #         # 把获取到的每条数据追加到列表中
    #         all_data.append(dict_data)
    #         # print(content,'------', title)
    #     return all_data


    # ----------基于管道的持久化存储-------------
    def parse(self, response):
        # 解析段子的内容
        # response.xpath跟tree.xpath不一样
        # 但使用基本一样，只是response.xpath返回的是一个selector的对象，
        li_list = response.xpath('//*[@id="list"]/ul/li')
        for li in li_list:
            # 把返回的selector对象转换成字符串
            # content = li.xpath('./div[1]/text()')[0].extract()
            # 跟上面的一样效果
            content = li.xpath('./div[1]/text()').extract_first()
            # 多个元素用extract
            title = li.xpath('./div[2]/a/text()').extract()[0]
            # 在Item类中定义相关的属性，在上层目录中items.py文件中定义属性，解析的数据有几个字段就定义几个字段
                # title = scrapy.Field()
                # content = scrapy.Field()
            # 将解析到数据存储到Item对象中
            item = ScrapyLearnItem()
            # 给Item对象属性赋值
            item['title'] = title
            item['content'] = content
            # 将存储了解析数据的Item对象提交给管道,pipelines.py中定义好了管道类
            yield item
            # 进入pipelines.py中在管道文件中接受Item对象，且对其进行任意形式的持久化存储操作（一次只能接受一个item对象）


'''

    - 数据持久化存储
        - 基于终端执行命令的持久化存储
            scrapy crawl duanzi -o duanzi.csv
        - 基于管道：
            - 1、在爬虫文件中解析数据
            - 2、在Item类中定义相关的属性
            - 3、将在爬虫文件中解析的数据存储封装到Item对象中
            - 4、将存储了解析数据的Item对象提交给管道
            - 5、在管道文件中接受Item对象，且对其进行任意形式的持久化存储操作
            - 6、在配置文件中开启管道
                - 在settings.py文件里开启管道
                    -   ITEM_PIPELINES = {
                           'scrapy_learn.pipelines.ScrapyLearnPipeline': 300,
                        }
            终端执行scrapy crawl duanzi
'''

