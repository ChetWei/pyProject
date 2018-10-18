#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/10/14 18:24'

from none import on_command,CommandSession
from none import on_natural_language,NLPSession,NLPResult

from .data_source import *

@on_command('news', aliases=('新闻', '今日新闻', '快讯','今日快讯'))
async def weather(session: CommandSession):
    news_info = get_today_news()
    await session.send('今日快讯\n\n'+news_info)