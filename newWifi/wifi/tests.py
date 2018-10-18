from django.test import TestCase

# Create your tests here.
import re
import math

if __name__ == "__main__":
    str = '[转账] 31元已转账成功，请使用手机QQ查看。'

    transfer = re.match('^\[转账\]\s(\d+.?\d+)+元已转账成功，请使用手机QQ查看。',str)
    if transfer:
        money = float(transfer.group(1))
        print(money)


        if money < 1 :
            print(math.floor(money/0.3))

        elif money == 1:
            print(3)

        elif money > 1 and money < 10:
            time = math.floor(money/0.25)
            print(time)

        elif money == 10 :
            print(50)

        elif money > 10 and money < 30:
            print(50 + math.floor((money-10)/0.2))

        elif money == 30:
            print(200)

        elif money > 30:
            print(200 + math.floor((money-30)/0.18))
