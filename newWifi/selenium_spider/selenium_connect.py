#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/10/11 23:55'

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('window-size=200x300') #指定浏览器分辨率
chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
#chrome_options.add_argument('--headless') #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
#chrome_options.binary_location = r'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'



class SeleniumConnect():
    url = "http://127.0.0.1:8000/get_loginUI/"

    def setUp(self):
        self.browser = webdriver.Chrome(chrome_options=chrome_options)

    def login(self,ip,account,password):
        try:
            self.browser.get(url=self.url)
            #获取操作元素
            ip_input_ele = self.browser.find_element_by_id('ip')
            account_input_ele = self.browser.find_element_by_id('username')
            pwd_input_ele = self.browser.find_element_by_id('password')
            login_ele = self.browser.find_element_by_id('login')
            ip_input_ele.send_keys(ip)
            account_input_ele.send_keys(account)
            pwd_input_ele.send_keys(password)
            #登录
            login_ele.click()
            sleep(1)
            res = self.browser.find_element_by_id('info').text
            return res  #success fail
        except:
            return 'error'


    def logout(self,ip,account):
        try:
            self.browser.get(url=self.url)
            ip_input_ele = self.browser.find_element_by_id('ip')
            account_input_ele = self.browser.find_element_by_id('username')
            logout_ele = self.browser.find_element_by_id('logout-dm')
            ip_input_ele.send_keys(ip)
            account_input_ele.send_keys(account)
            logout_ele.click()
            sleep(1)
            res = self.browser.find_element_by_id('info').text
            return res  #success fail
        except:
            return 'error'

    def tearDown(self):
        self.browser.close()
