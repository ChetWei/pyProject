#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/9/16 23:25'

from flask import jsonify,request

from .blueprint import web


from utils import common    #工具
from yushu_book import YuShuBook
from app.forms.book_form import SearchForm




"""查找视图"""
@web.route('/book/search/')
def search():
    """
    @q :普通关键字或isbn
    @page :页码
    ?q=..&page=   (获取参数)
    :return:
    """
    # Request Response
    # HTTP 的请求信息
    # 查询参数Post参数

    form = SearchForm(request.args) #form验证
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data

        query_key = common.is_key_or_isbn(q)

        yushu = YuShuBook()

        if query_key == "isbn":
            result = yushu.search_by_isbn(query_key)
        else:
            result = yushu.search_by_keyword(query_key)
            # dict 序列化
            # API
        return jsonify(result)
    else:
        return jsonify(form.errors)