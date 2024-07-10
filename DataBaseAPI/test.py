import pandas as pd
from pymongo import MongoClient
import numpy as np

# Kết nối tới MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["RcuetProject"]  # Tên cơ sở dữ liệu của bạn
face_collection = db["faces_data"]  # Tên bộ sưu tập của bạn

cursor = face_collection.find({})
data_list = list(cursor)
face_data = pd.DataFrame(data_list)
face_data["embedding"] = face_data["embedding"].apply(np.array)
print(face_data)
