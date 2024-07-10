import requests

# Gửi yêu cầu GET để nhận dữ liệu từ server
response = requests.get("http://localhost:5000/api/data")
if response.status_code == 200:
    data = response.json()
    print("Received data:", data)
else:
    print("Failed to fetch data")

# Gửi yêu cầu POST để gửi dữ liệu từ client đến server
new_data = {"thietbi": "cong tac 1", "trangthai": "on"}
response = requests.post("http://localhost:5000/api/save", json=new_data)
if response.status_code == 200:
    print("Data saved successfully")
else:
    print("Failed to save data")
