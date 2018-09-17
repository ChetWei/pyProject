#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/9/16 17:43'

from flask import Flask,make_response
from config import DEBUG,PORT

app = Flask(__name__)
app.config.from_object('config')


#@app.route('/hello/')        #添加路由,兼容/ 。。/ 内部重定向
def hello():                #基于函数的视图
    return "Hello World"



def hi():
    """
    status code 200 ,400,301
    content-type : http headers
    content-type = text/html  默认值
    封装成 Response对象
    """
    headers = {
        'content-type':'text/plain', #text/html 默认 ,application/json
        #'location':'http://www.baidu.com'  #请求转发，状态码设置为301
    }
    # response = make_response('<html></html>',301)
    # response.headers = headers
    # return response  #返回内容会被服务器解析成html代码

    return '<html></html>', 301, headers


app.add_url_rule('/hello/',view_func=hello)
app.add_url_rule('/hi',view_func=hi)

if __name__ == '__main__':
    #生产环境 nginx + uwsgi
    #避免加载执行,防止和nginx + uwsgi已经启动的服务器冲突
    app.run(host='0.0.0.0',debug=app.config['DEBUG'],port=app.config['PORT'])  #启动web服务器,指定ip地址任意访问,开启调试，在浏览器中显示错误,指定端口

