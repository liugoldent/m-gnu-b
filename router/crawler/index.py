from fastapi import APIRouter, Request, BackgroundTasks
from .goodInfo import postGoodInfo, getGoodInfoCrossData, getEchartsObj
import asyncio
from ..public.getDifference import getDifferenceFunc

router = APIRouter()


@router.get('/')
def api():
    return {'msg': "crawler Connect OK"}

# 更新collection資料庫
@router.post('/goodInfo/{crossType}')
async def api(background_tasks: BackgroundTasks, crossType: str):
    background_tasks.add_task(postGoodInfo, crossType)
    # result = postGoodInfo(crossType)
    return 'ing'

# 一次更新所有collection資料庫
@router.post('/goodInfo')
async def api(background_tasks: BackgroundTasks):
    background_tasks.add_task(postGoodInfo, 'cross1020')
    background_tasks.add_task(postGoodInfo, 'cross0520')
    background_tasks.add_task(postGoodInfo, 'cross051020')
    return 'ing'

# 取得cross資料庫資料
# {crossType}：是哪個資料庫（cross1020 or cross0520
# {listType}：是取交集或是單純列表
# {marketType}：bull or bear去區分多空
@router.post('/goodInfo/{crossType}/{listType}/{marketType}')
async def api(listType, marketType, crossType, request: Request):
    postData = await request.json()
    rawDay = postData['day']
    resultObj = {}
    list1 = getGoodInfoCrossData(rawDay['day1'], marketType, crossType)
    if listType == 'list':
        return list1
    if listType == 'difference':
        list2 = getGoodInfoCrossData(rawDay['day2'], marketType, crossType)
        resultObj[marketType] = [] if len(list1[marketType]) > len(list2[marketType]) else getDifferenceFunc(list1[marketType], list2[marketType])
        return resultObj


@router.post('/echarts')
async def api():
    result = getEchartsObj('cross1020')
    return result