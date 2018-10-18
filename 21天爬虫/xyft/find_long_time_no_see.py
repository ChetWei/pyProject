#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/10/6 21:52'

import requests
from lxml import etree

def get_current_day_data():

    """获取某日的数据"""

    url = "https://www.1395p.com/xyft/kaijiang"
    res = requests.get(url=url)
    html = res.text
    selector = etree.HTML(html)
    tr_list = selector.xpath('//*[@id="history"]/tbody/tr')
    f = open("K:\\pyProject\\21天爬虫\\xyft\\data\\current_day_data.txt", "w+", encoding="UTF-8")
    for tr in tr_list:
        term_number = tr.xpath('td[1]/i[1]/text()')[0]
        number_1 = tr.xpath('td[2]/div[@class="number_pk10"]/span[1]/text()')[0]
        number_2 = tr.xpath('td[2]/div[@class="number_pk10"]/span[2]/text()')[0]
        number_3 = tr.xpath('td[2]/div[@class="number_pk10"]/span[3]/text()')[0]
        number_4 = tr.xpath('td[2]/div[@class="number_pk10"]/span[4]/text()')[0]
        number_5 = tr.xpath('td[2]/div[@class="number_pk10"]/span[5]/text()')[0]
        number_6 = tr.xpath('td[2]/div[@class="number_pk10"]/span[6]/text()')[0]
        number_7 = tr.xpath('td[2]/div[@class="number_pk10"]/span[7]/text()')[0]
        number_8 = tr.xpath('td[2]/div[@class="number_pk10"]/span[8]/text()')[0]
        number_9 = tr.xpath('td[2]/div[@class="number_pk10"]/span[9]/text()')[0]
        number_10 = tr.xpath('td[2]/div[@class="number_pk10"]/span[10]/text()')[0]


        line_data = term_number + " " + number_1 + " " + number_2 + " " + number_3 + " " + number_4 + " " + number_5 + " " + number_6 + " " + number_7 + " " + number_8 + " " + number_9 + " " + number_10 + "  \n"
        f.write(line_data)





def scan_number(test_position=1):

    """扫描某一个位置，没有出现的号码前五排行榜"""
    f = open("K:\\pyProject\\21天爬虫\\xyft\\data\\current_day_data.txt","r",encoding="UTF-8")
    #每个数字连续没有出现的次数的程度
    number1 = 0
    number2 = 0
    number3 = 0
    number4 = 0
    number5 = 0
    number6 = 0
    number7 = 0
    number8 = 0
    number9 = 0
    number10 = 0



    lines_list = f.readlines()
    for line in reversed(lines_list):   #以时间顺序排序
        number_list = line.split(' ')

        position = number_list[test_position]

        if position == '1':
            number1 = 0
            number2 += 1
            number3 += 1
            number4 += 1
            number5 += 1
            number6 += 1
            number7 += 1
            number8 += 1
            number9 += 1
            number10 += 1
        elif position == '2':
            number2 = 0
            number1 += 1
            number3 += 1
            number4 += 1
            number5 += 1
            number6 += 1
            number7 += 1
            number8 += 1
            number9 += 1
            number10 += 1

        elif position == '3':
            number3 = 0
            number1 += 1
            number2 += 1
            number4 += 1
            number5 += 1
            number6 += 1
            number7 += 1
            number8 += 1
            number9 += 1
            number10 += 1

        elif position == '4':
            number4 = 0
            number1 += 1
            number2 += 1
            number3 += 1
            number5 += 1
            number6 += 1
            number7 += 1
            number8 += 1
            number9 += 1
            number10 += 1

        elif position == '5':
            number5 = 0
            number1 += 1
            number2 += 1
            number3 += 1
            number4 += 1
            number6 += 1
            number7 += 1
            number8 += 1
            number9 += 1
            number10 += 1

        elif position == '6':
            number6 = 0
            number1 += 1
            number2 += 1
            number3 += 1
            number4 += 1
            number5 += 1
            number7 += 1
            number8 += 1
            number9 += 1
            number10 += 1

        elif position == '7':
            number7 = 0
            number1 += 1
            number2 += 1
            number3 += 1
            number4 += 1
            number5 += 1
            number6 += 1
            number8 += 1
            number9 += 1
            number10 += 1

        elif position == '8':
            number8 = 0
            number1 += 1
            number2 += 1
            number3 += 1
            number4 += 1
            number5 += 1
            number6 += 1
            number7 += 1
            number9 += 1
            number10 += 1

        elif position == '9':
            number9 = 0
            number1 += 1
            number2 += 1
            number3 += 1
            number4 += 1
            number5 += 1
            number6 += 1
            number7 += 1
            number8 += 1
            number10 += 1

        elif position == '10':
            number10 = 0
            number1 += 1
            number2 += 1
            number3 += 1
            number4 += 1
            number5 += 1
            number6 += 1
            number7 += 1
            number8 += 1
            number9 += 1

    f.close()
    rank_list = [number1,number2,number3,number4,number5,number6,number7,number8,number9,number10]
    sorted_rank_list = sorted(rank_list)
    max = sorted_rank_list[-1]
    p = rank_list.index(max)

    print("{0}位置: 1号{1}期未出 2号{2}期未出 3号{3}期未出 4号{4}期未出 5号{5}期未出 6号{6}期未出 7号{7}期未出 8号{8}期未出 9号{9}期未出 10号{10}期未出 第{0}名@号码{11}最大未出期数{12},".format(
        test_position, number1, number2, number3, number4, number5, number6, number7, number8, number9, number10,p+1,max))

    return {test_position:{"最大未出期数":max,"未出号码":p+1} }



if __name__ == "__main__":
    get_current_day_data()
    MAX = 0
    MAX_DICT = {}
    for i in range(10):
        rank_dict = scan_number(test_position=i+1)
        if rank_dict[i+1]["最大未出期数"] > MAX:
            MAX = rank_dict[i+1]["最大未出期数"]
            MAX_DICT = rank_dict

    print("\033[1;36;m",MAX_DICT)
