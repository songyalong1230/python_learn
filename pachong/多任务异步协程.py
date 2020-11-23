'''
    - 多任务异步协程【asyncio】
        - 环境安装
            - pip install asyncio
        - 特殊函数
            - 如果一个函数的定义被asyncio关键字修饰，则该函数就变成了一个特殊的函数
            - 该函数调用后函数内部的实现语句不会被  立即 执行
            - 返回结果是一个协程对象
        - 协程
            - 协程本质意义上就是一个对象，该对象是特殊函数调用后返回的协程对象
            - 协程对象  == 特殊的函数
        - 任务对象
            - 就是一个高级的协程对象
            - 任务对象  ==  协程对象  == 特殊的函数
            - 任务对象也表示一组特定的操作
        - 事件循环EventLoop
            - 对象
            - 如何创建事件循环对象
                loop = asyncio.get_event_loop()
            - 作用
                - 是用来装载任务对象的，也可以装载协程对象
                    - 可以将事件循环当做是一个容器，容器中存放的是一个或多个任务对象
                    - 如果事件循环存放了多个任务对象且事件循环启动后，则事件循环对象就可以
                        异步的将每一个任务对象对应的指定操作进行执行
        - 如何将任务对象存储且启动事件循环对象
            loop.run_until_complete(task)
        - 问题
            - 事件循环执行后如何拿到返回值，
                - 基于任务对象的回调函数
                - 如何给任务对象绑定回调函数
                    task.add_done_callback(parse)
            -
        - 如何注册将多个任务对象注册到事件循环中？
            loop.run_until_complete(asyncio.wait(task_list))
            - wait()方法的作用
                - 表示挂起的意思，就是cpu不停的切换执行每一个任务，遇到阻塞的话执行下个任务
        - 如何解决让程序异步执行【重要】
            - 在特殊函数内部的实现语句中，不可以出现不支持异步的模块代码，否则会中断整个异步效果；
            - 支持异步网络请求的模块【aiohttp】
            - aiohttp的编码使用：
                - 编写一个大致架构
                        with aiohttp.ClientSession() as sess: #实例化一个请求对象叫sess
                            # sess.get()和sess.post()的用法跟原生的基本一样，只是参数proxy跟原生的requests模块的不一样
                            # proxy= "http://ip:port"
                            with sess.get(url=url) as respones: # 调用get发请求，然后返回一个相应对象
                                page_text = respones.text()  # 获取页面数据
                                # text()返回字符串的响应数据
                                # read()返回bytes类型的数据
                                return page_text
                - 在上面大致架构中补充细节，
                    1、在每一个with语句前面加一个 async关键字
                    2、在每一个阻塞操作前加上一个await 关键字，每一个请求前面加；
                        加await的意思是因为当在事件循环列表里对任务进行执行的时候，当任务1执行到阻塞的时候，会跳到任务2那边执行非阻塞操作，
                        如果不加 await的话，那么当任务1执行到阻塞操作的时候，那么cpu会跳过任务1的阻塞操作，直接执行任务1的下一步操作，不会去执行任务2，
                            只有任务1全部都执行完之后才会去执行任务2
                    - 完整代码：
                            async with aiohttp.ClientSession() as sess: #实例化一个请求对象叫sess
                                # sess.get()和sess.post()的用法跟原生的基本一样，只是参数proxy跟原生的requests模块的不一样
                                # proxy= "http://ip:port"
                                async with await sess.get(url=url) as respones: # 调用get发请求，然后返回一个相应对象
                                    page_text = await respones.text()  # 获取页面数据
                                    # text()返回字符串的响应数据
                                    # read()返回bytes类型的数据
                                    return page_text

'''

import asyncio
import time

# 原来特殊的函数
# async def func(arg):
#     print(f'线程{arg}开始')

#     time.sleep(2) #time.sleep(2)模拟requests.get()请求
#
#     return len(arg)
import aiohttp
url = 'http://www.baidu.com'

async def func(arg):
    print(f'线程{arg}开始')
    # 使用aiohttp进行异步请求
    url = 'http://www.baidu.com'
    async with aiohttp.ClientSession() as sess: #实例化一个请求对象叫sess
        # sess.get()和sess.post()的用法跟原生的基本一样，只是参数proxy跟原生的requests模块的不一样
        # proxy= "http://ip:port"
        async with await sess.get(url=url) as respones: # 调用get发请求，然后返回一个相应对象
            page_text = await respones.text()  # 获取页面数据
            # text()返回字符串的响应数据
            # read()返回bytes类型的数据
            return page_text

    # time.sleep(2)


#定义一个任务对象的回调函数,注意：回调函数必须有一个参数，该参数表示的就是该函数的绑定者，可以理解为特殊函数的执行对象，
#调用task.result()来获取特殊函数的返回结果，return的结果
def parse(task):
    # 多任务的异步爬虫中数据解析或者持久化存储的操作需要写在任务对象的回调函数中
    print(f'我是一个任务对象的回调函数{task.result()}')


#这是一个单个任务对象的事件循环异步调用
def single_thread():
    #创建一个协程对象
    c = func('haha')
    '''
        创建一个任务对象，（基于已有的协程对象创建任务对象）
    '''
    task = asyncio.ensure_future(c)
    #给task任务对象绑定一个回调函数
    task.add_done_callback(parse)


    '''
        创建一个事件循环对象
    '''
    loop = asyncio.get_event_loop()

    '''
        将task任务【一个】对象存储到loop事件中，并启动事件循环对象
        
    '''
    loop.run_until_complete(task)


# 这是多个任务对象的事件循环异步调用
def multi_thread():
    # 创建三个协程对象
    c = func('haha')
    d = func('heihei')
    e = func('xixixixi')
    xiecheng_list = [c, d, e]
    '''
        创建三个任务对象，（基于已有的协程对象创建任务对象）,创建一个空的任务对象列表
    '''
    task_list = []
    for i in xiecheng_list:

        task = asyncio.ensure_future(i)

        # 给task任务对象绑定一个回调函数
        task.add_done_callback(parse)
        task_list.append(task)

    '''
        创建一个事件循环对象
    '''
    loop = asyncio.get_event_loop()

    '''
        将task任务列表中的【多个】对象存储到loop循环事件中
        
        现在这一步不不是真正的实现异步任务执行

    '''
    loop.run_until_complete(asyncio.wait(task_list))

if __name__ == '__main__':
    start_time = time.time()
    multi_thread()
    end_time = time.time() - start_time
    print(f'任务执行了{end_time}秒')

