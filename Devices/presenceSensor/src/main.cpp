// #include <mqttConfig.h>
#include <mqttConfig.h>

void reconnect()
{
  while (!client.connected())
  {
    Serial.print("Đang cố gắng kết nối MQTT...");
    if (client.connect("ESP32Client", mqttUser, mqttPassword))
    {
      Serial.println("Đã kết nối");
      // Đăng ký nếu cần thiết
      client.subscribe(relay_topic);
    }
    else
    {
      Serial.print("Thất bại, rc=");
      Serial.print(client.state());
      Serial.println(" thử lại sau 5 giây");
      delay(5000);
    }
  }
}

void callback(char *topic, byte *payload, unsigned int length)
{
  // Xử lý thông điệp từ MQTT nếu cần
}

// void mqttConfig()
// {
//   client.publish(config_topic, default_id);
// }
void setup()
{

  Serial.begin(115200);
  mySerial.begin(9600, SERIAL_8N1, RX_PIN, TX_PIN); // Cấu hình UART1 9600
  Serial.println("Kiểm tra cảm biến hiện diện LD2410C");
  strcpy(default_id, generateRandomString(10));

  // Kiểm tra UART
  if (mySerial)
  {
    Serial.println("UART1 đã khởi động thành công");
  }
  else
  {
    Serial.println("Khởi động UART1 thất bại");
  }

  // Khởi động WiFiManager
  WiFiManager wifiManager;

  // Xóa thông tin kết nối WiFi trước đó
  // wifiManager.resetSettings();

  // Khởi động kết nối WiFi tự động
  wifiManager.autoConnect("RCUET-Config");

  Serial.println("Kết nối WiFi thành công!");

  // Cấu hình MQTT
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop()
{
  mqttConfig();
  if (!client.connected())
  {
    reconnect();
  }
  client.loop();

  if (mySerial.available())
  {
    String data = "";
    while (mySerial.available())
    {
      char c = mySerial.read();
      data += c;
    }
    Serial.print("Dữ liệu từ LD2410C: ");
    Serial.println(data);

    // Xử lý dữ liệu từ LD2410C
    data.trim();

    // Kiểm tra các trường hợp có người
    if (data.indexOf("i") != -1)
    {
      detectionCount++;
      noDetectionCount = 0; // Đặt lại biến đếm không phát hiện

      if (noDetectionCount <= noDetectionThreshold)
      {
        Serial.println("Phát hiện có người!");
        client.publish(relay_topic, "ON");
      }
    }
    else
    {
      detectionCount = 0; // Đặt lại biến đếm phát hiện
      noDetectionCount++;

      if (noDetectionCount >= noDetectionThreshold)
      {
        detectionCount = 0; // Đặt lại biến đếm phát hiện
        Serial.println("Không phát hiện có người.");
        client.publish(relay_topic, "OFF");
      }
    }
  }
  else
  {
    Serial.println("Không có dữ liệu từ LD2410C");
  }
  delay(1000);
}
