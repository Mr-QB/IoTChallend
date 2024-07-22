#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <WiFiManager.h> // Thư viện WiFiManager

int relayPin1 = 26; // Sử dụng GPIO 26 cho relay 1
int relayPin2 = 27; // Sử dụng GPIO 27 cho relay 2

const char *mqtt_server = "192.168.0.118";
const char *mqttUser = "";
const char *mqttPassword = "";

WiFiClient espClient;
PubSubClient client(espClient);

void callback(char *topic, byte *payload, unsigned int length) {
  String cmd = "";
  for (unsigned int i = 0; i < length; i++) {
    cmd += (char)payload[i];
  }
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  Serial.println(cmd);

  if (cmd == "poweron1") {
    digitalWrite(relayPin1, HIGH);
    client.publish("/plug", "poweron1:success");
    delay(10);
  } else if (cmd == "poweroff1") {
    digitalWrite(relayPin1, LOW);
    client.publish("/plug", "poweroff1:success");
  }
  if (cmd == "poweron2") {
    digitalWrite(relayPin2, HIGH);
    client.publish("/plug", "poweron2:success");
  } else if (cmd == "poweroff2") {
    digitalWrite(relayPin2, LOW);
    client.publish("/plug", "poweroff2:success");
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client___", mqttUser, mqttPassword)) {
      Serial.println("connected");
      client.subscribe("/plug");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  pinMode(relayPin1, OUTPUT);
  pinMode(relayPin2, OUTPUT);

  Serial.begin(9600);

  WiFiManager wifiManager;

  // Tạo đối tượng để lưu trữ SSID và mật khẩu WiFi
  WiFiManagerParameter custom_wifi_ssid("wifi_ssid", "WiFi SSID", "", 32);
  WiFiManagerParameter custom_wifi_password("wifi_password", "WiFi Password", "", 64);

  // Thêm đối tượng vào WiFiManager
  wifiManager.addParameter(&custom_wifi_ssid);
  wifiManager.addParameter(&custom_wifi_password);

  // Tự động kết nối và nếu không thành công thì tạo AP với mật khẩu
  wifiManager.setConfigPortalTimeout(180); // Đặt thời gian chờ cho cổng cấu hình (180 giây)
  wifiManager.setMinimumSignalQuality(); // Chấp nhận mọi chất lượng tín hiệu
  wifiManager.setWiFiAutoReconnect(true); // Tự động kết nối lại WiFi khi mất kết nối
  
  if (!wifiManager.autoConnect("RCUET-Config", "rcuet@2024")) {
    Serial.println("Failed to connect and hit timeout");
    delay(3000);
    ESP.restart();
  }

  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // Lấy SSID và mật khẩu từ WiFiManager
  String wifi_ssid = custom_wifi_ssid.getValue();
  String wifi_password = custom_wifi_password.getValue();

  Serial.print("SSID: ");
  Serial.println(wifi_ssid);
  Serial.print("Password: ");
  Serial.println(wifi_password);

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
