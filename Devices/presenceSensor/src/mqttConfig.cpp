#include <mqttConfig.h>

// Cấu hình UART
HardwareSerial mySerial(1); // UART 1

// Địa chỉ MQTT broker
const char *mqtt_server = "192.168.1.13";
const char *mqttUser = "";
const char *mqttPassword = "";
char relay_topic[50] = "/test";
const char *config_topic = "/mqttconfig";
char default_id[11];
bool setup_mqtt_done = false;

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
            client.subscribe(default_id);
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
    // Chuyển payload thành chuỗi để xử lý
    payload[length] = '\0';
    String message = String((char *)payload);

    Serial.println(topic);
    Serial.println(message);
    // Kiểm tra nếu topic là "abc"
    if (strcmp(topic, default_id) == 0)
    {
        strncpy(relay_topic, message.c_str(), sizeof(relay_topic) - 1);
        relay_topic[sizeof(relay_topic) - 1] = '\0'; // Đảm bảo kết thúc chuỗi

        // Lưu relay_topic vào EEPROM
        writeToEEPROM();

        setup_mqtt_done = true;
    }
    else
    {
        // Nếu không phải topic "abc", bạn có thể xử lý các trường hợp khác ở đây
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
    // Đọc dữ liệu từ EEPROM vào biến relay_topic
    EEPROM.get(EEPROM_ADDRESS, relay_topic);
    Serial.print("Read relay_topic from EEPROM: ");
    Serial.println(relay_topic);
}

void writeToEEPROM()
{
    // Ghi giá trị relay_topic vào EEPROM
    EEPROM.put(EEPROM_ADDRESS, relay_topic);
    EEPROM.commit(); // Lưu thay đổi vào EEPROM
    Serial.print("Wrote relay_topic to EEPROM: ");
    Serial.println(relay_topic);
}
