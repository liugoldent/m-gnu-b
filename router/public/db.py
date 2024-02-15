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
 

# 取得 goodInfo 10cross20 collection
def getDBGoodInfoCross1020(day):
    db = client['goodInfo']
    result = db['cross1020'].find({'updateDay': day})
    print(result)
    return result


# 更新goodInfo 10cross20 collection
def postDBGoodInfoCross1020(codeObject):
    db = client['goodInfo']
    db['cross1020'].insert_one(codeObject)