#   -*-coding:utf-8 -*-
#   @Author: 'ChetWei'
#   @Time: '2018/10/5 18:26'

import requests

url = "https://cp99136.com/#/game"

headers = {
'Host': 'cp99136.com',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0',
'Cookie': 'ddcp_web=ddcp-web-01; visid_incap_1815066=AfMVkIY1QnaJEZzd8d7WaeA9t1sAAAAAQUIPAAAAAABG09cf4AkzTE8gkCH9DsbT; nlbi_1815066=CbN2OCIINCIF6ozkj/4CCgAAAAAf7CZoB2CSutpFsZ53LVN+; incap_ses_625_1815066=uO78SoieKU/YxxLo+nKsCOA9t1sAAAAANNjHWlEAmK/B8rskfyDi7g==',
'Upgrade-Insecure-Requests': '1',
'TE': 'Trailers'
}

res = requests.get(url=url,headers=headers)
print(res.status_code)
print(res.encoding)
print(res.content.decode())