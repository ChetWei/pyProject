#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/10/5 0:21'

import requests
from lxml import etree




def get_data_by_day(day,type="draw-speed10-",abs_dir_path="K:\\pyProject\\21天爬虫\happy\\real_data\\"):
    """按天，类型获取当天的开奖记录，并保持到本地文件"""
    url = "https://www.06kj33.com/{0}{1}.html".format(type,day)
    res = requests.get(url=url)
    html = res.content.decode("UTF-8")
    selector = etree.HTML(html)
    tr_list = selector.xpath("//tr[@class='tr']") #每一次开奖的数据，列表

    f = open(abs_dir_path+type+day+".txt",'w',encoding='UTF-8')
    asc_tr_list = reversed(tr_list)
    for tr in asc_tr_list:   #遍历每一次的数据
        try:
            term_number = tr.xpath("td[@class='time']/span/text()")[0] #期号
            number_1 = tr.xpath("td[2]/div[1]/span[1]/text()")[0]   #冠军数字
            number_2 = tr.xpath("td[2]/div[1]/span[2]/text()")[0]    #亚军数字
            number_3 = tr.xpath("td[2]/div[1]/span[3]/text()")[0]
            number_4 = tr.xpath("td[2]/div[1]/span[4]/text()")[0]
            number_5 = tr.xpath("td[2]/div[1]/span[5]/text()")[0]
            number_6 = tr.xpath("td[2]/div[1]/span[6]/text()")[0]
            number_7 = tr.xpath("td[2]/div[1]/span[7]/text()")[0]
            number_8 = tr.xpath("td[2]/div[1]/span[8]/text()")[0]
            number_9 = tr.xpath("td[2]/div[1]/span[9]/text()")[0]
            number_10 = tr.xpath("td[2]/div[1]/span[10]/text()")[0]

            numbers = term_number+" "+number_1+" "+number_2+" "+number_3+" "+number_4+" "+number_5+" "+number_6+" "+number_7+" "+number_8+" "+number_9+" "+number_10+" "
            f.write(numbers+"\n")
        except :
            print("error")

    f.close()






type_tupe = ("draw-speed10-","draw-jsft-")
type = type_tupe[0]


if __name__ == "__main__":
    start = 20180900
    for i in range(30):
        start += 1
        str_start = str(start)
        get_data_by_day(day=str_start,type=type,abs_dir_path="K:\\pyProject\\21天爬虫\\happy\\real_data\\month09\\")