#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/10/14 19:29'

import requests
from lxml import etree
import re


def today_weather_info():
    url = 'http://www.weather.com.cn/weather/101240101.shtml'

    res = requests.get(url=url)
    text = res.content.decode()
    html = etree.HTML(text)
    day7_list = html.xpath('//*[@id="7d"]/ul/li')

    today = day7_list[0]

    day = today.xpath('h1/text()')[0]  # 14日（今天）
    wea = today.xpath('p[@class="wea"]/text()')[0]  # 小雨

    high_tem = today.xpath('p[@class="tem"]/span/text()')  # 18
    if not high_tem:
        high_tem = ''
    else:
        high_tem = high_tem[0] + '/'

    low_tem = today.xpath('p[@class="tem"]/i/text()')[0]  # 16℃
    win = today.xpath('p[@class="win"]/em/span/@title')[0]  # '东北风', '北风'
    strength = today.xpath('p[@class="win"]/i/text()')[0]  # <3级

    return {'wea':wea,'low_tem':low_tem,'win':win}




def care(wea,lowtem):

    error = '机器猫今天生病了不能给你播天气了,亲爱的主人记得出门看看哦'
    try:
        lowtem = int(re.match('(\d+)℃', lowtem).group(1))
        rain_info = ''
        clothes_info = ''
        if '雨' in wea:
            rain_info = '今天会下雨哦,记得带上雨伞'
        if lowtem > 25:
            clothes_info = '今天机器猫要穿T恤，谁也不要拦我'
        elif lowtem <= 25 and lowtem > 20:
            clothes_info = '机器猫都可以穿衬衫加短袖了'
        elif  lowtem <= 20 and lowtem > 15:
            clothes_info = '今天有点冷呢,三件衣服妥妥的呀'
        elif lowtem <= 15 and lowtem > 10:
            clothes_info = '很冷哦,记得穿上袄子呢'
        elif lowtem <= 10 and lowtem > 5:
            clothes_info = '机器猫都瑟瑟发抖了,衣服一定要多穿啦'
        elif lowtem <= 5 and lowtem >0:
            clothes_info = '机器猫已经冻得不行啦,你快把所有衣服都穿上吧~'
        elif lowtem <= 0 :
            clothes_info = '建议你裹上被子呢,都结冰了'
        return rain_info,clothes_info

    except:
        return error,''



