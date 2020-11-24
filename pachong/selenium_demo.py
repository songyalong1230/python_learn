'''
    Selenium 是什么？
        - 说白了就是一个模拟真实浏览器的一个东西
        - 一句话，自动化测试工具。它支持各种浏览器，包括 Chrome，Safari，Firefox 等主流界面式浏览器，
        - 如果你在这些浏览器里面安装一个 Selenium 的插件，那么便可以方便地实现 Web 界面的测试
    -下载安装selenium
        pip install selenium
    - 下载浏览器驱动
        把驱动放在一个文件目录，或者放在系统环境变量里也行，
        或者随便找个地方放，然后通过创建驱动的时候，手工指定驱动文件的路径

        下载selenium的谷歌浏览器的驱动
            https://sites.google.com/a/chromium.org/chromedriver/downloads
        - 下面是各个浏览器的驱动
            Chrome:	https://sites.google.com/a/chromium.org/chromedriver/downloads
            Edge:	https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
            Firefox:	https://github.com/mozilla/geckodriver/releases
            Safari:	https://webkit.org/blog/6900/webdriver-support-in-safari-10/
    - selenium和爬虫之间的关联
        - 非常便捷的捕获到任意形式动态加载出来的数据
            - 可见既可得
            - 但是爬取数据的效率低
        - 可以模拟登陆
            - 通常有些大型网站的反爬机制比较高，但可以使用selenium进行模拟登陆
'''

# 运行的文件命名一定不要为selenium，因为执行文件的时候导致Python会先导入这个文件selenium，然后再导入标准库里面的selenium.py
from selenium import webdriver
from lxml import etree
import time

# 动态加载数据的爬取
bro = webdriver.Chrome(executable_path='./chromedriver') # 创建一个驱动
bro.get('http://scxk.nmpa.gov.cn:81/xk/')
# 等待两秒钟后再获取页面被加载出来的页面源码
time.sleep(2)

# 获取所有页面的源码
page_text = bro.page_source
#把获取到的页面源码加载到HTMl对象里
tree = etree.HTML(page_text)
#使用xpath 获取数据
# print(tree.xpath('//*[@id="3001"]/div/h3/a'))
resu_list = tree.xpath('//*[@id="gzlist"]/li')
for i in resu_list:
    name = i.xpath('./dl/@title')[0]
    print(name)
#关闭浏览器
bro.quit()