
from kingadmin.kingadmin_base import BaseKingAdmin

class AdminSite(object):
    def __init__(self):
        self.enabled_admins = {}
        #全局 enabled_admins ={ app名称 : { 表名 : 定制的admin model } }
        # {kingadmin :{ customerinfo : CustomerInfoAdmin }}

    def register(self,model_class,admin_class=None):
        """注册admin表"""


        app_name = model_class._meta.app_label     #models.CustomerInfo._meta.app_label
        # 通过表的类名拿到数据库表的名称
        model_name = model_class._meta.model_name  #models.CustomerInfo._meta.model_name

        if not admin_class:
            #实例化 避免多个model共享同一个BaseKingAdmin对象
            admin_class = BaseKingAdmin()
        else:
            admin_class = admin_class()

        admin_class.model = model_class  #将model class 赋值给admin_class

        if app_name not in self.enabled_admins:     #将所有setting的app进行注册
            self.enabled_admins[app_name] = {}

        self.enabled_admins[app_name][model_name] = admin_class



        print(model_class,admin_class)



site = AdminSite()  #第一次调用实例化，之后调用不再实例化，使用内存对象