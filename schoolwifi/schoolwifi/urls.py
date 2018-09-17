"""schoolwifi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include

from user import views

urlpatterns = [
    #admi后台
    path('admin/', admin.site.urls),
    #进入首页
    path('index/',views.get_index,name='get_index'),

    #注册
    path('register/',views.user_register,name='register'),

    #用户激活
    re_path('active/(?P<active_code>.*)/',views.user_active,name='user_active') ,#用户激活

    #登录
    path('login/',views.user_login,name='login'),
    #验证码
    path('reflesh_code',views.reflesh_code,name='reflesh_code'),
    #登出
    path('logout/',views.user_logout,name='logout'),
    #教程
    path('guide/',views.user_guider,name='guider'),
    #连接首页
    path('connect_home/',views.connect_home,name="connect_home"),
    #连接动作
    path('connect/',views.get_connect,name="connect"),
    #断开连接动作
    path('disconnect/',views.cut_connect,name="disconnect"),



]
