#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/10/6 17:06'
import requests
from lxml import etree


def judge_year(year):
    if year % 100 == 0:
        if year % 400 == 0:
            return True

    else:
        if (year % 4 == 0):
            return True

    return False




def get_two_str_number(number):
    if number < 10 and number > 0 :
        str_number = str(number)
        return "0"+str_number

    elif number >= 10:
        str_number = str(number)
        return str_number



def get_month_day_by_yearAndmonth(year,month):
    if month in (1,3,5,7,8,10,12):
        return 31
    elif month in (4,6,9,11):
        return 30

    elif month == 2:
        if judge_year(year):
            return 29
        else:
            return 28



def get_str_date(year=2018,start_month=1,stop_month=12):
    str_year = str(year)
    while start_month < stop_month:
        str_month = get_two_str_number(start_month)
        MONTHDAY = get_month_day_by_yearAndmonth(year=year,month=start_month)
        for i in range(MONTHDAY):
            DAY = i+1
            str_day = get_two_str_number(DAY)
            str_date = str_year+"-"+str_month+"-"+str_day
            yield str_date
        start_month += 1











def get_pk10_data(day='2018-01-01'):
    url = "https://www.55128.cn/zs/115_999.htm?searchTime={0}".format(day)

    res = requests.get(url=url)

    html = res.text
    selector = etree.HTML(html)

    tr_list = selector.xpath('//*[@id="chartData"]/tr')

    f = open("K:\\pyProject\\21天爬虫\\pk10\\data\\pk10-2018-data.txt","a",encoding="UTF-8")
    for tr in tr_list:
        term_number = tr.xpath('td[1]/text()')[0]
        number_1 = tr.xpath('td[2]/text()')[0]
        number_2 = tr.xpath('td[3]/text()')[0]
        number_3 = tr.xpath('td[4]/text()')[0]
        number_4 = tr.xpath('td[5]/text()')[0]
        number_5 = tr.xpath('td[6]/text()')[0]
        number_6 = tr.xpath('td[7]/text()')[0]
        number_7 = tr.xpath('td[8]/text()')[0]
        number_8 = tr.xpath('td[9]/text()')[0]
        number_9 = tr.xpath('td[10]/text()')[0]
        number_10 = tr.xpath('td[11]/text()')[0]

        line_data = term_number+" "+number_1+" "+number_2+" "+number_3+" "+number_4+" "+number_5+" "+number_6+" "+number_7+" "+number_8+" "+number_9+" "+number_10+"  \n"
        f.write(line_data)


if __name__ == "__main__":
    date_generate = get_str_date(year=2018,start_month=1,stop_month=10)
    for day in date_generate:
        get_pk10_data(day=day)