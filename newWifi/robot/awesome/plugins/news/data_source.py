#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/10/14 18:25'

import requests
from lxml import etree


def get_today_news(top=10):
    url = 'http://www.zaobao.com/'
    res = requests.get(url=url)
    text = res.text
    html = etree.HTML(text)
    li_list = html.xpath('//*[@id="global-latest-focus"]//div[@class="view-content"]/ul[@class="post-list"]/li')

    news = ''

    for i,li in enumerate(li_list[0:top]):
        i = i+1
        title = li.xpath('div/a/div/span[1]/text()')[0]
        news = news + str(i) + ':' + title +'\n'

    return news

