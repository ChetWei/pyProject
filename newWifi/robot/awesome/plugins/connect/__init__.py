#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/10/10 18:23'
import re
from none import on_command,CommandSession
from none import on_natural_language,NLPSession,NLPResult
from .data_source import *

import os
os.environ.setdefault('DJANGO_SETTING_MODULE', 'newWifi.settings')
import django
django.setup()

import random
from datetime import datetime

import none
from wifi.models import Account,User,Connect,AuthorizationCode

from selenium_spider.tulin_robot import ask_tulin


"""登录命令"""

@on_command('login', aliases=('登录', '登陆', '连接'))
async def login(session: CommandSession):
    if session.bot.config.LOGIN:
        # 从 Session 对象中ip地址（ip），如果当前不存在，则询问用户
        ip = session.get('ip', prompt='你的电脑IP地址是什么呢?')
        is_ip = await valiable_ip(ip)
        if(not is_ip):
            #用户输入错误的ip,提示重头输入命令
            await session.send('电脑IP地址不合法,请重新输入登录命令')
        else:
            # 输入了正确的ip,并且允许登录功能,进行连接操作

            qq = session.ctx['user_id']
            user_obj_list = User.objects.filter(number=qq)

            # 用户不存在，创建用户记录
            if not user_obj_list:
                user_obj = User(number=qq, remain_time=60, free_chances=False)
                user_obj.save()

                account_obj_list = Account.objects.filter(is_using=False)  # 可用的账号对象列表
                available_accounts = len(account_obj_list)  # 可用数量
                account_obj = account_obj_list[random.randint(0, available_accounts - 1)]  # 随机抽取一个可用账号（）

                #如果当前没有可用账号
                if not account_obj:
                    await session.send('☕当前用户过多,稍后尝试☕')
                else:
                    account = account_obj.account
                    password = account_obj.password

                    brower = session.bot.config.BROWSER
                    await session.send('☕...正在连接请稍等...☕')
                    # 利用selenium执行连接操作
                    res = brower.login(ip=ip, account=account, password=password)
                    if res == 'success':  # 登录成功
                        # 更新数据库 user,connect,account表
                        user_obj.is_online = True
                        user_obj.login_times = 1
                        user_obj.last_login_ip = ip
                        user_obj.last_login_time = datetime.now()
                        user_obj.last_login_account = account
                        user_obj.save()

                        # connect表关联表对象 新记录
                        connect_obj = Connect(qq_number=user_obj, ip=ip, login_time=datetime.now(), tea_account=account_obj)
                        connect_obj.save()

                        account_obj.is_using = True
                        account_obj.save()

                        # 返回消息
                        await session.send('✨新用户✨\n[CQ:face,id=144]连接成功[CQ:face,id=144]\n🕕赠送免费时长60分钟🕣')
                    else:  # 登录失败
                        # 不更新user表默认字段，和其他表
                        await session.send('[CQ:face,id=64]连接失败,请重试[CQ:face,id=64]\n提示:请检查ip')


            # 用户已经存在，查看时长，因为首次注册用户默认时长为60
            else:
                user_obj = user_obj_list[0]
                remain_time = user_obj.remain_time

                # 时长小于等于 0,并且不是超级用户，提醒用户，无法连接
                if remain_time <= 0 and user_obj.identity != 0:

                    await session.send(
                        '✨{0}✨\n[CQ:face,id=64]剩余0分钟,请充值[CQ:face,id=64]'.format(user_obj.get_identity_display()))

                #被禁止登录
                elif user_obj.ban:
                    await session.send('对不起,当前用户已被禁止登录')

                # 时长不为0,没有被禁用 或者超级用户 进行连接操作
                else:
                    account_obj_list = Account.objects.filter(is_using=False)  # 可用的账号对象列表
                    available_accounts = len(account_obj_list)  # 可用数量
                    account_obj = account_obj_list[random.randint(0, available_accounts - 1)]  # 随机抽取一个可用账号

                    # 如果当前没有可用账号
                    if not account_obj:
                        await session.send('☕当前用户过多,稍后尝试☕')
                    else:
                        #有可用账号，进行连接操作
                        account = account_obj.account
                        password = account_obj.password

                        browser = session.bot.config.BROWSER
                        await session.send('☕...正在连接请稍等...☕')
                        # 利用selenium执行连接操作
                        res = browser.login(ip=ip, account=account, password=password)
                        if res == 'success':  # 登录成功
                            # 更新数据库 user,connect,account表
                            user_obj.is_online = True
                            user_obj.login_times += 1
                            user_obj.last_login_ip = ip
                            user_obj.last_login_time = datetime.now()
                            user_obj.last_login_account = account
                            user_obj.save()

                            # connect表关联表对象 新记录
                            connect_obj = Connect(qq_number=user_obj, ip=ip, login_time=datetime.now(),
                                                  tea_account=account_obj)
                            connect_obj.save()

                            account_obj.is_using = True
                            account_obj.save()
                            # 返回消息
                            await session.send('✨{0}✨\n[CQ:face,id=144]网络连接成功[CQ:face,id=144]\n🕕剩余{1}分钟🕣'.format(
                                user_obj.get_identity_display(), remain_time))

                        else:  # 登录失败
                            # 不更新user表默认字段，和其他表
                            await session.send(
                                '✨{0}✨\n[CQ:face,id=64]连接失败,请重试[CQ:face,id=64]\n提示:提示:请检查ip'.format(user_obj.get_identity_display()))
    else:
        await session.send('对不起,机器人暂时关闭登录功能。\n请联系管理员')



