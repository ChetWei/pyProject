#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/10/18 12:09'

from spider import connect


conn = connect.Connect()


#login_res = conn.remote_connect(connect_ip='10.110.133.22',connect_username='000405',connect_password='{B}SGptNzg3Nzg3')
#print(login_res)
"""
登录成功返回:login_ok,,bQ0qQMxJvKa38joL2%2FjcHkC%2BmsG82yAhTQy6ooDWqw1beAUfdeKT5kJVJK3DDs2Yw8U5Qi1e%2FPINC4XlaTHpBRowytvWUlyv...

登录失败：
    1）E2620: You are already online.(已经在线了)    》 当前账号已经在这台电脑登录了
    2）


"""

logout_res = conn.remote_cut(cut_ip='10.110.133.22',cut_username='000405')
print(logout_res)