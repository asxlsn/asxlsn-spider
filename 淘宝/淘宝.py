
import json
import pandas as pd
import re
from DrissionPage import ChromiumPage, ChromiumOptions

co = ChromiumOptions().set_browser_path(r'F:\Google\Chrome\Application\chrome.exe')
page = ChromiumPage(co)
page.get('https://www.taobao.com/')

#搜索输入框
page.ele('css:.search-suggest-combobox-imageSearch-input').input('小米15')
page.listen.start('h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0',method='GET')
#搜索按钮
page.ele('css:.btn-search.tb-bg').click()

response = page.listen.wait().response
tb_data = response.body
# print(tb_data)
data = re.findall('mtopjsonp\d+\((.*)\)', tb_data)[0]

mtop_data = json.loads(data)
itemArray =mtop_data["data"]["itemsArray"]
for item in itemArray:
    print(item['title'])
