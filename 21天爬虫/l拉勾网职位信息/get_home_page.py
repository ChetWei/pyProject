#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/9/30 22:01'
import requests

url = "https://www.lagou.com/"

headers = {
    'Host': 'www.lagou.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.lagou.com/jobs/list_%E5%A4%A7%E6%95%B0%E6%8D%AE?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=',
}

res = requests.get(url=url,headers=headers)
print(res.status_code)
print(res.content.decode('UTF-8'))