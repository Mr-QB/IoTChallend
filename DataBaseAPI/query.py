import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["RcuetProject"]
devices_collection = mydb["Devices"]

query = {"room_name": {"$ne": ""}, "device_name": {"$ne": ""}}

mydoc = devices_collection.find(query)
count = devices_collection.count_documents(query)


print(count)
