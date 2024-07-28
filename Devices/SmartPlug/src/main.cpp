#include <Arduino.h>
#include <WiFi.h> // WiFi library for ESP32
#include <PubSubClient.h>
#include <WiFiManager.h> // WiFiManager library
#include <WiFiClientSecure.h>

int relayPin1 = 26; // Use GPIO 26 for relay 1
int relayPin2 = 27; // Use GPIO 27 for relay 2

const char *mqtt_server = "192.168.0.118";
const char *mqttUser = "";
const char *mqttPassword = "";

WiFiClient espClient; // Use WiFiClientSecure for SSL/TLS
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
  // Try to reconnect to MQTT until successful
  while (!client.connected())
  {
    Serial.print("Attempting MQTT connection...");
    // Connect using login credentials
    if (client.connect("ESP32Client___", mqttUser, mqttPassword))
    {
      Serial.println("connected");
      // Subscribe to MQTT topic to receive control commands
      client.subscribe("/plug");
    }
    else
    {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup()
{
  // Declare relay control pins
  pinMode(relayPin1, OUTPUT);
  pinMode(relayPin2, OUTPUT);

  // Start Serial communication
  Serial.begin(9600);

  // Start WiFiManager
  WiFiManager wifiManager;

  // Configure to allow WiFi connection
  wifiManager.autoConnect("RCUET-Config");

  // Print WiFi connection information
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // Set up ESPClient for insecure communication (without valid SSL certificate)
  // espClient.setInsecure();

  // Set up MQTT client
  client.setServer(mqtt_server, 1883); // Use port 1883 for non
