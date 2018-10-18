#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/10/15 21:08'

from none import on_notice,NoticeSession,RequestSession,on_request


@on_request('friend')
async def _(session:RequestSession):
    #申请 并且备注为qq号
    user_id = session.ctx.get('user_id')
    await session.approve(remark=user_id)




@on_notice('group_increase')
async def _(session:NoticeSession):
    #新人加群 欢迎消息
    await session.send('欢迎新人入群[CQ:face,id=99][CQ:face,id=99][CQ:face,id=99]')






