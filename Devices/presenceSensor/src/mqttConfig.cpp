#include <mqttConfig.h>

// Configure UART
HardwareSerial mySerial(1); // UART 1

// MQTT broker address
const char *mqtt_server = "192.168.1.13";
const char *mqttUser = "";
const char *mqttPassword = "";
char relay_topic[50] = "/test";
const char *config_topic = "/mqttconfig";
char default_id[11];
bool setup_mqtt_done = false;

const int detectionThreshold = 5; // Consecutive detection threshold
int detectionCount = 0;
int noDetectionCount = 0;
const int noDetectionThreshold = 5; // Consecutive no detection threshold

WiFiClient espClient;
PubSubClient client(espClient);

char *generateRandomString(size_t length)
{
    const char charset[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    const size_t max_index = (sizeof(charset) - 1);
    char *randomString = new char[length + 1];

    for (size_t i = 0; i < length; ++i)
    {
        randomString[i] = charset[rand() % max_index];
    }
    randomString[length] = '\0'; // Ensure the string ends with a null character

    return randomString;
}

void reconnect()
{
    while (!client.connected())
    {
        Serial.print("Attempting MQTT connection...");
        if (client.connect("ESP32Client", mqttUser, mqttPassword))
        {
            Serial.println("Connected");
            // Subscribe if needed
            client.subscribe(relay_topic);
            client.subscribe(default_id);
        }
        else
        {
            Serial.print("Failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds");
            delay(5000);
        }
    }
}

void callback(char *topic, byte *payload, unsigned int length)
{
    // Convert payload to string for processing
    payload[length] = '\0';
    String message = String((char *)payload);

    Serial.println(topic);
    Serial.println(message);
    // Check if topic is "abc"
    if (strcmp(topic, default_id) == 0)
    {
        strncpy(relay_topic, message.c_str(), sizeof(relay_topic) - 1);
        relay_topic[sizeof(relay_topic) - 1] = '\0'; // Ensure the string ends with a null character

        // Save relay_topic to EEPROM
        writeToEEPROM();

        setup_mqtt_done = true;
    }
    else
    {
        // If not topic "abc", handle other cases here
        Serial.print("Received message on topic '");
        Serial.print(topic);
        Serial.print("': ");
        Serial.println(message);
    }
}

void mqttConfig()
{
    if (!setup_mqtt_done)
    {
        client.publish(config_topic, default_id);
    }
}

void readFromEEPROM()
{
    // Read data from EEPROM into relay_topic variable
    EEPROM.get(EEPROM_ADDRESS, relay_topic);
    Serial.print("Read relay_topic from EEPROM: ");
    Serial.println(relay_topic);
}

void writeToEEPROM()
{
    // Write relay_topic value to EEPROM
    EEPROM.put(EEPROM_ADDRESS, relay_topic);
    EEPROM.commit(); // Save changes to EEPROM
    Serial.print("Wrote relay_topic to EEPROM: ");
    Serial.println(relay_topic);
}