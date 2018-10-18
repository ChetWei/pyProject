#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/9/16 23:01'

from httper import HTTP
from flask import current_app

class YuShuBook:
    per_page = 15
    isbn_url = "http://t.yushu.im/v2/book/isbn{}"
    keyword_url = "http://t.yushu.im/v2/book/search?q={}&count={}&start={}"

    @classmethod
    def search_by_isbn(cls,isbn):
        url = cls.isbn_url.format(isbn)
        json_result = HTTP.get(url)
        #dict
        return json_result


    @classmethod
    def search_by_keyword(cls,keyword,page=1):
        url = cls.keyword_url.format(keyword,cls.per_page,(page-1)*cls.per_page)
        json_result = HTTP.get(url)
        #dict
        return json_result

    pass