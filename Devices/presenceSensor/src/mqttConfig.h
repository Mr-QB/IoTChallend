#ifndef MQTTCONFIG_H
#define MQTTCONFIG_H

#include <EEPROM.h>
#include <HardwareSerial.h>
#include <string>
#include <cstdlib>
#include <ctime>
#include <PubSubClient.h>
#include <WiFi.h>
#include <WiFiManager.h>

extern HardwareSerial mySerial;
extern const char *mqtt_server;
extern const char *mqttUser;
extern const char *mqttPassword;
extern char relay_topic[50];
extern const char *config_topic;
extern const int detectionThreshold;
extern int detectionCount;
extern int noDetectionCount;
extern const int noDetectionThreshold;
extern char default_id[11];
extern bool setup_mqtt_done;

// extern char devices_id[11];
extern WiFiClient espClient;
extern PubSubClient client;
#define RX_PIN 33
#define TX_PIN 18
#define EEPROM_SIZE 512
#define EEPROM_ADDRESS 0

char *generateRandomString(size_t length);
void mqttConfig();
void reconnect();
void callback(char *topic, byte *payload, unsigned int length);
void readFromEEPROM();
void writeToEEPROM();

#endif // MQTTCONFIG_H