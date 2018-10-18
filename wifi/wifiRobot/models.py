from django.db import models
from datetime import  datetime

"""用户表"""
class User(models.Model):

    identity_choices = (
        (0,'超级用户'),
        (1,'普通用户'),
        (2,'VIP'),
        (3,'SVIP'),
    )

    qq_number = models.CharField(verbose_name='qq账号',primary_key=True,null=False,blank=False,max_length=16)
    identity = models.IntegerField(verbose_name='用户身份',choices=identity_choices,default=1)
    is_online = models.BooleanField(verbose_name='是否在线',default=False)
    remain_time = models.IntegerField(verbose_name='剩余时长',default=0)
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=datetime.now)
    last_modify_time = models.DateTimeField(verbose_name='最后修改时间',auto_now=datetime.now)
    login_times = models.IntegerField(verbose_name='累计登录次数',default=0)
    last_login_ip = models.CharField(verbose_name='最后登录ip',max_length=20,default='')
    last_login_time = models.DateTimeField(verbose_name='最后登录时间',null=True,blank=True)
    last_logout_time = models.DateTimeField(verbose_name='最后断开时间',null=True,blank=True)
    last_login_account = models.CharField(verbose_name='最后登录使用账号',null=True,blank=True,max_length=16)
    free_chances = models.BooleanField(verbose_name='免费权限是否已经使用',default=True)
    newest_recharge = models.FloatField(verbose_name='上次充值金额',null=True)
    accumulated_recharge = models.FloatField(verbose_name='累计充值金额',null=True,default=0)
    ban = models.BooleanField(verbose_name='是否被禁用',default=False)




"""连接表"""
class Connect(models.Model):
    #不指名主键会默认生成id自增
    ip = models.CharField(verbose_name='用户登录ip',max_length=16)
    login_time = models.DateTimeField(verbose_name='登录时间',default=datetime.now)
    logout_time = models.DateTimeField(verbose_name='退出时间',null=True,blank=True)
    qq_number = models.ForeignKey(verbose_name='用户表',to='User',to_field='number',on_delete=models.CASCADE)
    tea_account = models.ForeignKey(verbose_name='账号表',to='Account',to_field='account',on_delete=models.SET_NULL,null=True)


"""账号表"""
class Account(models.Model):
    account = models.CharField(verbose_name='tea账号',primary_key=True,max_length=8)
    password = models.CharField(verbose_name='密码',null=False,blank=False,max_length=32)
    name = models.CharField(verbose_name='姓名',max_length=16)
    is_available = models.BooleanField(verbose_name='是否可用',default=True)
    is_using = models.BooleanField(verbose_name='是否正在使用',default=False)
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=datetime.now)


