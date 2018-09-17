from django.db import models
from django.contrib.auth.models import AbstractUser

from teacher.models import Teacher

from datetime import datetime
 # Create your models here.

"""用户表"""
class UserProfile(AbstractUser):
    # 继承django自带的User，可以自己扩展字段
    #id,password,last_login,is_superuser,usern_name,first_name,last_name,email,is_staff,is_active,date_joined
    #user_name , password is required
    GENDER_CHOICE = (
        ('male', '男'),
        ('female', '女')
    )
    GRADE_CHOICE = (
        ('Freshman','大一'),
        ('Sophomore','大二'),
        ('Junior','大三'),
        ('Senior','大四'),
        ('Graduate','毕业生')
    )
    nick_name = models.CharField(verbose_name='昵称',max_length=32,null=True,blank=True)
    school_number = models.CharField(verbose_name='学号',max_length=16)
    gender = models.CharField(verbose_name="性别", choices=GENDER_CHOICE, max_length=8, null=True, blank=True)
    grade = models.CharField(verbose_name="年级",choices=GRADE_CHOICE,max_length=16, null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(verbose_name='最后登录ip',null=True,blank=True)
    last_login_time = models.DateTimeField(verbose_name='最后登录时间',null=True,blank=True)
    last_connect_account = models.CharField(verbose_name='最后连接的tea账号',null=True,blank=True,max_length=16)
    last_connect_ip = models.GenericIPAddressField(verbose_name="最后连接ip",null=True,blank=True)
    last_connect_time = models.DateTimeField(verbose_name="最后连接时间",null=True,blank=True)
    connect_times = models.IntegerField(verbose_name='连接次数',null=True,blank=True)
    authorization_times = models.IntegerField(verbose_name='授权次数',null=True,blank=True)
    is_connecting = models.BooleanField(verbose_name="是否正在连接状态",default=False)


    def __str__(self):
        return self.username


    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name



"""用户操作表，与用户表是一对多的关系"""
class UserOperation (models.Model):
    user = models.ForeignKey(UserProfile,verbose_name="用户外键",on_delete=models.CASCADE)
    connect_time = models.DateTimeField(verbose_name='连接时间')
    discut_time = models.DateTimeField(verbose_name='断开时间')
    connect_ip = models.GenericIPAddressField(verbose_name='连接ip')
    discut_ip = models.GenericIPAddressField(verbose_name='断开ip')



"""用户授权表，多对多的中间表"""
class Authorized(models.Model):
    user = models.ForeignKey(UserProfile,verbose_name="用户外键",on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,verbose_name='教师外键',on_delete=models.CASCADE,null=True)
    expiration_time = models.DateTimeField(verbose_name='授权过期时间')
    privilege = models.BooleanField(verbose_name='是否特权',default=False)
    is_authorized = models.BooleanField(verbose_name='是否授权',default=False)


"""验证码表,独立的表"""
class EmailVerifyRecord(models.Model):
    send_choices = (
        ('register','注册'),
        ('forget','找回密码'),
        ('update_email','修改邮箱')
    )

    code = models.CharField('验证码',max_length=20)
    email = models.EmailField('邮箱',max_length=50)
    send_type = models.CharField(choices=send_choices,max_length=20,verbose_name='验证类型')
    send_time = models.DateTimeField(default=datetime.now,verbose_name='发送时间')

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name