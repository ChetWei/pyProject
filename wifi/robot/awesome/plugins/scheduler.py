#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/10/12 16:15'


import os
os.environ.setdefault('DJANGO_SETTING_MODULE', 'newWifi.settings')
import django
django.setup()

from wifi.models import Account,User,Connect,AuthorizationCode
import random
from datetime import datetime
import none
import pytz
from aiocqhttp.exceptions import Error as CQHttpError
from none import on_natural_language,NLPSession,NLPResult


from ..plugins.baby.say import today_weather_info,care
from ..plugins.news.data_source import get_today_news


from selenium_spider.selenium_connect import SeleniumConnect

browser = SeleniumConnect()
browser.setUp()   #开启一个为到期用户关闭的浏览器






@none.scheduler.scheduled_job('interval', minutes=1)
async def _():
    bot = none.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    print('\033[0;32;m每分钟任务报时\033[0m',now)
    try:

        if now.hour == 0 and now.minute == 0:  #零点任务
            for i in range(3):
                await bot.send_private_msg(user_id=2548810667,message='💤叮当猫温馨提示💤\n\n[CQ:face,id=63]亲爱的宝宝[CQ:face,id=63]\n[CQ:face,id=75]夜深了,该睡觉了[CQ:face,id=75]\n[CQ:face,id=66]注意休息哦[CQ:face,id=66]')


        if now.hour == 7 and now.minute == 0: #早上七点任务

            weather_dict = today_weather_info()   #{'wea':wea,'low_tem':low_tem,'win':win}
            wea = weather_dict['wea']
            low_tem = weather_dict['low_tem'].strip()
            win = weather_dict['win']
            rain_info,clothes_info = care(wea=wea,lowtem=low_tem)

            news_info = get_today_news()


            for i in range(3):
                await bot.send_private_msg(user_id=2548810667,message='[CQ:face,id=125]早安,宝贝[CQ:face,id=125]\n\n💤叮当猫天气预报💤\n{0}\n最低气温{1}\n{2}\n{3}\n{4}'.format(wea,low_tem,win,rain_info,clothes_info))

            #发生每天群提醒
            #天气
            await bot.send_group_msg(group_id=828892924, message='今日天气\n\n天气\t{0}\n最低气温\t{1}\n风向\t{2}'.format(wea,low_tem,win))
            #今日新闻
            await bot.send_group_msg(group_id=828892924, message='今日快讯\n\n'+ news_info)



            #每一分钟扫描数据库,在线用户减时间,如果用户时长为0则断开连接



        online_user_list = User.objects.filter(is_online=True)

        for online_user in online_user_list:
            remain_time = online_user.remain_time  #剩余时间
            user_qq = online_user.number
            user_identity = online_user.get_identity_display()
            last_login_ip = online_user.last_login_ip
            last_login_account = online_user.last_login_account

            if remain_time == 10: #10分钟预警
                await bot.send_group_msg(group_id=828892924, message='[CQ:at,qq={1}] \n✨{0}✨\n[CQ:face,id=54]您的时长不足10分钟[CQ:face,id=54]'.format(user_identity,user_qq))
                await bot.send_private_msg(user_id=user_qq,message='✨{0}✨\n[CQ:face,id=54]您的时长不足10分钟[CQ:face,id=54]'.format(user_identity))

            # 剩余时间为0 普通用户断开连接
            elif remain_time == 0 and online_user.identity == 1 :

                browser.logout(ip=last_login_ip,account=last_login_account)
                online_user.is_online = False
                online_user.save()

                await bot.send_group_msg(group_id=828892924, message='[CQ:at,qq={1}] \n✨{0}✨\n[CQ:face,id=54]时长不足,已断开连接[CQ:face,id=54]'.format(user_identity,user_qq))
                await bot.send_private_msg(user_id=user_qq, message='✨{0}✨\n[CQ:face,id=54]时长不足,已断开连接[CQ:face,id=54]'.format(user_identity))


            #剩余时间为0的会员，延迟断开预警
            elif remain_time == 0 and online_user.identity != 1 :
                await bot.send_group_msg(group_id=828892924,
                                         message='[CQ:at,qq={1}] \n✨{0}✨\n[CQ:face,id=54]时长不足,为您延迟60分钟断开连接[CQ:face,id=54]'.format(
                                             user_identity, user_qq))
                await bot.send_private_msg(user_id=user_qq,
                                           message='✨{0}✨\n[CQ:face,id=54]时长不足,为您延迟60分钟断开连接[CQ:face,id=54]'.format(
                                               user_identity))

            #会员延迟 到期，断开连接
            elif remain_time == -60 and (online_user.identity ==2 or online_user.identity ==3 or online_user.identity ==0 ) :
                browser.logout(ip=last_login_ip, account=last_login_account)
                online_user.is_online = False
                online_user.save()

                await bot.send_group_msg(group_id=828892924,
                                         message='[CQ:at,qq={1}] \n✨{0}✨\n[CQ:face,id=54]时长延迟已到,已断开连接[CQ:face,id=54]'.format(
                                             user_identity, user_qq))
                await bot.send_private_msg(user_id=user_qq,
                                           message='✨{0}✨\n[CQ:face,id=54]时长延迟已到,已断开连接[CQ:face,id=54]'.format(
                                               user_identity))


            #只要在线,递减
            if online_user.is_online:
                online_user.remain_time -= 1 #减一分钟
                online_user.save()

    except:
        print('\033[0;31;m每分钟任务报时{0},发生异常'.format(now))

