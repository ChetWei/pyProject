#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/10/9 12:58'


from flask import Flask,render_template,request

app = Flask(__name__)


@app.route('/login',methods=['GET'])
def hello_world():
    return render_template('login.html')


@app.route('/login',methods=['POST'])
def login():
    ip = request.form['ip']
    print(ip)

    return '<h1>hello</hello>'



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