@login.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if session.current_key:
        print(session.current_arg)
        session.args[session.current_key] = stripped_arg
    elif stripped_arg:
        session.args['ip'] = stripped_arg




'''断开连接命令处理 断开 ip'''
@on_command('logout', aliases=('断开', '断开连接', '退出'))
async def logout(session: CommandSession):

    #为了避免断开失败，可以允许提交ip
    qq = session.ctx['user_id']
    message = session.ctx['message']   #'message': [{'type': 'text', 'data': {'text': '断开 10.110.280.36'}}]
    text = message[0]['data']['text']
    ip = ''
    if re.match(r'(\D+)\s+(\d+.\d+.\d+.\d+)', text):   #判断用户是否发送了ip
        ip = re.match(r'(\D+)\s+(\d+.\d+.\d+.\d+)', text).group(2)
    print(ip)

    user_obj_list = User.objects.filter(number=qq)

    # 用户还不存在
    if not user_obj_list:
        await  session.send('✨新用户✨\n您还没有连接')

    #用户存在
    else:
        user_obj = user_obj_list[0]
        # 如果不在线
        if not user_obj.is_online:
            await session.send('✨{0}✨\n☕您当前未连接,断开无效☕'.format(user_obj.get_identity_display()))

        # 在线，进行断开连接操作,user表中获取上次连接的信息，或者判断用户是否提交了ip
        else:
            last_login_account = user_obj.last_login_account
            last_login_ip = user_obj.last_login_ip
            browser = session.bot.config.BROWSER

            res = ''
            # 用户提交了ip,通过用户当前ip和最后登录账号断开连接
            if ip:
                print('提交了ip')
                is_ip = await valiable_ip(ip)
                if (not is_ip):
                    await session.send('☕请发送正确的IP地址☕')
                # 合格的ip,进行断开连接操作
                else:
                    await session.send('☕...正在断开连接请稍等...☕')
                    res = browser.logout(ip=ip, account=last_login_account)
            #没有提交ip
            else:
                print('没有提交ip')
                await session.send('☕...正在断开连接请稍等...☕')
                res = browser.logout(ip=last_login_ip, account=last_login_account)


            #成功断开连接
            if res == 'success':
                user_obj.last_logout_time = datetime.now()
                user_obj.is_online = False
                user_obj.save()
                remain_time = user_obj.remain_time
                # 通过最后登录ip 反向查询 connect表，并找到最新一条记录，更新退出时间
                connect_obj_list = user_obj.connect_set.filter(ip=last_login_ip).order_by('-login_time')
                newest_connect_obj = connect_obj_list[0]
                newest_connect_obj.logout_time = datetime.now()
                newest_connect_obj.save()
                # 更新account表
                account_obj = Account.objects.filter(account=last_login_account)[0]
                account_obj.is_using = False
                account_obj.save()
                await session.send('✨{0}✨\n[CQ:face,id=144]您已经成功断开连接[CQ:face,id=144]\n🕣您的剩余时长{1}分钟🕣'.format(
                    user_obj.get_identity_display(), remain_time))

            #没有发送ip,并且断开连接失败
            elif not ip and res == 'fail':
                await session.send('✨{0}✨\n[CQ:face,id=146]断开失败[CQ:face,id=146]\n如果IP变动请发送👇\n断开 当前的ip'.format(
                    user_obj.get_identity_display()))

            #发送了ip,还是断开连接失败
            elif res == 'fail':
                await session.send('✨{0}✨\n[CQ:face,id=146]断开失败[CQ:face,id=146]\n☕此IP的电脑似乎没有网络连接☕'.format(user_obj.get_identity_display()))

            else:
                await session.send('✨{0}✨\n[CQ:face,id=146]断开失败[CQ:face,id=146]\n☕请您重试☕'.format(
                    user_obj.get_identity_display()))



@logout.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if session.current_key:
        print(session.current_arg)
        session.args[session.current_key] = stripped_arg
    elif stripped_arg:
        session.args['ip'] = stripped_arg




