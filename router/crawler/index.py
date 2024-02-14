from fastapi import APIRouter, Request
from .goodInfo import postGoodInfo

router = APIRouter()


@router.get('/')
def api():
    return {'msg': "crawler Connect OK"}


@router.get('/goodInfo')
def api():
    result = postGoodInfo()
    return result
