#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/10/10 0:02'
from os import path
import none
from robot import config

from selenium_spider.selenium_connect import SeleniumConnect


if __name__ == '__main__':

    browser = SeleniumConnect()
    browser.setUp()
    config.BROWSER = browser

    none.init(config)  #使用默认配置初始化 NoneBot 包
    none.load_plugins(path.join(path.dirname(__file__), 'awesome', 'plugins'),'awesome.plugins') #加载 NoneBot 的插件
    none.run() #在地址 127.0.0.1:8080 运行 NoneBot

