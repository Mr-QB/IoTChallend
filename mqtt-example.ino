
#include <WiFi.h>
#include <WiFiMulti.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

#define LED_PIN 14
#define BTN_PIN 22
#define BOARD_LED_PIN 2

int led_status = LOW;
WiFiMulti wifiMulti;
WiFiClient espClient;  
PubSubClient client(espClient);

const char* mqtt_server = "mqttvcloud.innoway.vn";
const char* mqttUser = "test";
const char* mqttPassword = "hCF0hcIxWi5wXK4f7N7hp3spM8lpHDmd";
const char* deviceID = "3A:34:52:C4:69:B8";
const char* lwt_topic = "3A:34:52:C4:69:B8/connection";
const char* lwt_message = "disconnected";

void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);

  Serial.print(". Message: ");
  String messageTemp;
  

  for (int i = 0; i < length; i++) {
    messageTemp += (char)message[i];
  }
  Serial.println(messageTemp);

  //nếu 2 chuỗi bằng nhau
  if(strcmp(topic, "3A:34:52:C4:69:B8/status") == 0){
    if (messageTemp == "HIGH"){
      led_status = HIGH;
    }
    else if (messageTemp == "LOW"){
      led_status = LOW;
    }
  }
}

void setup(){
    Serial.begin(115200);

  WiFi.mode(WIFI_STA);  
  pinMode(LED_PIN, OUTPUT);
  pinMode(BTN_PIN, INPUT_PULLDOWN);
// Add list of wifi networks
  wifiMulti.addAP("BIGHOME 201", "66668888");
  wifiMulti.addAP("viettel", "88888888");
  wifiMulti.addAP("Omoide Cafe", "0837860886");
  wifiMulti.addAP("PQH", "12345678");

  // WiFi.scanNetworks will return the number of networks found
  
    client.setServer(mqtt_server, 1883);
    client.setCallback(callback);
}
void reconnectWifi() {
  while (wifiMulti.run() != WL_CONNECTED) {
    int n = WiFi.scanNetworks();
    if (n < 0)
      ESP.restart();
    else {
      Serial.println("scan done");
      if (n == 0) {
          Serial.println("no networks found");
      } 
      else {
        Serial.print(n);
        Serial.println(" networks found");
        for (int i = 0; i < n; ++i) {
          // Print SSID and RSSI for each network found
          Serial.print(i + 1);
          Serial.print(": ");
          Serial.print(WiFi.SSID(i));
          Serial.print(" (");
          Serial.print(WiFi.RSSI(i));
          Serial.print(")");
          Serial.println((WiFi.encryptionType(i) == WIFI_AUTH_OPEN)?" ":"*");
          delay(10);
      }
    }
    
  }
  }
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected() && wifiMulti.run() == WL_CONNECTED) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32", mqttUser, mqttPassword, lwt_topic, 0, true, lwt_message)) {
      client.subscribe("3A:34:52:C4:69:B8/#");
      Serial.println("Connect Success");
      client.publish("3A:34:52:C4:69:B8/connection", "connected");
      if (led_status == HIGH)
        client.publish("3A:34:52:C4:69:B8/status", "HIGH");
      else
        client.publish("3A:34:52:C4:69:B8/status", "LOW");
    } else {
  
      Serial.print("failed, rc=");
      Serial.print(client.state());
      delay(1000);
    }
  }
}
int buttonState = 0; 
int lastButtonState = 0;
int outputState = 0;
void loop(){
  if (wifiMulti.run() != WL_CONNECTED)
    reconnectWifi();
  if (!client.connected() && wifiMulti.run() == WL_CONNECTED) {
    reconnect();
  }
  client.loop();

  buttonState = digitalRead(BTN_PIN); 
  if (buttonState == HIGH && lastButtonState == LOW) {
    outputState = 1; // Xung sườn lên được phát hiện
    Serial.print("Button is pressed");
    led_status = !led_status;
    if (led_status == HIGH)
        client.publish("3A:34:52:C4:69:B8/status", "HIGH");
      else
        client.publish("3A:34:52:C4:69:B8/status", "LOW");
  } else {
    outputState = 0; // Không có xung sườn lên
  }

  lastButtonState = buttonState;

  digitalWrite(LED_PIN, led_status);
  delay(1000);
}

