#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/10/9 21:44'
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class SeleniumConnect():
    url = "http://127.0.0.1:8000/get_loginUI/"

    def setUp(self):
        self.browser = webdriver.Firefox()

    def login(self,ip,account,password):
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

        return res



    def logout(self,ip,account):
        self.browser.get(url=self.url)
        ip_input_ele = self.browser.find_element_by_id('ip')
        account_input_ele = self.browser.find_element_by_id('username')
        logout_ele = self.browser.find_element_by_id('logout-dm')
        ip_input_ele.send_keys(ip)
        account_input_ele.send_keys(account)
        logout_ele.click()
        sleep(1)
        res = self.browser.find_element_by_id('info').text

        return res


    def tearDown(self):
        self.browser.close()


if __name__ == "__main__":

    conn = SeleniumConnect()
    conn.setUp()

    login_info = conn.login(ip='10.110.155.224',account='000183',password='610615')

    #logout_info = conn.logout(ip='10.110.155.224',account='000182')

    sleep(2)
    login_info2 = conn.login(ip='10.110.155.224',account='000110',password='161412')

    print(login_info,login_info2)



