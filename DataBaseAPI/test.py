import pandas as pd
from pymongo import MongoClient
import numpy as np
from random import randint

# id = str(randint(1000, 5000))

# Kết nối tới MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["RcuetProject"]  
face_collection = db["faces_data"]  
devices_collection = db["Devices"]  

id = randint(1000, 5000)
cursor = devices_collection.find({})

new_device = {"device_name": "", "room_name": "", "id": id}
devices_collection.insert_one(new_device)
