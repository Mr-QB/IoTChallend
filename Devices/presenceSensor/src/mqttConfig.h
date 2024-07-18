#ifndef MQTTCONFIG_H
#define MQTTCONFIG_H

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
extern const char *relay_topic;
extern const char *config_topic;
extern const int detectionThreshold;
extern int detectionCount;
extern int noDetectionCount;
extern const int noDetectionThreshold;
extern char default_id[11];
extern WiFiClient espClient;
extern PubSubClient client;
#define RX_PIN 33
#define TX_PIN 18

char *generateRandomString(size_t length);
void mqttConfig();

#endif // MQTTCONFIG_H