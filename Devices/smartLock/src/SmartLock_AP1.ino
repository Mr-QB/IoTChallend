#include <Arduino.h>
#include <MFRC522.h>
#include <LiquidCrystal_I2C.h>
#include <Keypad.h>
#include <WiFiManager.h>
#include <PubSubClient.h>
#include <EEPROM.h>

#define RST_PIN 4       // GPIO4 cho chân RESET của RC522
#define SS_PIN 5        // GPIO5 cho chân SS (Slave Select) của RC522
#define BUZZER_PIN 15   // GPIO15 cho còi
#define RELAY_PIN 2     // GPIO2 cho relay
#define EEPROM_ADDRESS 0

MFRC522 mfrc522(SS_PIN, RST_PIN);     // Khởi tạo MFRC522
LiquidCrystal_I2C lcd(0x27, 16, 2);   // Địa chỉ LCD là 0x27, kích thước 16x2

// Mảng lưu trữ các UID được chấp nhận
String accepted_UIDs[] = {"B1B9DB1D", "5371AFFE"};
const int num_accepted_UIDs = 2; // Số lượng UID được chấp nhận

// Định nghĩa các chân cho Keypad
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

// MQTT Broker mqtt_broker, mqtt_port
const char* mqtt_broker = "mqttvcloud.innoway.vn";
const char* mqtt_username = "test";
const char* mqtt_password = "hCF0hcIxWi5wXK4f7N7hp3spM8lpHDmd";
const char *topic_ = "/lock";
const int mqtt_port = 1883;
const char *topic_config = "/configtopic";

// Khai báo biến trạng thái khóa
String lock_status_new = "open";
String lock_status_old = "open";

// Khởi tạo đối tượng WiFi, MQTT và WebServer
WiFiClient espClient;
PubSubClient client(espClient);

// Biến đếm số lần nhập sai
int incorrectAttempts = 0;

void openDoor()
{
  digitalWrite(RELAY_PIN, HIGH);
  delay(5000); // Chốt mở trong 5 giây
  digitalWrite(RELAY_PIN, LOW); // Đóng chốt
}

void callback(char *topic, byte *payload, unsigned int length)
{
  String message = "";
  for (int i = 0; i < length; i++)
  {
    message += (char)payload[i];
  }
  Serial.println(message.c_str());
  if (message.equals("opened"))
  {
    openDoor();
    delay(2000);   // Chờ 2 giây
    resetScreen(); // Reset màn hình về trạng thái sẵn sàng
  }
  else if (message.equals("closed"))
  {
    Serial.println("Door is closed!");
  }
  else
  {
    Serial.println("Unknown message received.");
  }
}

void lcdPrintCentered(String text, int row)
{
  int paddingSize = (16 - text.length()) / 2;
  lcd.setCursor(paddingSize, row);
  lcd.print(text);
}

void resetPassword()
{
  enteredPassword = "";
  lcd.clear();
  lcdPrintCentered("Dat lai mat khau", 0);
  Serial.println("Dat lai mat khau");
}

void resetScreen()
{
  lcd.clear();
  lcdPrintCentered("San sang", 0);
}

void savePasswordToEEPROM(String password)
{
  int len = password.length();
  EEPROM.write(EEPROM_ADDRESS, len); // Ghi độ dài mật khẩu vào EEPROM
  for (int i = 0; i < len; i++)
  {
    EEPROM.write(EEPROM_ADDRESS + 1 + i, password[i]); // Ghi từng ký tự mật khẩu vào EEPROM
  }
  EEPROM.commit(); // Commit dữ liệu vào EEPROM
}

String readPasswordFromEEPROM()
{
  int len = EEPROM.read(EEPROM_ADDRESS); // Đọc độ dài mật khẩu từ EEPROM
  String password = "";
  for (int i = 0; i < len; i++)
  {
    password += char(EEPROM.read(EEPROM_ADDRESS + 1 + i)); // Đọc từng ký tự mật khẩu từ EEPROM
  }
  return password;
}

void handleIncorrectAccess()
{
  if (incorrectAttempts >= 5)
  {
    // Còi kêu liên tục nếu nhập sai quá 5 lần
    while (true)
    {
      digitalWrite(BUZZER_PIN, HIGH);
      delay(500);
      digitalWrite(BUZZER_PIN, LOW);
      delay(500);
    }
  }
  else
  {
    // Còi kêu 2 lần cho lỗi mật khẩu hoặc thẻ không hợp lệ
    for (int i = 0; i < 2; i++)
    {
      digitalWrite(BUZZER_PIN, HIGH);
      delay(500);
      digitalWrite(BUZZER_PIN, LOW);
      delay(500);
    }
    incorrectAttempts++;
  }
}

void processInvalidCard()
{
  digitalWrite(BUZZER_PIN, HIGH);
  delay(500);
  digitalWrite(BUZZER_PIN, LOW);
  lcd.clear();
  lcdPrintCentered("The khong hop le", 0);
  resetScreen();
  handleIncorrectAccess();
}

