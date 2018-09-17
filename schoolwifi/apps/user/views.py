from django.shortcuts import render, redirect, HttpResponse
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password,check_password #密码加密存储


from datetime import datetime
from io import BytesIO
import re
import base64
import json



from user import models
from user import utils

# Create your views here.

"""首页"""
def get_index(request):
    return render(request, 'index.html')


"""异步刷新验证码"""
def reflesh_code(request):
    if request.method == "GET":
        #生成新的验证码
        mstream, stream_value,code_text = utils.generate_verify_image()
        print("code_text",code_text)
        #将内存中的图片清除
        mstream.close()
        #将bytes base64转为str
        stream_value_base64 = str(base64.b64encode(stream_value), 'utf-8')
        #覆盖新的用户session验证
        request.session['check_code'] = code_text
        #返回验证码图
        resp = {'img':stream_value_base64,'status':200}
        return HttpResponse(json.dumps(resp), content_type='application/json')



"""用户登录"""
def user_login(request):
    error_msg = ''
    if request.method == "POST":
        #验证码校验
        post_check_code = request.POST.get('check_code','')
        print("post_check_code:",post_check_code)
        session_check_code = request.session['check_code']
        print("session_check_code:",session_check_code)

        if post_check_code.lower() == session_check_code.lower():
            print("验证码通过")
            next = request.GET.get('next', '/index')
            username = request.POST.get("username", None)
            password = request.POST.get("password", None)
            # 验证,修改继承，邮箱用户名都可验证  验证结果返回对象或None
            authenticate = utils.EmailAuthBackend()
            user = authenticate.authenticate(request=request,username=username,password=password)
            if user:
                #判断用户是否激活
                user_status = user.is_active
                if user_status:
                    # 登录（生成session）
                    login(request, user)
                    return redirect(next)  # 未登录进入状态，输入正确用户名之后进入之前想要进入的页面，参数next为空默认值首页

                else:
                    #未激活
                    error_msg = '用户未激活,请查收邮箱激活链接'
                    return render(request,'login.html',{'error_msg':error_msg})

            else:
                error_msg = "用户名或密码错误"
                return render(request,'login.html',{
                    'error_msg':error_msg
                })
        else:
            error_msg = "验证码错误"

    return render(request, 'login.html', {
        'error_msg': error_msg
    })





"""用户注册"""
def user_register(request):

    error = ''

    if request.method == 'POST':
        email = request.POST.get("email","")
        snumber = request.POST.get("snumber","")
        pwd1 = request.POST.get("pwd1","")
        pwd2 = request.POST.get("pwd2","")

        #验证邮箱是否合法
        if not utils.check_email(email):
            error = '邮箱不合法'
            return render(request,'register.html',{
                'error_msg':error
            })
        #验证学号是否存在

        #验证密码是否相同，并且满足要求
        elif not pwd1 == pwd2:
            error = '两次密码输入不相同'
            return render(request,'register.html', {
                'error_msg': error
            })

        #输入字段都合法，进行数据库注册
        #创建新用户，将邮箱写入数据库，生成对应的验证码，发送到邮箱，
        # 通过邮箱验证码，到激活账号页面进行激活


        #判断邮箱是否存在
        elif models.UserProfile.objects.filter(email=email):
            error = '邮箱已注册'
            return render(request, 'register.html',{
                'error_msg': error
            })


        else:
            user_obj = models.UserProfile()
            user_obj.username = email #用户邮箱当做用户名
            user_obj.email = email
            user_obj.is_active = False
            user_obj.password = make_password(pwd1) #加密存储

            user_obj.save()

            #发送邮箱激活账号链接
            emailVerify = utils.EmailVerify()
            emailVerify.send_email(email,'register')

            #转到登录 中间页面
            return render(request,'register_redirect.html')


    return render(request,'register.html')



"""用户邮箱激活"""
def user_active(request,active_code):
    if request.method == 'GET':
        #查询邮箱的验证码是否存在,可能有相同概率，
        email_verify_obj_lists = models.EmailVerifyRecord.objects.filter(code=active_code)

        #如果存在,找出该验证码对应的所有邮箱，并且从所有邮箱中找出有对应用户的邮箱
        if email_verify_obj_lists:
            for email_verify_obj in email_verify_obj_lists:
                email = email_verify_obj.email

                user = models.UserProfile.objects.filter(email=email).first()

                if user: #如果邮箱对应的用户存在
                    user.is_active = True #激活用户
                    user.save()

                    #激活成功跳到登录
                    return render(request,'active_redirect.html')


        else:  #验证码对应的验证码表记录不存在
            return redirect('/register')




