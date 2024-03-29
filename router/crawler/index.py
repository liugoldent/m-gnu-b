from fastapi import APIRouter, Request, BackgroundTasks
from .goodInfo import postGoodInfo, getGoodInfoCrossData, getEchartsObj, getTurnOverStockList, postInvestorList
import asyncio
from ..public.getDifference import getDifferenceFunc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import time


router = APIRouter()


@router.get('/')
def api():
    return {'msg': "crawler Connect OK"}

# 更新collection資料庫
@router.post('/goodInfo/{crossType}')
async def api(background_tasks: BackgroundTasks, crossType: str):
    background_tasks.add_task(postGoodInfo, crossType)
    return 'ing'

# 一次更新所有collection資料庫
@router.post('/goodInfo')
async def api():
    scheduler = BackgroundScheduler(timeZone='Asia/Shanghai')
    def task1():
        postGoodInfo('cross1020')
    def task2():
        postGoodInfo('cross0520')
    def task3():
        postGoodInfo('cross051020')
    def task4():
        getTurnOverStockList()
    def task5():
        postInvestorList()
    scheduler.add_job(
        task1, 
        trigger=CronTrigger(hour=22, minute=00),
        id="task1", 
        name="每天晚上22:00执行的定时任务"  
    )  
    scheduler.add_job(
        task2, 
        trigger=CronTrigger(hour=22, minute=40),
        id="task2", 
        name="每天晚上22:00执行的定时任务"  
    )  
    scheduler.add_job(
        task3, 
        trigger=CronTrigger(hour=22, minute=10),
        id="task3", 
        name="每天晚上22:00执行的定时任务"  
    )  
    scheduler.add_job(
        task4, 
        trigger=CronTrigger(hour=22, minute=20),
        id="task4", 
        name="每天晚上22:00执行的定时任务"  
    )  
    scheduler.add_job(
        task5, 
        trigger=CronTrigger(hour=22, minute=30),
        id="task5", 
        name="每天晚上22:00执行的定时任务"  
    )  
    scheduler.start()
    # 以下是背景任務
    # time.sleep(2)
    # background_tasks.add_task(postGoodInfo, 'cross1020')
    # time.sleep(2)
    # background_tasks.add_task(postGoodInfo, 'cross0520')
    # time.sleep(2)
    # background_tasks.add_task(getTurnOverStockList)
    # postInvestorList()
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


# 取得cross資料庫資料
# {crossType}：是哪個資料庫（cross1020 or cross0520
# {listType}：是取交集或是單純列表
# {marketType}：bull or bear去區分多空
@router.post('/goodInfo/turnOver/list')
def api():
    getTurnOverStockList()