#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/10/14 10:52'


import requests
from lxml import etree


url = 'http://www.weather.com.cn/weather/101240101.shtml'

res = requests.get(url=url)
text = res.content.decode()
html = etree.HTML(text)
weather = {'7day':[{},{},{},{},{},{},{}]}

day7_list = html.xpath('//*[@id="7d"]/ul/li')
p = 0
for i in day7_list:

    day = i.xpath('h1/text()')[0]  #14日（今天）
    wea = i.xpath('p[@class="wea"]/text()')[0]  #小雨
    #high_tem = i.xpath('p[@class="tem"]/span/text()')[0]  #18
    low_tem = i.xpath('p[@class="tem"]/i/text()')[0] #16℃
    win = i.xpath('p[@class="win"]/em/span/@title')[0]   #'东北风', '北风'
    strength = i.xpath('p[@class="win"]/i/text()')[0] #<3级

    weather['7day'][p] = {'day':day,'wea':wea,'tem':low_tem,'win':win+strength}
    p += 1

print(weather['7day'][1])

today_list = html.xpath('//*[@id="7d"]/ul/li')[0]
today = today_list.xpath('p[@class="tem"]/span/text()')

if not today:
    print(11)