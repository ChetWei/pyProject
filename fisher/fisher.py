#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/9/16 17:43'
import json

from flask import Flask


app = Flask(__name__)
app.config.from_object('config')

from app.web import book



if __name__ == '__main__':
    #生产环境 nginx + uwsgi
    #避免加载执行,防止和nginx + uwsgi已经启动的服务器冲突
    app.run(host='0.0.0.0',debug=app.config['DEBUG'],port=app.config['PORT'])  #启动web服务器,指定ip地址任意访问,开启调试，在浏览器中显示错误,指定端口

