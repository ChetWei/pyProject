from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.core.mail import send_mail


import random
import requests
import re
import base64
from io import  StringIO,BytesIO


from PIL import Image, ImageDraw, ImageFont, ImageFilter

from user.models import UserProfile,EmailVerifyRecord
from teacher import models
from schoolwifi.settings import EMAIL_FROM



"""重写ModelBackend方法，实现 邮箱、用户名 登录"""
class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user

        except Exception as e:
            return None




"""requests 的远程 连接 断开"""
class RequestsConnect():

    def remote_connect(self, connect_ip, connect_account, connect_password):
        '''发送远程post连接请求，返回post响应信息
            connect_ip          需要连接设备连接teacher的ip地址
            connect_account    连接老师账号
            connect_password    连接老师密码(加密密码)
            :return
                login_ok =>  连接成功(可以直接挤下当前在线account)
                网络好像有点延迟  =>  没用的ip，或者账号问题
                请等待5分钟再尝  =>   ip限制 访问频繁
        '''
        post_url = "http://219.229.251.2/include/auth_action.php"
        data = {
            'action': 'login',
            'username': connect_account,  # 连接账号
            'password': connect_password,  # 加密的密码
            'ac_id': '1',
            'save_me': '1',
            'user_ip': connect_ip,  # 设备ip
            'ajax': '1'
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        }
        r1 = requests.post(url=post_url, headers=headers, data=data, timeout=3)
        text = r1.content.decode('utf-8')  # 获取远程连接返回信息

        return text[:8]

    def remote_cut(self, cut_ip, cut_account):
        '''
        :param cut_ip: 需要断开设备的ip
        :param cut_account: 当前设备已经连接的用户名
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
            'username': cut_account,
        }
        r2 = requests.post(url=post_outURL, headers=logout_headers, data=logout_data, timeout=3)
        return r2.content.decode('utf-8')




"""为用户自动分配tea account"""
def get_undistributed_account():
    '''
    根据teacher表的is_consume字段,判断tea account是否被分配
    获取未被分配的tea account
    :return:  obj  ， None
    '''
    try:
        teacher_obj = models.Teacher.objects.filter(is_consume=False)[0]
        return teacher_obj
    except Exception as e:
        print("error with distribute", e)
        return None




"""合法ip验证"""
def check_ip(ipAddr):
    compile_ip = re.compile(
        '^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    if compile_ip.match(ipAddr):
        return True
    else:
        return False



"""合法邮箱校验"""
def check_email(e):
    exp = re.match(r'^[\w]+[\w._]*@\w+\.[a-zA-Z]+$', e)
    return exp


"""邮箱验证"""
class EmailVerify():

    #生成随机字符串
    def random_str(self,random_length=8):
        str = ''
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
        length = len(chars) -1 #实际下标长度

        for i in range(random_length):
            str += chars[random.randint(0,length)] #随机取字符串

        return str

    #发送邮箱，默认类型 注册
    def send_email(self,email,send_type='register'):
        #放松之前先保存到数据库，验证时查询是否存在

        #实例表对象
        email_record = EmailVerifyRecord()
        #生成随机的code放入链接
        code = self.random_str(16)

        email_record.code = code
        email_record.email = email
        email_record.send_type = send_type

        email_record.save()

        #定义邮箱内容
        email_title = ''
        email_boby = ''

        if send_type == 'register':
            email_title = "wifi账号激活链接"
            email_boby = "请点击下面的链接激活您的账号：http://127.0.0.1:8000/active/{0}".format(code)
            # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，发件人邮箱地址，收件人（是一个字符串列表）
            send_status = send_mail(email_title,email_boby,EMAIL_FROM,[email])
            if send_status: #如果发送成功
                return True
            else:
                return False


        elif send_type == 'forget':
            email_title = "wifi账号找回密码链接"
            email_boby = "请点击下面的链接找回您的密码：http://127.0.0.1:8000/active/{0}".format(code)
            # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，发件人邮箱地址，收件人（是一个字符串列表）
            send_status = send_mail(email_title,email_boby,EMAIL_FROM,[email])
            if send_status: #如果发送成功
                return True
            else:
                return False


        elif send_type == 'update_email':
            email_title = "wifi账号邮箱修改链接"
            email_boby = "请点击下面的链接修改您的邮箱：http://127.0.0.1:8000/active/{0}".format(code)
            # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，发件人邮箱地址，收件人（是一个字符串列表）
            send_status = send_mail(email_title,email_boby,EMAIL_FROM,[email])
            if send_status: #如果发送成功
                return True
            else:
                return False






"""生成图像验证码"""
_letter_cases = "abcdefghjkmnpqrstuvwxy"  # 小写字母
_upper_cases = "ABCDEFGHJKLMNPQRSTUVWXY"  # 大写字母
_numbers = "1234567890"  # 数字
init_chars = ''.join((_letter_cases, _upper_cases, _numbers))  # 生成允许的字符集合
#default_font = DevConfig.FONTPATH  # 验证码字体，在配置文件中定义
font_file = r'K:\pyProject\schoolwifi\apps\user\ACKNO.TTF'

# 生成验证码接口120 30
def generate_verify_image(size=(140, 40),
                          chars=init_chars,
                          img_type="PNG",
                          mode="RGB",
                          bg_color=(255, 255, 255),
                          fg_color=(0, 0, 255),
                          font_size=18,
                          font_file=font_file,
                          length=4,
                          draw_lines=True,
                          n_line=(1, 2),
                          draw_points=True,
                          point_chance=2,
                          save_img=True):
    width, height = size  # 宽， 高
    img = Image.new(mode, size, bg_color)  # 创建图形
    draw = ImageDraw.Draw(img)  # 创建画笔

    def get_chars():
        """生成给定长度的字符串，返回列表格式"""

        return random.sample(chars, length)

    def create_lines():
        """绘制干扰线"""

        line_num = random.randint(*n_line)  # 干扰线条数

        for i in range(line_num):
            # 起始点
            begin = (random.randint(0, size[0]), random.randint(0, size[1]))
            # 结束点
            end = (random.randint(0, size[0]), random.randint(0, size[1]))
            draw.line([begin, end], fill=(0, 0, 0))

    def create_points():
        """绘制干扰点"""

        chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]

        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    def create_strs():
        """绘制验证码字符"""
        c_chars = get_chars()
        strs = ' %s ' % ' '.join(c_chars)  # 每个字符前后以空格隔开

        font = ImageFont.truetype(font_file, font_size)
        font_width, font_height = font.getsize(strs)

        draw.text(((width - font_width) / 3, (height - font_height) / 3),
                  strs, font=font, fill=fg_color)

        return ''.join(c_chars)

    if draw_lines:
        create_lines()
    if draw_points:
        create_points()
    text_code = create_strs()

    # 图形扭曲参数
    params = [1 - float(random.randint(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500,
              0.001,
              float(random.randint(1, 2)) / 500
              ]
    img = img.transform(size, Image.PERSPECTIVE, params)  # 创建扭曲

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜

    mstream = BytesIO()

    img.save(mstream, img_type)

    return mstream, mstream.getvalue(), text_code



