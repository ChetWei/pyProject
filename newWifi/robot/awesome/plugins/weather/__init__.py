#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/10/10 16:32'

from none import on_command,CommandSession
from none import on_natural_language,NLPSession,NLPResult


from .data_source import get_nanchang_weather



"""
on_command 装饰器将函数声明为一个命令处理器
这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」
"""

@on_command('weather', aliases=('天气', '天气预报', '查天气','今天天气'))
async def weather(session: CommandSession):
    weather_info = get_nanchang_weather()
    await session.send(weather_info)



