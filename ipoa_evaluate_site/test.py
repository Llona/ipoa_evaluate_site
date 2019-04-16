from pymongo import MongoClient

db_client = MongoClient()
myquery = {"parent_article": "315993"}
reply_list = db_client.data_car['ucar_reply'].find(myquery)
for i in reply_list:
    print(i['page'])
