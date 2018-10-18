#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/10/11 22:46'

import django
django.setup()

import random


from wifi.models import Account,User




"""
查询qq用户是否存在
:return: True,False
"""
def existUser(qq):
    obj = User.objects.filter(number=qq)
    if obj:
        return True
    else:
        return False




"""
查询用户剩余时间
return INT
"""
def queryRemainTime(qq):
    user_obj = User.objects.filter(number=qq)[0]
    remain_time = user_obj.remain_time
    return remain_time



def loginOperation(qq):
    user_obj = User.objects.filter(number=qq)
    if not user_obj :
        #用户不存在，创建用户记录
        user = User(number=qq,remain_time=60,free_chances=False)
        user.save()
        p = random.randint(0,634)
        account_obj = Account.objects.filter(is_using=False)[p]  #随机的账号对象
        account = account_obj.account
        password = account_obj.password










    else:
        #用户记录存在
        pass


if __name__ == "__main__":
    user =  User.objects.filter(number=592190443)[0]
    user.identity = 0
    user.save()
    print(user.get_identity_display())