from django import conf     #动态获取settings已经导入的app

def kingadmin_auto_discover():
    for app_name in conf.settings.INSTALLED_APPS:  # 获取所有app的名字
        try:
            mod = __import__('%s.kingadmin' % app_name)  # 将每个app下面的kingadmin模块导入执行
            print(mod.kingadmin)
        except ImportError:
            pass