"""用户退出"""
def user_logout(request):
    logout(request)  # 清除session
    return redirect('/login')




"""连接页面"""
@login_required()
def connect_home(request):
    return render(request, 'connector.html')




"""使用教程"""
def user_guider(request):
    return render(request, 'guider.html')




"""立即连接"""
@login_required()
def get_connect(request):
    if request.method == "POST":
        # 获取ip
        ip = request.POST.get("ip", "")
        action = request.POST.get("action", "")
        if request.user.is_authenticated:
            # 判断用户是否登录
            user = request.user
            print(user)
            if utils.check_ip(ip):
                # 判断是否合法ip
                try:
                    authorized_obj = models.Authorized.objects.filter(user=user)[0]  # 判断用户是否在授权表,另外用户是否已经分配了tea account

                    if authorized_obj.is_authorized:
                        # 判断用户是否在授权列表

                        current_tea_account = authorized_obj.teacher

                        if current_tea_account is None:
                            # 判断用户是否已经分配了tea account

                            # 获取未分配的tea account
                            teacher_obj = utils.get_undistributed_account()
                            print(type(teacher_obj))
                            # 分配之后设置已经分配
                            teacher_obj.is_consume = True
                            teacher_obj.save()

                            authorized_obj.teacher = teacher_obj
                            authorized_obj.save()

                        # 使用requests post进行连接
                        connector = utils.RequestsConnect()
                        connnect_res = connector.remote_connect(connect_ip=ip,
                                                                connect_account=authorized_obj.teacher.account,
                                                                connect_password=authorized_obj.teacher.encode_pwd)

                        if connnect_res == "login_ok":
                            # 远程连接成功，记录相关信息，返回信息到前端
                            # 更新记录：
                            # 用户表：更新用户连接次数,最后连接时间，ip,连接状态
                            user.connect_times += 1
                            user.last_connect_time = datetime.now()
                            user.last_connect_ip = ip
                            user.is_connecting = True
                            user.save()
                            # 用户操作记录表  插入一条新的记录
                            useroperation_obj = models.UserOperation()
                            useroperation_obj.user = user
                            useroperation_obj.connect_ip = ip
                            useroperation_obj.connect_time = datetime.now()
                            useroperation_obj.save()

                            # 返回信息到前端
                            return HttpResponse('{"msg":"login_ok","status":"200"}', content_type='application/json')

                        elif connnect_res == "网络好像有点延迟":
                            # 远程连接失败，返回信息到前端
                            return HttpResponse('{"msg":"delay","status":"500"}', content_type='application/json')

                        elif connnect_res == "请等待5分钟再尝":
                            # 远程连接失败，返回信息到前端
                            return HttpResponse('{"msg":"limit","status":"404"}', content_type='application/json')

                        else:
                            return HttpResponse('{"msg":"login_fail","status":"404"}', content_type='application/json')

                    else:
                        #用户没有在授权列表
                        return HttpResponse('{"msg":"unauthorized","status":"404"}', content_type='application/json')


                except Exception as e:
                    print(e)


            else:
                #不合法的ip
                return HttpResponse('{"msg":"invalid_ip","status":"500"}', content_type='application/json')

        else:
            #未登录
            return redirect('/login')




"""断开连接"""
@login_required()
def cut_connect(request):
    if request.method == "POST":
        # 获取ip
        ip = request.POST.get("ip", "")
        action = request.POST.get("action", "")
        if request.user.is_authenticated:
            # 判断用户是否登录
            user = request.user

            if utils.check_ip(ip):
                # 判断是否合法ip
                is_connecting = user.is_connecting
                if is_connecting:
                    #判断是否正在连接状态
                    #获取上次连接的ip地址,tea 账号
                    last_login_ip = user.last_connect_ip
                    last_connect_account = user.last_connect_account
                    connector = utils.RequestsConnect()
                    # 实现远程注销
                    connector.remote_cut(cut_ip=last_login_ip,cut_account=last_connect_account)
                    #更改连接状态
                    user.is_connecting = False
                    return HttpResponse('{"msg":"logout_ok","status":"200","is_ok":"yes"}',
                                        content_type='application/json')
                else:
                    #用户没有连接，无需断开
                    return HttpResponse('{"msg":"logout_fail","status":"200","is_ok":"yes"}',
                                        content_type='application/json')

            else:
                # 不合法的ip
                return HttpResponse('{"msg":"invalid_ip","status":"500"}', content_type='application/json')
        else:
            #用户没有登录
            return redirect('/login')




"""获取授权"""
@login_required()
def get_authorization(request):
    pass


