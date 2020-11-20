from lxml import etree
import requests
url = 'http://pic.netbian.com/'
url = 'http://pic.netbian.com/4kmeinv/index_%d.html'
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
for page in range(1, 6):
    if page == 1:
        new_url = 'http://pic.netbian.com/'
    else:
        new_url = format(url%page)
    response = requests.get(new_url, headers=headers).text
    tree = etree.HTML(response)
    li_list = tree.xpath('//div[@class="slist"]/ul/li')
    for li in li_list:
        img_url = 'http://pic.netbian.com' + li.xpath('.//img/@src')[0]
        img_name = li.xpath('./a/b/text()')[0].encode('ISO-8859-1').decode('gbk') + '.jpg'
        img_content = requests.get(img_url, headers=headers).content
        with open(f'./imgs/meinv/{img_name}', 'wb') as f:
            f.write(img_content)
        print(img_name + '下载完毕！！！')