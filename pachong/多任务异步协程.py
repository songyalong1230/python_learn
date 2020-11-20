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
            - 事件循环执行后如何拿到返回值
            -


'''

import asyncio
import time


async def func(arg):
    print(f'线程{arg}开始')
    time.sleep(2)
    return len(arg)

if __name__ == '__main__':
    #创建一个协程对象
    c = func('haha')

    '''
        创建一个任务对象，（基于已有的协程对象创建任务对象）
    '''
    task = asyncio.ensure_future(c)

    '''
        创建一个事件循环对象
    '''
    loop = asyncio.get_event_loop()

    '''
        将task任务【一个】对象存储到loop事件中，并启动事件循环对象
        
    '''
    loop.run_until_complete(task)

