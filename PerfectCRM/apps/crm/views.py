from django.shortcuts import render
from django.contrib.auth.decorators import login_required   #防止未登录进入首页

# Create your views here.

@login_required()
def dashbord(request):

    return  render(request, 'crm/dashboard.html')