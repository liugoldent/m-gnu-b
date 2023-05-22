# 寫入db
from pymongo import MongoClient
import certifi
from bson import json_util
import json
import os

user_name = 'fintrackerowner'
user_pwd = 'MEyAVn830L7GuiMo'
cluster = f"mongodb+srv://{user_name}:{user_pwd}@cluster0.lzg4zlq.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(cluster, tlsCAFile=certifi.where())
 
# 更新capitalDB
def postCapitalDb(codeList, collectionName):
    db = client['capital']
    db[collectionName].delete_many({})
    db[collectionName].insert_one(codeList)

# 清空capitalDB
def deleteCapitalDb(collectionName):
    db = client['capital']
    db[collectionName].delete_many({})


# 取得空頭or多頭股票
def getBullOrBearCode(collectionName):
    db = client['capital']
    return db[collectionName].find({})

# 更新wantgoo 最新資料
def postWantgoo(codeList,collectionName):
    db = client['wantgoo']
    db[collectionName].delete_many({})
    db[collectionName].insert_many(codeList)

# 取得wantgoo 最新資料
def getWantgoo(collectionName):
    db = client['wantgoo']
    return db[collectionName].find({})

# 更新goodInfo 投信兩日買超前20名：最新資料
def postgoodInfo(codeList, collectionName):
    db = client['goodInfo']
    db[collectionName].insert_many(codeList)

# 刪除goodInfo 投信兩日買超前20名：最新資料
def delgoodInfo(collectionName):
    db = client['goodInfo']
    db[collectionName].delete_many({})

# 取得goodInfo 投信一日買超前20名：最新資料
def getGoodInfoDb(collectionName):
    db = client['goodInfo']
    return db[collectionName].find({})