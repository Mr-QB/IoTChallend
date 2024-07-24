import json
import paho.mqtt.client as mqtt

# Thông tin MQTT Broker
broker = "192.168.0.118"  # Địa chỉ của MQTT Broker
port = 1883  # Cổng mặc định của MQTT

# Thông tin đăng nhập
username = ""  # Thay bằng username của bạn
password = ""  # Thay bằng password của bạn

# Topic để đăng ký
topic = "/test"  # Thay bằng topic của bạn


# Hàm callback khi kết nối đến MQTT Broker thành công
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Kết nối thành công!")
        # Đăng ký vào topic
        client.subscribe(topic)
    else:
        print(f"Kết nối thất bại với mã lỗi {rc}")


# Hàm callback khi nhận được tin nhắn từ MQTT Broker
def on_message(client, userdata, msg):
    try:
        # Chuyển đổi payload từ bytes sang chuỗi
        message = msg.payload.decode("utf-8")
        if message == "OFF":
            client.publish("/plug", "poweroff1", 0, True)
        elif message == "ON":
            client.publish("/plug", "poweron1", 0, True)
    except json.JSONDecodeError as e:
        print(f"Lỗi giải mã JSON: {e}")


# Tạo một client MQTT
client = mqtt.Client()

# Thiết lập thông tin đăng nhập nếu có
if username and password:
    client.username_pw_set(username, password)

# Gán các hàm callback
client.on_connect = on_connect
client.on_message = on_message

# Kết nối đến MQTT Broker
client.connect(broker, port, 60)

# Chạy vòng lặp để giữ kết nối và lắng nghe tin nhắn
client.loop_forever()
