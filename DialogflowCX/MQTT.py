import json
import paho.mqtt.client as mqtt


"""
install mosquitto windown :
    net start mosquitto
    mosquitto -p 1883
"""

# Thông tin MQTT Broker
broker = "localhost"  # Địa chỉ của MQTT Broker (ví dụ: "mqtt.eclipse.org")
port = 1883  # Cổng mặc định của MQTT

# Thông tin đăng nhập
username = ""  # Thay bằng username của bạn
password = ""  # Thay bằng password của bạn


# Chuyển đổi payload sang định dạng JSON
# Hàm callback khi kết nối tới broker thành công
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Public payload JSON lên topic


# Tạo một client MQTT
client = mqtt.Client()

# Thiết lập thông tin đăng nhập
client.username_pw_set(username, password)

# Gán hàm callback cho sự kiện kết nối
client.on_connect = on_connect
# Kết nối tới MQTT Broker
client.connect(broker, port, 60)

# json_file =  chatbot......()

# ten_phong = 'abc'
# ten_thiet_bi = "den"
trang_thai = "bat"
id_thietbi = "den_2"

# id_thietbi = data[ten_phong][ten_thiet_bi]


topic = "control thiet bi"
msg = "{} {}".format(id_thietbi, trang_thai)
client.publish(topic, msg, 0, True)
# client.subscribe("#")
# client.on_message = on_message
# Chờ client xử lý các sự kiện
