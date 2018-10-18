#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/10/15 18:12'

import requests

def ask_tulin(info,key="255c0b489b3f43729e813b5f7bd00938"):

    url = 'http://www.tuling123.com/openapi/api'

    send = {
        "key":key,
        "info":info
    }

    res = requests.post(url=url,data=send)

    code = res.json()['code']
    text = res.json()['text']
    # 40001参数key错误
    # 40002请求内容info为空
    # 40007数据格式异常 / 请按规定的要求进行加密
    if code == 40001 or code == 40002 or code == 40007 or text == '':
        return '我好像没听懂你的意思，可以明确一点吗？'

    elif code == 40004:       #当天请求次数已使用完
        return 40004

    return text

