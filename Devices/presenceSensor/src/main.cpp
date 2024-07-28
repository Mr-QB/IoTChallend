#include <mqttConfig.h>

void setup()
{
  Serial.begin(115200);
  mySerial.begin(9600, SERIAL_8N1, RX_PIN, TX_PIN); // Configure UART1 to 9600
  Serial.println("Checking LD2410C presence sensor");
  strcpy(default_id, generateRandomString(10));

  // Read relay_topic value from EEPROM
  EEPROM.begin(EEPROM_SIZE);
  readFromEEPROM();

  // Check UART
  if (mySerial)
  {
    Serial.println("UART1 successfully started");
  }
  else
  {
    Serial.println("Failed to start UART1");
  }

  // Start WiFiManager
  WiFiManager wifiManager;

  // Clear previous WiFi connection information
  // wifiManager.resetSettings();

  // Start automatic WiFi connection
  wifiManager.autoConnect("RCUET-Config");

  Serial.println("WiFi connected successfully!");

  // Configure MQTT
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop()
{
  Serial.println(relay_topic);
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
    Serial.print("Data from LD2410C: ");
    Serial.println(data);

    // Process data from LD2410C
    data.trim();

    // Check for presence
    if (data.indexOf("i") != -1)
    {
      detectionCount++;
      noDetectionCount = 0; // Reset no detection counter

      if (noDetectionCount <= noDetectionThreshold)
      {
        Serial.println("Presence detected!");
        client.publish(relay_topic, "ON");
      }
    }
    else
    {
      detectionCount = 0; // Reset detection counter
      noDetectionCount++;

      if (noDetectionCount >= noDetectionThreshold)
      {
        detectionCount = 0; // Reset detection counter
        Serial.println("No presence detected.");
        client.publish(relay_topic, "OFF");
      }
    }
  }
  else
  {
    Serial.println("No data from LD2410C");
  }
  delay(1000);
}
