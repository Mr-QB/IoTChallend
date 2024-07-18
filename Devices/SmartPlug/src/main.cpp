#include <Arduino.h>
#include <WiFi.h> // Thư viện WiFi cho ESP32
#include <PubSubClient.h>
#include <WiFiManager.h> // Thư viện WiFiManager
#include <WiFiClientSecure.h>

int relayPin1 = 26; // Sử dụng GPIO 26 cho relay 1
int relayPin2 = 27; // Sử dụng GPIO 27 cho relay 2

const char *mqtt_server = "192.168.0.118";
const char *mqttUser = "";
const char *mqttPassword = "";

WiFiClient espClient; // Sử dụng WiFiClientSecure cho SSL/TLS
PubSubClient client(espClient);

void callback(char *topic, byte *payload, unsigned int length)
{
  String cmd = "";
  for (unsigned int i = 0; i < length; i++)
  {
    cmd += (char)payload[i];
  }
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  Serial.println(cmd);

  if (cmd == "poweron1")
  {
    digitalWrite(relayPin1, HIGH);
    client.publish("/plug", "poweron1:success");
    delay(10);
  }
  else if (cmd == "poweroff1")
  {
    digitalWrite(relayPin1, LOW);
    client.publish("/plug", "poweroff1:success");
  }
  if (cmd == "poweron2")
  {
    digitalWrite(relayPin2, HIGH);
    client.publish("/plug", "poweron2:success");
  }
  else if (cmd == "poweroff2")
  {
    digitalWrite(relayPin2, LOW);
    client.publish("/plug", "poweroff2:success");
  }
}

void reconnect()
{
  // Thử kết nối lại MQTT cho đến khi thành công
  while (!client.connected())
  {
    Serial.print("Attempting MQTT connection...");
    // Kết nối sử dụng thông tin đăng nhập
    if (client.connect("ESP32Client___", mqttUser, mqttPassword))
    {
      Serial.println("connected");
      // Đăng ký chủ đề MQTT để nhận lệnh điều khiển
      client.subscribe("/plug");
    }
    else
    {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Đợi 5 giây trước khi thử lại
      delay(5000);
    }
  }
}

void setup()
{
  // Khai báo chân điều khiển relay
  pinMode(relayPin1, OUTPUT);
  pinMode(relayPin2, OUTPUT);

  // Khởi động giao tiếp Serial
  Serial.begin(9600);

  // Khởi động WiFiManager
  WiFiManager wifiManager;

  // Cấu hình cho phép kết nối WiFi
  wifiManager.autoConnect("RCUET-Config");

  // In ra thông tin kết nối WiFi
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // Thiết lập ESPClient cho giao tiếp không an toàn (không có chứng chỉ SSL hợp lệ)
  // espClient.setInsecure();

  // Thiết lập client MQTT
  client.setServer(mqtt_server, 1883); // Sử dụng cổng 8883 cho SSL/TLS
  client.setCallback(callback);
}

void loop()
{
  // Kết nối lại MQTT nếu mất kết nối
  if (!client.connected())
  {
    reconnect();
  }
  // Duy trì kết nối MQTT và xử lý các thông điệp đến
  client.loop();
}