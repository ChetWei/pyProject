#   -*-coding:utf-8 -*-

from datetime import  datetime

import os
import pymysql


os.environ.setdefault('DJANGO_SETTING_MODULE', 'newWifi.settings')
import django
django.setup()
from wifi.models import Account,Connect



def get6(number):
    if len(number) == 2:
        return "0000"+number
    elif len(number) == 3:
        return "000"+number
    elif len(number) == 4:
        return "00"+number
    elif len(number) == 5:
        return "0"+number
    elif len(number) == 6:
        return number





db = pymysql.connect(host='localhost', user='root', password='110811', port=3306, charset='utf8', db='school')
query_cursor = db.cursor()

query_sql = 'SELECT * FROM new where useful = %s'

query_cursor.execute(query_sql,'1')


results = query_cursor.fetchall()

for row in results:
    account = get6(row[0])
    password = row[1]
    name = row[2]
    obj = Account(account=account,password=password,name=name,is_available=True,is_using=False,create_time=datetime.now())
    obj.save()

if __name__ == "__main__":
    connect_obj_list = Connect.objects.all().order_by('-login_time')
    for obj in  connect_obj_list:
        print(obj.id)