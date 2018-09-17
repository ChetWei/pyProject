#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/9/16 23:01'

from http import HTTP

class YuShuBook:
    isbn_url = "http://t.yushu.im/v2/book/isbn{}"
    keyword_url = "http://t.yushu.im/v2/book/search?q={}&count={}&start={}"

    def search_by_isbn(self,isbn):
        url = self.isbn_url.format(isbn)
        json_result = HTTP.get(url)
        #dict
        return json_result

    def search_by_keyword(self,keyword,count=15,start=9):
        url = self.keyword_url.format(keyword,count,start)
        json_result = HTTP.get(url)
        #dict
        return json_result

    pass