void setup()
{
  Serial.begin(9600); // Khởi tạo Serial với baud rate 9600
  SPI.begin();        // Khởi tạo SPI bus
  mfrc522.PCD_Init(); // Khởi tạo MFRC522

  EEPROM.begin(512);                          // Khởi tạo EEPROM với dung lượng 512 byte
  correctPassword = readPasswordFromEEPROM(); // Đọc mật khẩu từ EEPROM

  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);

  pinMode(BUZZER_PIN, OUTPUT);   // Đặt chân còi là OUTPUT
  digitalWrite(BUZZER_PIN, LOW); // Tắt còi ban đầu

  lcd.init();                      // Khởi tạo LCD
  lcd.backlight();                // Bật đèn nền LCD
  lcd.clear();                    // Xóa màn hình
  lcdPrintCentered("San sang", 0); // Hiển thị "San sang" khi hệ thống sẵn sàng ở giữa màn hình

  // Khởi tạo WiFiManager với cấu hình AP có mật khẩu
  WiFiManager wifiManager;
  WiFiManagerParameter custom_ssid("ssid", "SSID", "", 32);
  WiFiManagerParameter custom_password("password", "Password", "", 32);
  wifiManager.addParameter(&custom_ssid);
  wifiManager.addParameter(&custom_password);
  
  wifiManager.startConfigPortal("SmartLock_AP", "rcuet@2024"); // Tạo AP với mật khẩu "rcuet@2024"
  Serial.println("Connected to WiFi");

  // Hiển thị thông báo thành công trên LCD
  lcd.clear();
  lcdPrintCentered("Da ket noi WIfi", 0);
  delay(3000);
  resetScreen();

  // Connecting to MQTT broker
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);
  while (!client.connected())
  {
    String client_id = "lk";
    client_id += String(WiFi.macAddress());
    Serial.printf("The client %s connects to the public MQTT broker\n", client_id.c_str());
    if (client.connect(client_id.c_str(), mqtt_username, mqtt_password))
    {
      Serial.println("Public MQTT broker connected.");
      client.subscribe(topic_);
      client.subscribe(topic_config);
    }
    else
    {
      Serial.print("Failed to connect, status code = ");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void loop()
{
  client.loop();

  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial())
  {
    String cardUID = "";
    for (byte i = 0; i < mfrc522.uid.size; i++)
    {
      cardUID += String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
      cardUID += String(mfrc522.uid.uidByte[i], HEX);
    }
    cardUID.toUpperCase();

    bool isAccepted = false;
    for (int i = 0; i < num_accepted_UIDs; i++)
    {
      if (cardUID == accepted_UIDs[i])
      {
        isAccepted = true;
        break;
      }
    }

    if (isAccepted)
    {
      digitalWrite(BUZZER_PIN, HIGH);
      delay(400);
      digitalWrite(BUZZER_PIN, LOW);
      openDoor();
      delay(500);
      resetScreen();
      incorrectAttempts = 0; // Đặt lại số lần nhập sai
    }
    else
    {
      processInvalidCard();
    }
  }

  char key = keypad.getKey();
  if (key)
  {
    if (key == '#')
    {
      if (isChangingPassword)
      {
        if (oldPasswordConfirmed)
        {
          if (newPassword == enteredPassword)
          {
            savePasswordToEEPROM(newPassword);
            lcd.clear();
            lcdPrintCentered("Mat khau moi", 0);
            lcdPrintCentered("da duoc luu", 1);
            delay(1000);
            resetScreen();
            isChangingPassword = false;
            enteredPassword = "";
          }
          else
          {
            lcd.clear();
            lcdPrintCentered("Mat khau khong", 0);
            lcdPrintCentered("trung khop", 1);
            delay(1000);
            resetScreen();
            enteredPassword = "";
            newPassword = "";
          }
        }
        else
        {
          if (enteredPassword == correctPassword)
          {
            oldPasswordConfirmed = true;
            lcd.clear();
            lcdPrintCentered("Nhap mat khau", 0);
            lcdPrintCentered("moi", 1);
            enteredPassword = "";
            isChangingPassword = true;
          }
          else
          {
            lcd.clear();
            lcdPrintCentered("Mat khau cu sai", 0);
            delay(1000);
            resetScreen();
            enteredPassword = "";
            oldPasswordConfirmed = false;
          }
        }
      }
      else
      {
        if (enteredPassword == correctPassword)
        {
          digitalWrite(BUZZER_PIN, HIGH);
          delay(400);
          digitalWrite(BUZZER_PIN, LOW);
          openDoor();
          resetScreen();
          incorrectAttempts = 0; // Đặt lại số lần nhập sai
        }
        else
        {
          handleIncorrectAccess();
          lcd.clear();
          lcdPrintCentered("Mat khau sai", 0);
          delay(1000);
          resetScreen();
          enteredPassword = ""; // Xóa mật khẩu đã nhập
        }
      }
    }
    else if (key == 'D')
    {
      resetPassword();
      isChangingPassword = true;
      oldPasswordConfirmed = false;
    }
    else if (key == '*')
    {
      if (enteredPassword.length() > 0)
      {
        enteredPassword.remove(enteredPassword.length() - 1); // Xóa ký tự cuối cùng
        lcd.setCursor(0, 1);
        lcd.print(String(enteredPassword.length(), '*')); // Hiển thị dấu '*'
      }
    }
    else
    {
      if (isChangingPassword)
      {
        newPassword += key;
        lcd.setCursor(0, 1);
        lcd.print(String(newPassword.length(), '*')); // Hiển thị dấu '*'
      }
      else
      {
        enteredPassword += key;
        lcd.setCursor(0, 1);
        lcd.print(String(enteredPassword.length(), '*')); // Hiển thị dấu '*'
      }
    }
  }
}
