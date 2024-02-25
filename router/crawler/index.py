from fastapi import APIRouter, Request, BackgroundTasks
from .goodInfo import postGoodInfo, getGoodInfoCrossData
import asyncio

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
    return 'ing'

# 取得cross1020資料庫資料
# day：交易日期（格式2024-02-25）
# type：bull or bear去區分多空
@router.get('/goodInfo/{crossType}/{day}/{marketType}')
def api(day, marketType, crossType):
    result = getGoodInfoCrossData(day, marketType, crossType)
    return result

