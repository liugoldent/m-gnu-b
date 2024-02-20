from fastapi import APIRouter, Request
from .goodInfo import postGoodInfo, getGoodInfoCrossData

router = APIRouter()


@router.get('/')
def api():
    return {'msg': "crawler Connect OK"}

# 更新collection資料庫
@router.post('/goodInfo/{crossType}')
def api(crossType):
    result = postGoodInfo(crossType)
    return result

# 取得cross1020資料庫資料
# day：交易日期（格式2024-02-25）
# type：bull or bear去區分多空
@router.get('/goodInfo/{crossType}/{day}/{marketType}')
def api(day, marketType, crossType):
    result = getGoodInfoCrossData(day, marketType, crossType)
    return result