'''查询剩余时长命令处理'''
@on_command('search',aliases=('查询','查询时长','查询剩余时长','剩余时间','剩余时长'))
async def search(session:CommandSession):
    qq = session.ctx['user_id']
    user_obj_list = User.objects.filter(number=qq)
    #用户是否存在
    if not user_obj_list:
        await session.send('✨新用户✨\n您的剩余免费时长60分钟')
    else:
        user_obj = user_obj_list[0]
        remain_time = user_obj.remain_time
        await session.send('✨{0}✨\n🕣剩余{1}分钟🕣'.format(user_obj.get_identity_display(),remain_time))




'''充值 命令提示'''
@on_command('recharge',aliases=('充值','怎么充值','没时间了','续费'))
async def recharge(session:CommandSession):
    await session.send('👇套餐业务👇\n'
                       '1元\t\t180分钟\n10元\t3000分钟(会员)\n30元\t12000分钟(超级会员)\n会员时长为0可延长断网时间\n\n'
                       '👇充值方式👇\n'
                       'Ⅰ 添加我为好友，直接转账(不支持红包)，自动购买。\n'
                       'Ⅱ 联系管理员充值。')



'''帮助 提示'''
@on_command('help',aliases=('帮助','你是干嘛的','你有什么功能','功能','提示'))
async def help(session:CommandSession):
    await session.send('您好,我是机器猫\n有什么可以帮您💤\n\n群内请@我发送\n私聊直接发送\n\n-------命令列表-------\n\n'
                       '"登陆 电脑ip" 👉登陆校园网\n"断开" 👉断开校园网\n"查询" 👉查看剩余时长\n"充值" 👉查看充值帮助')





# keywords 表示需要响应的关键词，类型为任意可迭代对象，元素类型为 str
# 如果不传入 keywords，则响应所有没有被当作命令处理的消息
#返回处理结果 3个参数 置信度，命令名，命令会话
@on_natural_language()
async def _(session: NLPSession):
    qq = session.ctx['user_id']
    print(qq)
    content = session.msg_text
    content = content.strip()
    print(content)
    #判断内容 是否与"发送ip"的命令 相符合 "登录 ip  断开 ip"
    login = re.match("登陆\s*(.*)",content)
    logout = re.match("断开连接",content)
    transfer = re.match('^\[转账\]\s(\d+.?\d+)+元已转账成功，请使用手机QQ查看。', content)
    help = re.match('帮助',content)


    #转账的信息
    if transfer:
        money = float(transfer.group(1))
        bot = none.get_bot()
        user_obj_list = User.objects.filter(number=qq)
        if not user_obj_list:
            #用户没有注册,就转账,先注册用户
            user_obj = User(number=qq, remain_time=0, free_chances=False)
            user_obj.save()

            #根据金额添加时长
            time = buy_time(money)
            user_obj.remain_time += time #数据库添加时间
            user_obj.accumulated_recharge += money  #更新累计充值
            user_obj.newest_recharge = money #最新充值
            if user_obj.accumulated_recharge > 10: #升级会员
                user_obj.identity = 2
            elif user_obj.accumulated_recharge > 30: #升级创超级会员
                user_obj.identity = 3

            user_obj.save()
            await session.send('💰充值{0}元💰\n🕕获得{1}分钟🕕\n🕣剩余{2}分钟🕣\n✨当前身份:{3}✨'.format(money, time, user_obj.remain_time,user_obj.get_identity_display()))
            await bot.send_private_msg(user_id=592190443, message='用户{0}充值{1}元'.format(user_obj.number,money))
        else:
            #已注册用户
            user_obj = user_obj_list[0]
            time = buy_time(money)
            user_obj.remain_time += time #数据库添加时间
            user_obj.accumulated_recharge += money  # 更新累计充值
            user_obj.newest_recharge = money  # 最新充值
            if user_obj.accumulated_recharge > 10 and user_obj.accumulated_recharge < 30 and user_obj.identity != 0:  # 升级会员
                user_obj.identity = 2
            elif user_obj.accumulated_recharge > 30 and user_obj.identity != 0:  # 升级超级会员
                user_obj.identity = 3

            user_obj.save()
            await session.send('💰充值{0}元💰\n🕕获得{1}分钟🕕\n🕣剩余{2}分钟🕣\n✨当前身份:{3}✨'.format(money,time,user_obj.remain_time,user_obj.get_identity_display()))
            await bot.send_private_msg(user_id=592190443, message='用户{0}充值{1}元'.format(user_obj.number, money))



    #其他的消息 交给图灵机器人
    else:
        response = ask_tulin(content)
        if response == 40004: #次数不够了
            response = ask_tulin(content,key='268bb4dc88d14ffe9232661aca8dcc12')

        await session.send(response)


