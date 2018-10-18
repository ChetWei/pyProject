#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/10/18 11:51'

import requests

# 连接界面
class Connect():

    def remote_connect(self,connect_ip, connect_username, connect_password):
        '''发送远程post连接请求，返回post响应信息
            connect_ip          需要连接设备连接teacher的ip地址
            connect_username    连接老师账号
            connect_password    连接老师密码(加密密码)

            返回参数：

        '''
        post_url = "http://219.229.251.2/include/auth_action.php"
        data = {
            'action': 'login',
            'username': connect_username,  # 连接账号
            'password': connect_password,  # 加密的密码
            'ac_id': '1',
            'save_me': '1',
            'user_ip': connect_ip,  # 设备ip
            'ajax': '1'
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        }

        r1 = requests.post(url=post_url, headers=headers, data=data)
        text = r1.content.decode('utf-8')  # 获取远程连接返回信息
        return text

    def remote_cut(self,cut_ip,cut_username):
        '''
        :param cut_ip: 需要断开设备的ip
        :param cut_username: 当前设备已经连接的用户名
        :return: 没有
        '''
        post_outURL = 'http://219.229.251.2/srun_portal_pc_succeed.php'
        logout_headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'http://219.229.251.2',
            'Referer': 'http://219.229.251.2/srun_portal_pc_succeed.php',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            'X-DevTools-Emulate-Network-Conditions-Client-Id': '3FCFC7872E45E16E216DADA6125B0705',
        }
        logout_data = {
            'action': 'auto_logout',
            'info': '',
            'user_ip': cut_ip,
            'username': cut_username,
        }
        r2 = requests.post(url=post_outURL, headers=logout_headers, data=logout_data)
        return r2.content.decode('utf-8')





