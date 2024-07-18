#include <mqttConfig.h>

// Cấu hình UART
HardwareSerial mySerial(1); // UART 1

// Địa chỉ MQTT broker
const char *mqtt_server = "192.168.1.13";
const char *mqttUser = "";
const char *mqttPassword = "";
const char *relay_topic = "/test";
const char *config_topic = "/mqttconfig";
char default_id[11];

const int detectionThreshold = 5; // Ngưỡng phát hiện liên tiếp
int detectionCount = 0;
int noDetectionCount = 0;
const int noDetectionThreshold = 5; // Ngưỡng không phát hiện liên tiếp

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
    randomString[length] = '\0'; // Đảm bảo kết thúc chuỗi với ký tự null

    return randomString;
}

void mqttConfig()
{
    client.publish(config_topic, default_id);
}
