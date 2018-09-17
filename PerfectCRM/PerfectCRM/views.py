from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout


"""用户登录"""
def user_login(request):
    error_msg = ''
    if request.method == "POST":
        username = request.POST.get("username",None)
        password = request.POST.get("password",None)
        print(username,password)
        #验证  验证结果返回对象或None
        user = authenticate(username=username,password=password)

        if user:
            # 登录（生成session）
            login(request,user)
            # return redirect('/crm/')
            return redirect(request.GET.get('next','/crm')) #未登录进入状态，输入正确用户名之后进入之前想要进入的页面，参数next为空默认值首页

        else:
           error_msg = "用户名或密码错误"
    return render(request,'login.html',{
        'error_msg':error_msg,
    })


"""用户退出"""
def user_logout(request):
    logout(request) #清除session
    return redirect('/login')