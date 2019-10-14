import requests
from lxml import etree
import time
class DouBan:
    def __init__(self):
        self.url = 'https://movie.douban.com/top250'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }
    def parsePage(self, url):
        response = requests.get(url, headers=self.headers)
        html = etree.HTML(response.text)
        movies = html.xpath('//div[@class="info"]')
        for movie in movies:
            item = {}
            title = movie.xpath('div[@class="hd"]/a/span/text()')[0]
            info = movie.xpath('div[@class="bd"]/p[1]')[0].xpath('string(.)').replace('\xa0', '')
            # info1 = info.split('\n')[0]
            # info2= info.split('\n')[1].strip()
            star = movie.xpath('div[@class="bd"]/div[@class="star"]/span/text()')[0]
            quote = movie.xpath('div[@class="bd"]/p[@class="quote"]/span/text()')
            quote = quote[0] if quote else ''
            item['title'] = title
            item['info'] = info.strip()
            item['star'] = star
            item['quote'] = quote
            self.process_item(item)

        time.sleep(2)

        # 下一页的链接
        nextLink = html.xpath('//span[@class="next"]/a/@href')
        if nextLink:
            nextLink = self.url + nextLink[0]
            self.parsePage(nextLink)

    def process_item(self, item):
        with open('douban.txt', 'a', encoding='utf-8') as f:
            f.write(str(item) + '\n')

    def run(self):
        self.parsePage(self.url)


if __name__ == '__main__':
    douban = DouBan()
    douban.run()
