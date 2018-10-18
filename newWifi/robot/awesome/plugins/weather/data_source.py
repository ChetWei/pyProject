#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/10/10 16:32'


import requests
from lxml import etree


'''根据城市id获取城市7天的天气'''
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
        #high_tem = i.xpath('p[@class="tem"]/span/text()')[0]  # 18
        high_tem = i.xpath('p[@class="tem"]/span/text()')  # 18
        if not high_tem:
            high_tem = ''
        else:
            high_tem = high_tem[0]+'/'

        low_tem = i.xpath('p[@class="tem"]/i/text()')[0]  # 16℃
        win = i.xpath('p[@class="win"]/em/span/@title')[0]  # '东北风', '北风'
        strength = i.xpath('p[@class="win"]/i/text()')[0]  # <3级

        weather['7day'][p] = {'day': day, 'wea': wea, 'tem': high_tem + low_tem, 'win': win + strength}
        p += 1

    weather7d = weather['7day']
    weather_info = '南昌天气'
    for one_day_dict in weather7d:
        # day[1]  {'day': '15日（明天）', 'wea': '小雨转阴', 'tem': '20/16℃', 'win': '东北风<3级'}
        today = one_day_dict['day']
        wea = one_day_dict['wea']
        tem = one_day_dict['tem']
        win = one_day_dict['win']
        weather_info = weather_info + '\n' + today + '\n天气:' + wea + '\n温度:' + tem + '\n风向' + win

    return weather_info





