#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/9/16 23:25'

from flask import jsonify


from utils import common
from yushu_book import YuShuBook
from fisher import app

@app.route('/book/search/<q>/<page>')
def search(q,page):
    """
    @q :普通关键字或isbn
    @page :页码
    :return:
    """
    query_key = common.is_key_or_isbn(q)

    yushu = YuShuBook()

    if query_key == "isbn":
        result = yushu.search_by_isbn(query_key)
    else:
        result = yushu.search_by_keyword(query_key)
        # dict 序列化
        # API
    return jsonify(result)
