#include <Arduino.h>
#include <Lib.h>

#define RST_PIN 4     // GPIO4 cho chân RESET của RC522
#define SS_PIN 5      // GPIO5 cho chân SS (Slave Select) của RC522
#define BUZZER_PIN 15 // GPIO15 cho còi
#define Relay_PIN 2   // GPIO2 cho relay
#define EEPROM_ADDRESS 0

MFRC522 mfrc522(SS_PIN, RST_PIN);   // Khởi tạo MFRC522
LiquidCrystal_I2C lcd(0x27, 16, 2); // Địa chỉ LCD là 0x27, kích thước 16x2

// Mảng lưu trữ các UID được chấp nhận
String accepted_UIDs[] = {"B1B9DB1D", "5371AFFE"};
const int num_accepted_UIDs = 2; // Số lượng UID được chấp nhận

const byte ROWS = 4; // Số hàng của bảng mã số
const byte COLS = 4; // Số cột của bảng mã số
char keys[ROWS][COLS] = {
    {'1', '2', '3', 'A'},
    {'4', '5', '6', 'B'},
    {'7', '8', '9', 'C'},
    {'*', '0', '#', 'D'}};
byte rowPins[ROWS] = {13, 12, 14, 27}; // Định nghĩa các chân cho các hàng
byte colPins[COLS] = {26, 25, 33, 32}; // Định nghĩa các chân cho các cột
Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

String correctPassword = "1234";   // Mật khẩu đúng
String enteredPassword = "";       // Biến lưu trữ mật khẩu đã nhập
String newPassword = "";           // Biến lưu trữ mật khẩu mới
bool isChangingPassword = false;   // Biến để kiểm tra xem có đang thay đổi mật khẩu hay không
bool confirmNewPassword = false;   // Biến để xác nhận mật khẩu mới
bool oldPasswordConfirmed = false; // Biến để xác nhận mật khẩu cũ đã được nhập đúng

// WiFi
const char *ssid = "HBA";             // Enter your WiFi name
const char *password = "tamconsotam"; // Enter WiFi password

// MQTT Broker
const char *mqtt_broker = "192.168.0.118";
const char *topic_ = "/lock";
const char *mqtt_username = "";
const char *mqtt_password = "emqx";
const int mqtt_port = 1883;

const char *topic_config = "/configtopic";

String lock_satus_new = "open";
String lock_satus_old = "open";