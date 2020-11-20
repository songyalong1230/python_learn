import requests

'''
    session跟登录与否没有关系，要看你代码，如果你在本次浏览的代码中打开了session就会有，有了session不一定就是登录了
    session跟登录与否没有任何关系，搞清楚session的原理。
    比如，你的网站使用了验证码，那么验证码信息肯定要放session里的，这个时候，session已经存在了，但是和登陆没有关系。
'''
#基于session自动处理cookie

sess = requests.Session()

url = 'https://xueqiu.com/'
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
#该次请求指示为了补货cookie存储到sess中
sess.get(url=url, headers=headers)
print(sess.cookies)
url_1 = 'https://xueqiu.com/9201106692/163683766'
#携带获取到的cookie去请求url
json_data = sess.get(url=url_1, headers=headers).text
# print(json_data)
