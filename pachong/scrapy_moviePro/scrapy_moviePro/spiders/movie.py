import scrapy
'''
    - 首先在setting.py文件里添加三个配置
        1、item配置
            ITEM_PIPELINES = {
               'scrapy_moviePro.pipelines.ScrapyMovieproPipeline': 300,
            }
        2、ua配置
            USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'
        3、日志级别配置
            LOG_LEVEL = 'ERROR'
'''
# 讲4567电影网站中的电影名称和电影简介进行爬取
# 深度爬取
from scrapy_moviePro.items import ScrapyMovieproItem

class MovieSpider(scrapy.Spider):
    name = 'movie'
    # allowed_domains = ['www.baidu.com']
    start_urls = ['https://www.4567kan.com/index.php/vod/show/class/%E5%8A%A8%E4%BD%9C/id/5.html']
    url = 'https://www.4567kan.com/index.php/vod/show/class/动作/id/5/page/%d.html'
    pageNum = 2
    def parse(self, response):
        # 解析电影对应的列表数据元素定位
        li_list = response.xpath('/html/body/div[1]/div/div/div/div[2]/ul/li')
        for li in li_list:
            name = li.xpath('./div/a/@title').extract_first()
            detail_url = 'https://www.4567kan.com' + li.xpath('./div/a/@href').extract_first()
            # 创建item对象
            item = ScrapyMovieproItem() # 不可以设定成全局的
            item['name'] = name
            # 把item对象传到回调函数里
            # 手动请求详情页，爬取详情页的数据，在详情页中解析出电影详情页的简介
            # 通过请求传参的机制，将item对象传到回调函数detail_parse里,加一个参数meta
            yield scrapy.Request(detail_url, callback=self.detail_parse, meta={'item': item})
            if self.pageNum <= 5:
                # 构建下一页的url，去请求解析
                new_url = self.url % self.pageNum
                self.pageNum += 1
                # 手动发送请求，并递归调用自身parse数据解析函数
                yield scrapy.Request(new_url, callback=self.parse)
    # 解析详情页的数据
    def detail_parse(self, response):
        #接受meta传参
        item = response.meta['item']
        desc = response.xpath('/html/body/div[1]/div/div/div/div[2]/p[5]/span[2]/text()').extract_first()
        item['desc'] = desc
        #向管道传递itme
        yield item