from django.conf.urls import url,include
from kingadmin import views


urlpatterns = [
    url(r'^$',views.app_index,name='app_index'),
    url(r'^login/$', views.king_login,name='king_login'),
    url(r'^logout/$', views.king_logout,name='king_logout'),

    url(r'^/(\w+)/(\w+)/$', views.table_obj_list,name='table_obj_list'),

]