from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required   #防止未登录进入首页

from kingadmin import app_setup
from kingadmin.sites import site




app_setup.kingadmin_auto_discover()
print("enabled_admins",site.enabled_admins)


"""首页"""
@login_required()
def app_index(request):
    return render(request,'kingTemplates/app_index.html',{
        'site':site,    #site   实例化的内存对象

    })


"""用户登录"""
def king_login(request):
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
            return redirect(request.GET.get('next','/kingadmin/')) #未登录进入，输入正确用户名之后进入之前想要进入的页面，参数next为空默认值首页

        else:
           error_msg = "用户名或密码错误"
    return render(request,'kingTemplates/login.html',{
        'error_msg':error_msg,
    })


"""用户退出"""
def king_logout(request):
    logout(request) #清除session
    return redirect('/kingadmin/login')


@login_required()
def table_obj_list(request,app_name,model_name):
    """取出指定model里的数据返回给前端"""
    admin_class = site.enabled_admins[app_name][model_name]
    print("admin class model" ,admin_class.model)
    print("admin class",admin_class)


    querysets = admin_class.model.objects.all()
    print(querysets)

    return render(request,'kingTemplates/table_obj_list.html',{
        'querysets':querysets,
        'admin_class':admin_class
    })