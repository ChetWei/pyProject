#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/10/10 18:23'
import re
import math

import requests
from lxml import etree

'''根据金额返回对应时长'''
def buy_time(money):
    if money < 1:
        return math.floor(money / 0.3)*60

    elif money == 1:
       return 3*60

    elif money > 1 and money < 10:
        return math.floor(money / 0.25)*60

    elif money == 10:
        return 50*60

    elif money > 10 and money < 30:
        return 50*60 + math.floor((money - 10) / 0.2)*60

    elif money == 30:
        return 200*60

    elif money > 30:
        return 200*60 + math.floor((money - 30) / 0.18)*60




def get_nanchang_weather():
    url = 'http://www.weather.com.cn/weather/101240101.shtml'

    res = requests.get(url=url)
    text = res.content.decode()
    html = etree.HTML(text)
    weather = {'7day': [{}, {}, {}, {}, {}, {}, {}]}

    day7_list = html.xpath('//*[@id="7d"]/ul/li')
    p = 0
    for i in day7_list:
        day = i.xpath('h1/text()')[0]  # 14日（今天）
        wea = i.xpath('p[@class="wea"]/text()')[0]  # 小雨
        high_tem = i.xpath('p[@class="tem"]/span/text()')[0]  # 18
        low_tem = i.xpath('p[@class="tem"]/i/text()')[0]  # 16℃
        win = i.xpath('p[@class="win"]/em/span/@title')[0]  # '东北风', '北风'
        strength = i.xpath('p[@class="win"]/i/text()')[0]  # <3级

        weather['7day'][p] = {'day': day, 'wea': wea, 'tem': high_tem + '/' + low_tem, 'win': win + strength}
        p += 1

    #print(weather['7day'][1])
    return weather




'''判断合法的ip'''
async def valiable_ip(ip:str) -> bool:
    pattern = "^(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|[1-9])\\.(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)\\.(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)\\.(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)$"
    if re.match(pattern, ip):
        #pattern = "^(10\\.(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)\\.(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)\\.(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)$)"
        if ip == '10.110.0.1':
            return False
        return True
    else:
        return False





async def get_ip(ip:str) -> str:
    return f'你的ip为：{ip}'