#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/10/6 21:05'
import requests
from lxml import etree




def get_current_day_data():

    """获取某日的数据"""

    url = "https://www.1395p.com/pk10/kaijiang"
    res = requests.get(url=url)
    html = res.text
    selector = etree.HTML(html)
    tr_list = selector.xpath('//*[@id="history"]/tbody/tr')
    f = open("K:\\pyProject\\21天爬虫\\pk10\\data\\current_day_data.txt", "w", encoding="UTF-8")
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

if __name__ == "__main__":
    get_current_day_data()