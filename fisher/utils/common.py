#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/9/16 21:21'


def is_key_or_isbn(word):
    """
    isbn   isbn13  0-9的13个数字组成
    isbn10 10个0到9数字和一些符号'-'组成
    :param word:
    :return:
    """
    isbn_or_key = 'key'
    if len(word) == 13 and word.isdigit():
        isbn_or_key = 'isbn'

    short_word = word.replace('-', '')
    if '-' in short_word and short_word.isdigit() and len(short_word) == 10:
        isbn_or_key = 'isbn'

    return isbn_or_key