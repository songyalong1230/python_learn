import scrapy
'''
    这是自动生成的爬虫文件
'''

class Pachong01Spider(scrapy.Spider):
    # name 表示爬虫文件的名称， 表示的爬虫文件的唯一表示，不能重复
    name = 'pachong01'
    # 允许的域名，指的就是说用来做请求限定的，一旦该域名定义好之后，则start_urls只能发起该allowed_domains下的域名请求

    allowed_domains = ['www.baidu.com', 'http://www.sogou.com/']
    # 起始的url列表，可以将想要爬取的url存放在下面列表中，这个列表就可以帮我将每一个url进行get请求的发送
    start_urls = ['http://www.baidu.com/', 'http://www.sogou.com/']
    # parse 用作于数据解析的，parse的调用次数取决于start_urls里面的域名个数，返回几个response就调用几次parse函数
    def parse(self, response):
        print(response)
'''
    - 创建一个爬虫文件
                          文件名字    网址（随便写，文件里可以改）
        scrapy genspider pachong01 www.baidu.com
#命令行里执行 scrapy crawl pachong01 运行scrapy爬虫
# 执行完之后没有response返回，必须把robots协议给去掉
    - 不遵从robots协议
        - 在settings.py文件里修改ROBOTSTXT_OBEY = False  不遵从robots协议
    - 指定日志的等级
        - 在settings.py文件里添加 LOG_LEVEL = 'ERROR'，只会提示错误日志
    - UA伪装，在settings.py文件里修改USER_AGENT的值
        USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'


'''