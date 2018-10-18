#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/10/9 0:55'

import requests
import json

url = "http://localhost:63342/%E6%96%B0%E7%89%88%E6%A0%A1%E5%9B%AD%E7%BD%91%E7%99%BB%E5%BD%95/%E6%B1%9F%E8%A5%BF%E5%B8%88%E8%8C%83%E5%A4%A7%E5%AD%A601.htm?_ijt=on6jn570cpckiit6qamg2uuk4q"


res = requests.get(url=url)
print(res.text)

