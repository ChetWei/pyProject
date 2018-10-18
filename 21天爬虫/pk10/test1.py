#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/10/6 19:16'





def test_longest_BigOrSmall(position=1):
    """统计某一个位置，连续出现大小的次数"""

    f = open("K:\\pyProject\\21天爬虫\\pk10\\data\\pk10-2018-data.txt", "r", encoding="UTF-8")
    BIG_COUNT = 0
    SMALL_COUNT = 0
    MAX_BIG_COUNT = 0
    MAX_SMALL_COUNT = 0
    while True:
        line = f.readline()
        if line != '':
            term_list = line.split(' ')
            number = term_list[position]
            if int(number) > 5:
                SMALL_COUNT = 0
                BIG_COUNT += 1
                if BIG_COUNT > MAX_BIG_COUNT:
                    MAX_BIG_COUNT = BIG_COUNT
            else:
                BIG_COUNT = 0
                SMALL_COUNT += 1
                if SMALL_COUNT > MAX_SMALL_COUNT:
                    MAX_SMALL_COUNT = SMALL_COUNT
        else:
            print("读取完毕！")
            print("{0}位置,连续出现大最多的次数:{1}".format(position,MAX_BIG_COUNT))
            print("{0}位置,连续出现小最多的次数:{1}".format(position,MAX_SMALL_COUNT))
            break
    f.close()

def test_logest_positiveOrNegative(position):
    """统计某一个位置，连续出现单双的次数"""

    f = open("K:\\pyProject\\21天爬虫\\pk10\\data\\pk10-2018-data.txt", "r", encoding="UTF-8")
    DOUBLE_COUNT = 0
    SINGLE_COUNT = 0
    MAX_DOUBLE_COUNT = 0
    MAX_SINGLE_COUNT = 0
    while True:
        line = f.readline()
        if line != '':
            term_list = line.split(' ')
            number = term_list[position]
            if int(number)%2 == 0:  #双
                SINGLE_COUNT = 0
                DOUBLE_COUNT += 1
                if DOUBLE_COUNT > MAX_DOUBLE_COUNT:
                    MAX_DOUBLE_COUNT = DOUBLE_COUNT
            else:      #单
                DOUBLE_COUNT = 0
                SINGLE_COUNT += 1
                if SINGLE_COUNT > MAX_SINGLE_COUNT:
                    MAX_SINGLE_COUNT = SINGLE_COUNT
        else:
            print("读取完毕！")
            print("{0}位置,连续出现双最多的次数:{1}".format(position, MAX_DOUBLE_COUNT))
            print("{0}位置,连续出现单最多的次数:{1}".format(position, MAX_SINGLE_COUNT))
            break
    f.close()





if __name__ == "__main__":
    #test_longest_BigOrSmall(1)

    test_logest_positiveOrNegative(1)