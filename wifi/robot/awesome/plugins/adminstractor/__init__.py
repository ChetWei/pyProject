#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/10/14 22:48'

import re
from none import on_command,CommandSession
from .data_source import *

import os
os.environ.setdefault('DJANGO_SETTING_MODULE', 'newWifi.settings')
import django
django.setup()

import random
from datetime import datetime

from wifi.models import Account,User,Connect


"""管理员为用户添加时间"""
@on_command('addtime') #addtime 123123 300
async def addtime(session: CommandSession):
    qq = session.ctx['user_id']
    #是管理员qq发来的消息
    if qq == 592190443:
        try:
            content = session.get('content', prompt='Please send your total cmd')
            #抽离 qq 时长
            if re.match('(\d)+\s+(\d)+',content):
                customer_qq = re.match('(\d+)\s+(\d+)', content).group(1)
                time = re.match('(\d+)\s+(\d+)',content).group(2)

                customer_obj_list = User.objects.filter(number=customer_qq)
                if customer_obj_list:
                    #用户存在
                    customer_obj = customer_obj_list[0]

                    customer_obj.remain_time += int(time)   #为用户添加时间
                    customer_obj.save()

                    await session.send('添加时长成功,用户剩余时长:{0}'.format(customer_obj.remain_time))
                else:
                    #用户不存在
                    await session.send('当前用户不存在,添加失败')
        except:
            await session.send('操作出现异常')

    else:
        await session.send('对不起,您无权使用此命令。')


@addtime.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if session.current_key:
        print(session.current_arg)
        session.args[session.current_key] = stripped_arg
    elif stripped_arg:
        session.args['content'] = stripped_arg



"""管理员断开某个用户"""
@on_command('cut') #cut 123123
async def cut(session: CommandSession):
    qq = session.ctx['user_id']
    #是管理员qq发来的消息
    if qq == 592190443:
        try:
            content = session.get('content', prompt='Please send your total cmd')
            #抽离 qq
            if re.match('(\d+)',content):
                customer_qq = re.match('(\d+)', content).group(1)
                customer_obj_list = User.objects.filter(number=customer_qq)
                # 用户存在
                if customer_obj_list:
                    customer_obj = customer_obj_list[0]
                    #用户在线
                    if customer_obj.is_online:
                        browser = session.bot.config.BROWSER
                        await session.send('☕...正在断开请稍等...☕')
                        # 利用selenium执行断开操作
                        res = browser.logout(ip=customer_obj.last_login_ip, account=customer_obj.last_login_account)
                        #断开连接成功
                        if res == 'success':
                            customer_obj.last_logout_time = datetime.now()
                            customer_obj.is_online = False
                            customer_obj.save()
                            remain_time = customer_obj.remain_time
                            # 通过最后登录ip 反向查询 connect表，并找到最新一条记录，更新退出时间
                            connect_obj_list = customer_obj.connect_set.filter(ip=customer_obj.last_login_ip).order_by('-login_time')
                            newest_connect_obj = connect_obj_list[0]
                            newest_connect_obj.logout_time = datetime.now()
                            newest_connect_obj.save()
                            # 更新account表
                            account_obj = Account.objects.filter(account=customer_obj.last_login_ip)[0]
                            account_obj.is_using = False
                            account_obj.save()
                            await session.send('执行断开连接完成')
                        else:
                            await session.send('执行断开连接失败')
                    else:
                        #用户不在线
                        await session.send('当前用户不在线')
                else:
                    #用户不存在
                    await session.send('当前用户不存在')
        except:
            await session.send('操作出现异常')

    else:
        await session.send('对不起,您无权使用此命令。')



@cut.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if session.current_key:
        print(session.current_arg)
        session.args[session.current_key] = stripped_arg
    elif stripped_arg:
        session.args['content'] = stripped_arg





"""禁用登录功能"""
@on_command('STOP')
async def stop(session:CommandSession):
    qq = session.ctx['user_id']
    # 是管理员qq发来的消息
    if qq == 592190443:
        try:
            session.bot.config.LOGIN = False
            await session.send('禁止登录功能成功')
        except:
            await session.send('异常,禁止登录功能失败')
    else:
        await session.send('对不起,您无权操作')



"""开启登录功能"""
@on_command('START')
async def start(session:CommandSession):
    qq = session.ctx['user_id']
    # 是管理员qq发来的消息
    if qq == 592190443:
        try:
            session.bot.config.LOGIN = True
            await session.send('开启登录功能成功')
        except:
            await session.send('异常,开启登录功能失败')
    else:
        await session.send('对不起,您无权操作')



