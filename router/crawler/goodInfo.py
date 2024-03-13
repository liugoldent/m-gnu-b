from lxml import etree
from datetime import datetime
from ..public.fakeUserAgentGenerate import userAgentRoute
from ..public.db import postDBGoodInfoCross, getDBGoodInfoData, getCollectionAllData, postDBGoodInfoTurnOver
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
    },
    'cross051020': {
        'bull': 'https://goodinfo.tw/tw2/StockList.asp?RPT_TIME=&MARKET_CAT=%E6%99%BA%E6%85%A7%E9%81%B8%E8%82%A1&INDUSTRY_CAT=5%E6%97%A5%2F10%E6%97%A5%2F20%E6%97%A5%E7%B7%9A%E5%A4%9A%E9%A0%AD%E6%8E%92%E5%88%97%40%40%E5%9D%87%E5%83%B9%E7%B7%9A%E5%A4%9A%E9%A0%AD%E6%8E%92%E5%88%97%40%405%E6%97%A5%2F10%E6%97%A5%2F20%E6%97%A5',
        'bear': 'https://goodinfo.tw/tw2/StockList.asp?RPT_TIME=&MARKET_CAT=%E6%99%BA%E6%85%A7%E9%81%B8%E8%82%A1&INDUSTRY_CAT=5%E6%97%A5%2F10%E6%97%A5%2F20%E6%97%A5%E7%B7%9A%E7%A9%BA%E9%A0%AD%E6%8E%92%E5%88%97%40%40%E5%9D%87%E5%83%B9%E7%B7%9A%E7%A9%BA%E9%A0%AD%E6%8E%92%E5%88%97%40%405%E6%97%A5%2F10%E6%97%A5%2F20%E6%97%A5'
    }
}
overUrl = {
    'tureOver': 'https://goodinfo.tw/tw2/StockList.asp?RPT_TIME=&MARKET_CAT=%E7%86%B1%E9%96%80%E6%8E%92%E8%A1%8C&INDUSTRY_CAT=%E6%88%90%E4%BA%A4%E9%87%91%E9%A1%8D+%28%E9%AB%98%E2%86%92%E4%BD%8E%29%40%40%E6%88%90%E4%BA%A4%E9%87%91%E9%A1%8D%40%40%E7%94%B1%E9%AB%98%E2%86%92%E4%BD%8E'
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
        'updateDay':  listResult['updateDay']
    }

# 取得 echarts 顯示obj
def getEchartsObj(crossType):
    cursor = getCollectionAllData(crossType)
    # 初始化空列表
    bull_lengths = []
    bear_lengths = []
    update_days = []

    # 遍歷查詢結果
    for doc in cursor:
        # 計算 "bull" 和 "bear" 欄位的長度
        bull_lengths.append(len(doc['bull']))
        bear_lengths.append(len(doc['bear']))
        update_days.append(doc['updateDay'])

    # 構建新的字典
    result = {
        "bull": bull_lengths,
        "bear": bear_lengths,
        "updateDay": update_days
    }
    return result

# 取得成交金額排行
def getTurnOverStockList():
    finalResult = {}
    currentTime = datetime.now()
    for keyItem, urlItem in overUrl.items():
        print(urlItem)
        response = requests.get(urlItem, headers={'User-Agent': userAgentRoute()})
        time.sleep(1)
        response.encoding = 'utf-8'
        htmlTree = etree.HTML(response.text)
        categoryCodeList = htmlTree.xpath('//*[@id="divStockList"]/table[2]/tr/td[2]/nobr/a')
        categoryNameList = htmlTree.xpath('//*[@id="divStockList"]/table[2]/tr/td[3]/nobr/a')
        categoryDateList = htmlTree.xpath('//*[@id="divStockList"]/table[1]/tr/td[5]/nobr')
        updateDay = categoryDateList[1].text
        listResult = []
        for index, item in enumerate(categoryCodeList):
            if index <= 50:
                listResult.append({
                    'code': item.text,
                    'name': categoryNameList[index].text,
                    'updateDay': f"{currentTime.year}/{updateDay}",
                })
        finalResult['turnOverList'] = listResult
        finalResult['updateDay'] = f"{(finalResult['turnOverList'][0]['updateDay']).replace('/', '-')}"
    print(finalResult)
    postDBGoodInfoTurnOver(finalResult, 'turnOver')


