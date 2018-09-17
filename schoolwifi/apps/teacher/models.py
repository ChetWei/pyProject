from django.db import models
from datetime import datetime
# Create your models here.

#user table

class Teacher(models.Model):
    GENDER_CHOICE = (
        ('male','男'),
        ('female','女')
    )
    account = models.CharField(verbose_name='账号',max_length=16,primary_key=True,unique=True)
    name = models.CharField(verbose_name='姓名',max_length=16)
    gender = models.CharField(verbose_name="性别",choices=GENDER_CHOICE,max_length=8,null=True,blank=True)
    age = models.IntegerField(verbose_name='年龄',null=True,blank=True,default='')
    password = models.CharField(verbose_name='密码',max_length=16,null=False,blank=False)
    encode_pwd = models.CharField(verbose_name='加密密码',max_length=32,null=False,blank=False)
    is_useful = models.BooleanField(verbose_name='是否可用',default=True)
    is_consume = models.BooleanField(verbose_name='是否被分配使用',default=False)
    dept  = models.CharField(verbose_name='所属学院部门',max_length=32,null=True,blank=True,default='')
    position = models.CharField(verbose_name='职位',max_length=32,null=True,blank=True,default='')
    add_time = models.DateTimeField(verbose_name='添加时间',auto_now_add=True)
    last_modify_time = models.DateTimeField(verbose_name='最后更新时间',auto_now=True)

    def __str__(self):
        return self.account

    class Meta:
        db_table='teacher'