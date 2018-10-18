#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/10/5 2:06'



"""1块起步，1元获利，追本 (1,3,5,10,20,40,80...) 本金x"""

strategy_tupe = (1,3,5,10,20,40,80,100,300,500,1000,500,500)
index = 0
BALANCE = 2559 #余额
WANT = 3000
NEXT_BET = 0  #投注
BET_SUM = 0 #累计投注
RESULT = ""
GUESS_NEXT_RESULT = "大" #设定第一次开始的猜测

#统计连续输赢次数
MAX_CONTINUE_WIN = 0
MAX_CONTINUE_LOSE = 0
CONTINU_WIN = 0
CONTINU_LOSE = 0


#获得上一把，第一名的大小

f = open("K:\\pyProject\\21天爬虫\\happy\\real_data\\month09\\draw-speed10-20180913.txt",'r',encoding="UTF-8")
lines = f.readlines()

for line in lines:
    number_list = line.split(" ")
    term_number = number_list[0]
    number_1 = number_list[1]
    print(term_number+" "+number_1)


    #判断当前期的冠军大小
    if int(number_1) > 5: #大号
        RESULT = "大"
    else: #小号
        RESULT = "小"

    #比对猜测结果
    if RESULT == "大":
        if GUESS_NEXT_RESULT == RESULT:  #如果中

            #统计连续中的最多次数
            CONTINU_WIN += 1
            if CONTINU_WIN > MAX_CONTINUE_WIN:
                MAX_CONTINUE_WIN = CONTINU_WIN

            CONTINU_LOSE = 0 #连续输的次数归零
            BALANCE += NEXT_BET  #剩余余额

            #判断余额是否到达：
            if BALANCE >= WANT:
                break

            GUESS_NEXT_RESULT = "大"  #下一次猜测
            NEXT_BET = strategy_tupe[0]  #下一次投注量，从头开始
            index = 0 #偏移量回0
            print("\033[1;32;m第{0}期 *投注大* #结果大# 中奖,余额为\033[1;35;m{1}\033[0m,下一次猜测:{2} 投注:{3}\033[0m".format(term_number,BALANCE,GUESS_NEXT_RESULT,NEXT_BET))
        elif GUESS_NEXT_RESULT != RESULT: #如果没有中

            # 统计连续输的最多次数
            CONTINU_LOSE += 1
            if CONTINU_LOSE > MAX_CONTINUE_LOSE:
                MAX_CONTINUE_LOSE = CONTINU_LOSE

            CONTINU_WIN = 0 #连续赢的次数归零
            index += 1 #投注量偏移一位
            BALANCE -= NEXT_BET #剩余余额
            GUESS_NEXT_RESULT = "大" #下一次猜测
            NEXT_BET = strategy_tupe[index] #下一次投注量
            print("\033[1;31;m第{0}期 *投注小* #结果大# 没中奖,余额为\033[1;35;m{1}\033[0m,下一次猜测：{2} 追投:{3}\033[0m".format(term_number,BALANCE,GUESS_NEXT_RESULT,NEXT_BET))

    elif RESULT == "小":
        if GUESS_NEXT_RESULT == RESULT:  #如果中

            # 统计连续中的最多次数
            CONTINU_WIN += 1
            if CONTINU_WIN > MAX_CONTINUE_WIN:
                MAX_CONTINUE_WIN = CONTINU_WIN

            CONTINU_LOSE = 0  # 连续输的次数归零
            BALANCE += NEXT_BET  #剩余余额

            # 判断余额是否到达：
            if BALANCE > WANT:
                break

            GUESS_NEXT_RESULT = "小"  #下一次猜测
            NEXT_BET = strategy_tupe[0]  #下一次投注量，从头开始
            index = 0  # 偏移量回0
            print("\033[1;32;m第{0}期 *投注小* #结果小# 中奖,余额为\033[1;35;m{1}\033[0m,下一次猜测:{2} 投注:{3}\033[0m".format(term_number, BALANCE, GUESS_NEXT_RESULT, NEXT_BET))

        elif GUESS_NEXT_RESULT != RESULT: #如果没有中

            # 统计连续输的最多次数
            CONTINU_LOSE += 1
            if CONTINU_LOSE > MAX_CONTINUE_LOSE:
                MAX_CONTINUE_LOSE = CONTINU_LOSE

            CONTINU_WIN = 0  # 连续赢的次数归零
            index += 1 #投注量偏移一位
            BALANCE -= NEXT_BET #剩余余额
            GUESS_NEXT_RESULT = "小" #下一次猜测

            NEXT_BET = strategy_tupe[index] #下一次投注量
            print("\033[1;31;m第{0}期 *投注大* #结果小# 没中奖,余额为\033[1;35;m{1}\033[0m,下一次猜测：{2} 追投:{3}\033[0m".format(term_number, BALANCE, GUESS_NEXT_RESULT, NEXT_BET))

print("余额为:",BALANCE)
print("连续中的最大次数为{0}连续输的最大次数为{1}".format(MAX_CONTINUE_WIN,MAX_CONTINUE_LOSE))
