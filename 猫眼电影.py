from lxml import etree
import requests
import time
import re
import json

def getHTMLtext(url):
    '''获取页面信息'''
    try:
        header = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
        r = requests.get(url,headers = header,timeout = 5)
        r.raise_for_status()  #如果状态不是200，引发error异常
        return r.text
        # print(r.text)

    except:
        return "爬取失败"

# def  parse(html):
#     '''正则提取信息'''
#     pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
#                          + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
#                          + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
#     items = re.findall(pattern, html)
#     items = pattern.findall(html)
#     # print(items)
#     list1 = []
#     for item in items:
#         dict1 = {}
#         dict1["排名"]=item[0]
#         # dict1["图片"]=item[1]
#         dict1["电影名"]=item[2]
#         dict1["主演"]=item[3].strip()[3:]
#         dict1["上映时间"]=item[4].strip()[5:]
#         dict1["评分"]=item[5]+item[6]
#         list1.append(dict1)
#     return list1
    # print(list1)

def  parse(html):
    '''XPath提取信息'''
    items = etree.HTML(html)
    texts= items.xpath("//dd")   #获取所有dd标签
    list1=[]
    for text in texts:
        dict1 = {}
        dict1["排名"]=text.xpath('./i/text()')[0]
        # dict1["图片链接"]=text.xpath('.//img//@src')[0]
        dict1["电影名"]=text.xpath('.//p[@class="name"]/a/text()')[0]
        dict1["主演"]=text.xpath('.//p[@class="star"]/text()')[0].replace("主演：","").strip()
        dict1["上映时间"]=text.xpath('.//p[@class="releasetime"]/text()')[0].replace("上映时间：","")
        dict1["评分"]=text.xpath('.//p[@class="score"]//text()')[0]+text.xpath('.//p[@class="score"]//text()')[1]
        # print(dict1["图片链接"])
        list1.append(dict1)
    return list1

def save(texts):
    '''保存信息'''
    for text in texts:
        with open('maoyan.text','a',encoding='utf-8') as f:
            f.write(str(text) + '\n')
            print("保存成功")

if __name__ == '__main__':
    for i in range(10):
        url = f'https://maoyan.com/board/4?offset={i*10}'
        html = getHTMLtext(url)
        texts = parse(html)
        save(texts)
