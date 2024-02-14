from lxml import etree
from datetime import datetime
from ..public.fakeUserAgentGenerate import userAgentRoute
import re

import time
import requests


goodInfoBullUrl = {
    'bull': 'https://goodinfo.tw/tw2/StockList.asp?RPT_TIME=&MARKET_CAT=%E6%99%BA%E6%85%A7%E9%81%B8%E8%82%A1&INDUSTRY_CAT=10%E6%97%A5%2F20%E6%97%A5%E7%B7%9A%E5%A4%9A%E9%A0%AD%E6%8E%92%E5%88%97%40%40%E5%9D%87%E5%83%B9%E7%B7%9A%E5%A4%9A%E9%A0%AD%E6%8E%92%E5%88%97%40%4010%E6%97%A5%2F20%E6%97%A5',
}

def postGoodInfo():
    keys_list = list(goodInfoBullUrl.keys())
    values_list = list(goodInfoBullUrl.values())
    listResult = []
    for index, urlItem in enumerate(values_list):
        codeList = []
        nameList = []
        closeList = []
        volumeList = []
        updateDateList = []
        ma10BiasList = []
        ma20BiasList = []
        response = requests.get(urlItem, headers={
                'User-Agent': userAgentRoute()})
        time.sleep(2)
        response.encoding = 'utf-8'  # 設置編碼
        htmlTree = etree.HTML(response.text)
        categoryCodeList = htmlTree.xpath(
            '//*[@id="divStockList"]/table[2]/tr/td[1]/nobr/a/text()')
        categoryNameList = htmlTree.xpath(
            '//*[@id="divStockList"]/table[2]/tr/td[2]/nobr/a/text()')
        categoryCloseList = htmlTree.xpath(
            '//*[@id="divStockList"]/table[1]/tr/td[3]/nobr/a/text()')

        categoryVolumeList = htmlTree.xpath(
            '//*[@id="divStockList"]/table[1]/tr/td[6]/nobr')
        categoryDateList = htmlTree.xpath(
            '//*[@id="divStockList"]/table[1]/tr/td[7]/nobr')
        categoryBias10List = htmlTree.xpath(
            '//*[@id="divStockList"]/table[1]/tr/td[9]/@title')
        categoryBias20List = htmlTree.xpath(
            '//*[@id="divStockList"]/table[1]/tr/td[11]/@title')
        for codeIndex, item in enumerate(categoryCodeList):
                codeList.append(item)
        for codeIndex, item in enumerate(categoryNameList):
                nameList.append(item)
        for codeIndex, item in enumerate(categoryCloseList):
                closeList.append(float(item))

        for codeIndex, item in enumerate(categoryVolumeList):
                volumeList.append(item.text)
        for codeIndex, item in enumerate(categoryDateList):
                updateDateList.append(item.text)
        for codeIndex, item in enumerate(categoryBias10List):
                pattern = r"([+-]?\d+(\.\d+)?%)"
                result = re.search(pattern, item)
                if result: 
                    rawPercent = result.group()[:-1]
                    ma10BiasList.append(float(rawPercent))
                else:
                    ma10BiasList.append(100)
        for codeIndex, item in enumerate(categoryBias20List):
                pattern = r"([+-]?\d+(\.\d+)?%)"
                result = re.search(pattern, item)
                if result: 
                    rawPercent = result.group()[:-1]
                    ma20BiasList.append(float(rawPercent))
                else:
                    ma20BiasList.append(100)
        
        for nameIndex, item in enumerate(volumeList):
            if ',' in item:
                listResult.append({
                    'code': codeList[nameIndex], 
                    'name': nameList[nameIndex], 
                    'close': closeList[nameIndex],
                    'updateData': updateDateList[nameIndex],
                    'time': datetime.now(), 
                    'buyOrSell': keys_list[index],
                    'volume': int(item.replace(',', '')),
                    'bias10': ma10BiasList[nameIndex],
                    'bias20': ma20BiasList[nameIndex],
                })
        time.sleep(2.5)
    return listResult

def getGoodInfo():
    listResult = {
        'sell': [],
        'buy': []
    }
    rawList = getGoodInfoDb('local1')
    for item in rawList:
        if item['buyOrSell'] == 'sell':
            # listResult['sell'].append({'code': item['code'], 'name': item['name'], 'buyOrSell': item['buyOrSell']}) 這裡是所有可以拿的資料
            # 但因為篩選，所以回傳code而已
            listResult['sell'].append(item['code'])
        if item['buyOrSell'] == 'buy':
            listResult['buy'].append(item['code'])
    return listResult