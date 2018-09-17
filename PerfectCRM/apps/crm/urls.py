from django.conf.urls import url
from crm import views


urlpatterns = [

    url(r'^$', views.dashbord, name='sales_dashboard'),




]