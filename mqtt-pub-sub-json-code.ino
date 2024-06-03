#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

WiFiClient espClient;
PubSubClient client(espClient);

//khai báo địa chỉ, tên và tài khoản MQTT broker
const char* mqtt_server = "";
const char* mqttUser = "";
const char* mqttPassword = ""; 

// tên và password Wi-fi  
#define SSID "";
#define PASSWORD "";
DynamicJsonDocument doc(1024);
/*
Thiết bị sẽ luôn lắng nghe đến broker. Khi broker nhận được một message thì tức là thiết bị
cũng sẽ lắng nghe được 1 message và khi này hàm callback sẽ được khởi tạo
*/
void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  //in ra tên topic (tên topic sẽ được lưu ở biến topic dưới dạng char)
  Serial.print(topic);
  Serial.print(". Message: ");
  //Khởi tạo một biến để lưu lại message (message sẽ được lưu dưới dạng string)
  String data;
  for (int i = 0; i < length; i++) {
    data += (char)message[i];
  }
  Serial.println(data);
  //hàm chuyển dữ liệu từ dạng string sang json
  DeserializationError error = deserializeJson(doc, data); //decode từ string sang json
  if (error == 0){
    Serial.println(doc);
  } 
  else Serial.println("Decode Error")

  // thực thi lệnh khi nhận được từ topic mong muốn
  if(strcmp(topic, "example/example1") == 0 ){ //ví dụ nhận được topic từ topic /example/example1
    //in ra payload của topic nhận được dưới dạng json
    Serial.println(doc);
  }
  
  Serial.println("Exit Call back");
}
void setup(){
    Serial.begin(115200);

  WiFi.mode(WIFI_STA);  
  pinMode(LED_PIN, OUTPUT);

WiFi.begin(SSID, PASSWORD);
    Serial.println("\nConnecting");

    while(WiFi.status() != WL_CONNECTED){
        Serial.print(".");
        delay(100);
    }

    Serial.println("\nConnected to the WiFi network");
    Serial.print("Local ESP32 IP: ");
    Serial.println(WiFi.localIP());
    //port của mqtt server ở đây (thường sử dụng port 1883)
    client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32", mqttUser, mqttPassword)) {
      client.subscribe("lightDim");
      Serial.println("Connect Success");
    } else {
  
      Serial.print("failed, rc=");
      Serial.print(client.state());
      delay(1000);
    }
  }
}

void loop(){
    if (!client.connected()) {
    reconnect();
  }
    client.loop();

  doc["hello"] = "xin chao";
  doc["goodbye"] = "tam biet";
    //hàm publish lên mqtt broker
  client.publish("example/exmaple2", doc);
}
