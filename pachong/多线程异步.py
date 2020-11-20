from multiprocessing.dummy import Pool
from time import sleep
import time
#使用线程池进行异步爬虫
a = Pool(3)
list_data = [
    '11', '223', '3322'
]
def func(arg):
    print(f'线程{arg}开始')
    sleep(2)
    return len(arg)


if __name__ == '__main__':
    start_time = time.time()
    print(start_time)
    b = a.map(func, list_data)
    print(time.time() - start_time)