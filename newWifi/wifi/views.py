from django.shortcuts import render
from django.views.generic.base import View
# Create your views here.

class LoginView(View):
    def get(self,request):
        return render(request,'江西师范大学01.html')


class LoginSuccess(View):
    def get(self,request):
        return render(request,'success.html')


class LoginFail(View):
    def get(self,request):
        return render(request,'fail.html')