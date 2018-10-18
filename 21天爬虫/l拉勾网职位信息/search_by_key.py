#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/9/30 16:46'

import requests
from urllib import parse
import json


def get_company_info(key,page=1,city="全国"):

    referer_key = parse.quote(key)
    search_city = parse.quote(city)

    data = {
    'first':'true',
    'kd':key,  #查询的关键字
    'pn':page,  #页码
    }

    headers = {
        'Host': 'www.lagou.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.lagou.com/jobs/list_{0}?city={1}&labelWords=&fromSearch=true&suginput='.format(referer_key,search_city),
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Anit-Forge-Token': 'None',
        'X-Anit-Forge-Code': '0',
        'Content-Length':'46',
        'Cookie': 'JSESSIONID=ABAAABAAAFCAAEGA14233D1DDC80ED38DBF634DA9683D47; _ga=GA1.2.2137718491.1538313869; _gat=1; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1538313869,1538313922; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1538313922; user_trace_token=20180930212429-28f1d2d8-c4b4-11e8-a85f-525400f775ce; LGSID=20180930212429-28f1d477-c4b4-11e8-a85f-525400f775ce; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DxzJMAjtV6EHTeqm3ouDiWgLcLzQDP-gg9y2_oeS5dqC%26wd%3D%26eqid%3D91a06b460006a4be000000065bb0ce89; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGRID=20180930212522-4883e2b0-c4b4-11e8-bb68-5254005c3644; LGUID=20180930212429-28f1d5f8-c4b4-11e8-a85f-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; _gid=GA1.2.697492424.1538313872; TG-TRACK-CODE=index_search; SEARCH_ID=c45f378e66aa4cc7a3a2a876d7b27570',
        'Connection': 'keep-alive'
    }

    res = requests.post(url="https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false",headers=headers,data=data,timeout=5)
    text = res.content.decode("utf-8")
    json_dict = json.loads(text)
    company_list = json_dict['content']['positionResult']['result']  #单个公司信息列表

    for company in company_list:
        print(company)
        print(company['workYear'])


if __name__ == "__main__":

    for page in range(30):
        get_company_info("python",page=page+1)