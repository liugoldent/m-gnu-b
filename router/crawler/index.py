from fastapi import APIRouter, Request
from .goodInfo import postGoodInfo, getGoodInfoCross1020

router = APIRouter()


@router.get('/')
def api():
    return {'msg': "crawler Connect OK"}


@router.post('/goodInfo/cross1020')
def api():
    result = postGoodInfo()
    return result

# 取得cross1020資料庫資料
# day：交易日期（格式2024-02-25）
# type：bull or bear去區分多空
@router.get('/goodInfo/cross1020/{day}/{marketType}')
def api(day, marketType):
    result = getGoodInfoCross1020(day, marketType)
    return result

