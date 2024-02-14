from fastapi import APIRouter, Request
from ..public.db import postCapitalDb, getBullOrBearCode
router = APIRouter()


@router.get('/')
def api():
    return {'msg': "stock Connect OK"}

# 更新資料庫code
@router.post("/updateCode")
async def api(request: Request):
    data = await request.json()
    postCapitalDb({
        'code': data['codeArr']
    }, data['marketType'])
    return 'ok'

# 取得資料庫code
@router.post("/getBullBearCode")
async def api(request: Request):
    toFEResult = []
    data = await request.json()
    result = getBullOrBearCode(data['collectionName'])
    for item in result:
        toFEResult.append(item['code'])
    return toFEResult

