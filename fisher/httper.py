#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/9/16 21:55'

import requests



class HTTP():
    """
    """
    @staticmethod
    def get(url,return_json=True):
        res = requests.get(url=url)
        if res.status_code != 200:
            return {} if return_json else ''
        return res.json() if return_json else res.text


