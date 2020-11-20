import requests
import re
import time
def pachong():
    url = 'https://sc.chinaz.com/tag_tupian/YaZhouMeiNv.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    request_text = requests.get(url=url, headers=headers).text
    ex = '<a.*?<img src2="(.*?)" alt.*?</a>'
    img_src_list = re.findall(ex, request_text, re.S)
    print(img_src_list)
    for i in img_src_list:
        name = i.split('/')[-1]
        url = 'http:' + i
        img = requests.get(url, headers=headers).content
        with open(f'./imgs/{name}', 'wb') as f:
            f.write(img)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pachong()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