"""设置用户的身份 2 会员 3 超级会员 upgrade qq 2"""

@on_command('upgrade')  # upgrage 123123  2
async def upgrade(session: CommandSession):
    qq = session.ctx['user_id']
    # 是管理员qq发来的消息
    if qq == 592190443:
        try:
            content = session.get('content', prompt='Please send your total cmd')
            # 抽离 qq
            if re.match('(\d+)\s+(\d+)', content):
                customer_qq = re.match('(\d+)\s+(\d+)',content).group(1)
                identity = re.match('(\d+)\s+(\d+)', content).group(2)

                customer_obj_list = User.objects.filter(number=customer_qq)
                if customer_obj_list:
                    # 用户存在
                    customer_obj = customer_obj_list[0]
                    if customer_obj.identity == identity:  #已经是这个身份了
                        await session.send('用户已经是{0}'.format(customer_obj.get_identity_display()))
                    else:
                        #设置用户身份
                        customer_obj.identity = identity
                        customer_obj.save()
                        await session.send('用户身份设置成功,当前为{0}'.format(customer_obj.get_identity_display()))
                else:
                    # 用户不存在
                    await session.send('当前用户不存在')
        except:
            await session.send('操作出现异常')

    else:
        await session.send('对不起,您无权使用此命令。')


@upgrade.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if session.current_key:
        print(session.current_arg)
        session.args[session.current_key] = stripped_arg
    elif stripped_arg:
        session.args['content'] = stripped_arg



"""禁用某个用户"""
@on_command('ban') #ban 123123
async def ban(session: CommandSession):
    qq = session.ctx['user_id']
    #是管理员qq发来的消息
    if qq == 592190443:
        try:
            content = session.get('content', prompt='Please send your total cmd')
            #抽离 qq
            if re.match('(\d+)',content):
                customer_qq = re.match('(\d+)', content).group(1)
                customer_obj_list = User.objects.filter(number=customer_qq)

                if customer_obj_list:
                    #用户存在
                    customer_obj = customer_obj_list[0]
                    if customer_obj.ban:
                        await session.send('用户早已禁止登录')
                    else:
                        customer_obj.ban = True
                        customer_obj.save()
                        await session.send('用户已禁止登录')

                else:
                    #用户不存在
                    await session.send('当前用户不存在')
        except:
            await session.send('操作出现异常')

    else:
        await session.send('对不起,您无权使用此命令。')


@ban.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if session.current_key:
        print(session.current_arg)
        session.args[session.current_key] = stripped_arg
    elif stripped_arg:
        session.args['content'] = stripped_arg


"""解禁某个用户"""
@on_command('release')  # ban 123123
async def release(session: CommandSession):
    qq = session.ctx['user_id']
    # 是管理员qq发来的消息
    if qq == 592190443:
        try:
            content = session.get('content', prompt='Please send your total cmd')
            # 抽离 qq
            if re.match('(\d+)', content):
                customer_qq = re.match('(\d+)', content).group(1)
                customer_obj_list = User.objects.filter(number=customer_qq)

                if customer_obj_list:
                    # 用户存在
                    customer_obj = customer_obj_list[0]
                    if customer_obj.ban: #之前是禁止的
                        customer_obj.ban = False
                        customer_obj.save()
                        await session.send('用户已允许登录')
                    else:
                        await session.send('当前用户无需解禁')

                else:
                    # 用户不存在
                    await session.send('当前用户不存在')
        except:
            await session.send('操作出现异常')
    else:
        await session.send('对不起,您无权使用此命令。')


@release.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if session.current_key:
        print(session.current_arg)
        session.args[session.current_key] = stripped_arg
    elif stripped_arg:
        session.args['content'] = stripped_arg


"""管理员查看当前所有在线用户"""
@on_command('listonline')
async def listonline(session:CommandSession):
    qq = session.ctx['user_id']
    # 是管理员qq发来的消息
    if qq == 592190443:
        try:
            online_user_list = User.objects.filter(is_online=True)
            if online_user_list:
                users = ''
                num = len(online_user_list)
                for online_user in online_user_list:
                    online_user_qq = online_user.number
                    users += online_user_qq +'\n'
                await session.send('当前在线用户总数:{0}\n\n{1}'.format(num,users))
            else:
                await session.send('当前没有在线用户')

        except:
            await session.send('操作出现异常')
    else:
        await session.send('对不起,您无权使用此命令。')




"""管理员为帮某个用户执行连接"""
@on_command('connect')
async def connect(session:CommandSession):
    pass



"""查看某个用户的所有信息"""
@on_command('list')
async def list(session:CommandSession):
    pass