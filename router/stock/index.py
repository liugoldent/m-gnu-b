from fastapi import APIRouter, Request
router = APIRouter()


@router.get('/')
def api():
    return {'msg': "stock Connect OK"}



