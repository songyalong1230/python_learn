'''
    - 12306登陆页面
        https://kyfw.12306.cn/otn/resources/login.html
    - 12306的验证码需要用到打码平台
        - 使用超级鹰打码平台进行验证
        - selenium动作链进行验证码的点击
            - 因为页面进去的时候验证码就刷新了，所以验证码不能再次发送了，再次请求验证码的话 验证码会变的
                所以得使用截屏，把截屏发给打码平台

'''

from selenium import webdriver
from PIL import Image
from lxml import etree
from selenium.webdriver import ActionChains
import time

bro = webdriver.Chrome(executable_path='./chromedriver') # 创建一个驱动
#获取到目标网站的对象
bro.get('https://kyfw.12306.cn/otn/resources/login.html')
#预留一秒钟让其页面进行加载数据、图片等
time.sleep(2)
#找到账号登陆的按钮元素，并对其进行点击操作
bro.find_element_by_xpath('/html/body/div[2]/div[2]/ul/li[2]/a').click()
# 找到账号输入框，对其进行输入账号
bro.find_element_by_xpath('//*[@id="J-userName"]').send_keys('851096287@qq.com')
# 找到密码输入框，对其进行输入密码
bro.find_element_by_xpath('//*[@id="J-password"]').send_keys('wy907141230syl')
# 验证码识别处理，验证码应该呗截屏截取下来，而不应该单独请求
# 截图需要使用第三方模块PIL，pip install Pillow，from PIL import Image
bro.save_screenshot('./imgs/login.png') # login.png表示的是登录页面的对应的截取图片
# 在login.png中将验证码的局部图片进行裁剪，验证码左下角跟右下角的坐标定位到，就可以截取
# 定位到验证码图片的标签位置
code_img_tag = bro.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[2]/div[3]/div/div[4]/img')
# 获取当前标签所在页面的左下角的坐标,loaction的坐标位置是{'x': 856, 'y': 282}
location = code_img_tag.location

# 获取当前标签在页面中的尺寸,size的大小为{'height': 188, 'width': 300}
size = code_img_tag.size
print(f'loaction的坐标位置是{location},size的大小为{size}')

# 计算出左下角与右上角的坐标,让坐标的xy加上对应的宽高
rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']), int(location['y'] + size['height']))
print(rangle)
#基于IMage类提供的工具进行裁剪
''' 如果进行裁剪验证码图片出现偏差的话，你可以调整电脑的缩放比例为100%'''
i = Image.open('./imgs/login.png')
frame = i.crop(rangle)
frame.save('./imgs/code.png')

#把截取的图片发给打码平台，打码平台返回对应的坐标位置
#获取返回的结果
result = [] #返回的是需要点击验证码子图上的坐标 x1,y1|x2,y2
# 需要将x1,y1|x2,y2 转换成[[x1,y1],[x2,y2]]
result = [[12,32],[43,32]]
#点击转换后的坐标
#使用selenium动作链  from selenium.webdriver import ActionChains
for pos in result:
    x = pos[0]
    y = pos[1]
    # x y 就是需要点击的一个点的坐标
    #实例化动作链对象,从code_img_tag这个坐标位置开始偏移
    ActionChains(bro).move_to_element_with_offset(code_img_tag, x, y).click().perform()
    #一秒点一次
    time.sleep(1)


# 找到登录按钮点击登录
bro.find_element_by_xpath('//*[@id="J-login"]').click()

time.sleep(3)
bro.quit()

