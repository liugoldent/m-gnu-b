from lxml import etree
from datetime import datetime
from ..public.fakeUserAgentGenerate import userAgentRoute
from ..public.db import postDBGoodInfoCross, getDBGoodInfoData
import re

import time
import requests


# goodInfoBullUrl = {
#     'bull': 'https://goodinfo.tw/tw2/StockList.asp?RPT_TIME=&MARKET_CAT=%E6%99%BA%E6%85%A7%E9%81%B8%E8%82%A1&INDUSTRY_CAT=10%E6%97%A5%2F20%E6%97%A5%E7%B7%9A%E5%A4%9A%E9%A0%AD%E6%8E%92%E5%88%97%40%40%E5%9D%87%E5%83%B9%E7%B7%9A%E5%A4%9A%E9%A0%AD%E6%8E%92%E5%88%97%40%4010%E6%97%A5%2F20%E6%97%A5',
#     'bear': 'https://goodinfo.tw/tw2/StockList.asp?RPT_TIME=&MARKET_CAT=%E6%99%BA%E6%85%A7%E9%81%B8%E8%82%A1&INDUSTRY_CAT=10%E6%97%A5%2F20%E6%97%A5%E7%B7%9A%E7%A9%BA%E9%A0%AD%E6%8E%92%E5%88%97%40%40%E5%9D%87%E5%83%B9%E7%B7%9A%E7%A9%BA%E9%A0%AD%E6%8E%92%E5%88%97%40%4010%E6%97%A5%2F20%E6%97%A5'
# }
goodInfoTypeUrl = {
    'cross1020': {
        'bull': 'https://goodinfo.tw/tw2/StockList.asp?RPT_TIME=&MARKET_CAT=%E6%99%BA%E6%85%A7%E9%81%B8%E8%82%A1&INDUSTRY_CAT=10%E6%97%A5%2F20%E6%97%A5%E7%B7%9A%E5%A4%9A%E9%A0%AD%E6%8E%92%E5%88%97%40%40%E5%9D%87%E5%83%B9%E7%B7%9A%E5%A4%9A%E9%A0%AD%E6%8E%92%E5%88%97%40%4010%E6%97%A5%2F20%E6%97%A5',
        'bear': 'https://goodinfo.tw/tw2/StockList.asp?RPT_TIME=&MARKET_CAT=%E6%99%BA%E6%85%A7%E9%81%B8%E8%82%A1&INDUSTRY_CAT=10%E6%97%A5%2F20%E6%97%A5%E7%B7%9A%E7%A9%BA%E9%A0%AD%E6%8E%92%E5%88%97%40%40%E5%9D%87%E5%83%B9%E7%B7%9A%E7%A9%BA%E9%A0%AD%E6%8E%92%E5%88%97%40%4010%E6%97%A5%2F20%E6%97%A5'
    },
    'cross0520': {
        'bull': 'https://goodinfo.tw/tw2/StockList.asp?RPT_TIME=&MARKET_CAT=%E6%99%BA%E6%85%A7%E9%81%B8%E8%82%A1&INDUSTRY_CAT=5%E6%97%A5%2F20%E6%97%A5%E7%B7%9A%E5%A4%9A%E9%A0%AD%E6%8E%92%E5%88%97%40%40%E5%9D%87%E5%83%B9%E7%B7%9A%E5%A4%9A%E9%A0%AD%E6%8E%92%E5%88%97%40%405%E6%97%A5%2F20%E6%97%A5',
        'bear': 'https://goodinfo.tw/tw2/StockList.asp?RPT_TIME=&MARKET_CAT=%E6%99%BA%E6%85%A7%E9%81%B8%E8%82%A1&INDUSTRY_CAT=5%E6%97%A5%2F20%E6%97%A5%E7%B7%9A%E7%A9%BA%E9%A0%AD%E6%8E%92%E5%88%97%40%40%E5%9D%87%E5%83%B9%E7%B7%9A%E7%A9%BA%E9%A0%AD%E6%8E%92%E5%88%97%40%405%E6%97%A5%2F20%E6%97%A5'
    }
}
# 更新goodInfo交叉資料
def postGoodInfo(type):
    goodInfoUrl = goodInfoTypeUrl[type]
    finalResult = {}
    currentTime = datetime.now()
    for keyItem, urlItem in goodInfoUrl.items():
        response = requests.get(urlItem, headers={'User-Agent': userAgentRoute()})
        time.sleep(2)
        response.encoding = 'utf-8'
        htmlTree = etree.HTML(response.text)
        
        categoryCodeList = htmlTree.xpath('//*[@id="divStockList"]/table[2]/tr/td[1]/nobr/a/text()')
        categoryNameList = htmlTree.xpath('//*[@id="divStockList"]/table[2]/tr/td[2]/nobr/a/text()')
        categoryCloseList = htmlTree.xpath('//*[@id="divStockList"]/table[1]/tr/td[3]/nobr/a/text()')
        categoryVolumeList = htmlTree.xpath('//*[@id="divStockList"]/table[1]/tr/td[6]/nobr')
        categoryDateList = htmlTree.xpath('//*[@id="divStockList"]/table[1]/tr/td[7]/nobr')
        categoryBias10List = htmlTree.xpath('//*[@id="divStockList"]/table[1]/tr/td[9]/@title')
        categoryBias20List = htmlTree.xpath('//*[@id="divStockList"]/table[1]/tr/td[11]/@title')

        listResult = []
        for index, item in enumerate(categoryVolumeList):
            if ',' in categoryVolumeList[index].text:
                code = categoryCodeList[index]
                name = categoryNameList[index]
                close = float(categoryCloseList[index])
                volume = int(categoryVolumeList[index].text.replace(',', ''))
                updateDay = categoryDateList[index].text
                bias10 = getBias(categoryBias10List[index])
                bias20 = getBias(categoryBias20List[index])
                
                listResult.append({
                    'code': code,
                    'name': name,
                    'close': close,
                    'volume': volume,
                    'updateDay': f"{currentTime.year}/{updateDay}",
                    'buyOrSell': keyItem,
                    'bias10': bias10,
                    'bias20': bias20
                })
        finalResult[keyItem] = listResult
    finalResult['updateDay'] = f"{(finalResult['bull'][0]['updateDay']).replace('/', '-')}"
    postDBGoodInfoCross(finalResult, type)

# 計算Bias
def getBias(text):
    pattern = r"([+-]?\d+(\.\d+)?%)"
    result = re.search(pattern, text)
    if result: 
        rawPercent = result.group()[:-1]
        return float(rawPercent)
    else:
        return 100
    
# 取得某日的cross1020結果
def getGoodInfoCrossData(day, marketType, crossType):
    listResult = {
        'bear': [],
        'bull': [],
        'updateDay': ''
    }
    rawList = getDBGoodInfoData(day, crossType)
    for key in rawList:
        listResult['bear'] = key['bear']
        listResult['bull'] = key['bull']
        listResult['updateDay'] = key['updateDay']
    return {
        marketType: listResult[marketType],
        'updateDay':  key['updateDay']
    }