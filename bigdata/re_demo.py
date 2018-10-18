#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/9/24 9:33'

import re


logs = '"27.38.5.159" "-" "31/Aug/2015:00:04:54 +0800" "GET /theme/yui_combo.php?m/1427679483/block_navigation/navigation/navigation-min.js HTTP/1.1" "200" "3030" - "http://learn.ibeifeng.com/course/view.php?id=27" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36" "-" "learn.ibeifeng.com"'


fileHandle = open('bf.log','w',encoding='UTF-8')

result = re.match(r'^"([[\d|.]+)"\s"(.?)"\s"([^"]+)"\s"([^"]+)"\s"([^"]+)"\s"([^"]+)"\s([^"]+)\s"([^"]+)"\s"([^"]+)"\s"([^"]+)"\s"([^"]+)',logs)

with open('beifen.log') as logs :
    while True:
        line = logs.readline()
        if not line:
            break
        res = re.match(r'^"([[\d|.]+)"\s"(.?)"\s"([^"]+)"\s"([^"]+)"\s"([^"]+)"\s"([^"]+)"\s([^"]+)\s"([^"]+)"\s"([^"]+)"\s"([^"]+)"\s"([^"]+)',line)
        for j in range(11):
            fileHandle.write(res.group(j+1))
            fileHandle.write("\t")
        fileHandle.write("\n")