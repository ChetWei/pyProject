#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/10/11 21:12'

from datetime import  datetime

import os




os.environ.setdefault('DJANGO_SETTING_MODULE', 'newWifi.settings')
import django
django.setup()
from wifi.models import Account

# db = pymysql.connect(host='localhost', user='root', password='110811', port=3306, charset='utf8', db='new_wifi')
# cursor = db.cursor()
print(datetime.now)
obj = Account(account='000085',password='215006',name='杨晓平',is_available=True,is_using=False,create_time=datetime.now())
obj.save()