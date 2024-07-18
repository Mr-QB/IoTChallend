#include <Arduino.h>
#include <Config.h>

WiFiClient espClient;
PubSubClient client(espClient);

void openDoor()
{
  digitalWrite(Relay_PIN, HIGH);
  // sentMqtt("opened");
  delay(5000); // Chốt mở trong 5 giây
  // sentMqtt("closed");
  digitalWrite(Relay_PIN, LOW); // Đóng chốt
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
    // Thực hiện các thao tác khi cửa được mở
  }

  else if (message.equals("closed"))
  {
    Serial.println("Door is closed!");
    // Thực hiện các thao tác khi cửa được đóng
  }
  else
  {
    Serial.println("Unknown message received.");
    // Xử lý các trường hợp khác
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

void setup()
{
  Serial.begin(9600); // Khởi tạo Serial với baud rate 9600
  SPI.begin();        // Khởi tạo SPI bus
  mfrc522.PCD_Init(); // Khởi tạo MFRC522

  EEPROM.begin(512);                          // Khởi tạo EEPROM với dung lượng 512 byte
  correctPassword = readPasswordFromEEPROM(); // Đọc mật khẩu từ EEPROM

  pinMode(Relay_PIN, OUTPUT);
  digitalWrite(Relay_PIN, LOW);

  pinMode(BUZZER_PIN, OUTPUT);   // Đặt chân còi là OUTPUT
  digitalWrite(BUZZER_PIN, LOW); // Tắt còi ban đầu

  lcd.init();                      // Khởi tạo LCD
  lcd.backlight();                 // Bật đèn nền LCD
  lcd.clear();                     // Xóa màn hình
  lcdPrintCentered("San sang", 0); // Hiển thị "San sang" khi hệ thống sẵn sàng ở giữa màn hình

  // Mqtt setup
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Am Loop.....");
  Serial.println("Connected to the Wi-Fi network");
  // connecting to a mqtt broker
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);
  while (!client.connected())
  {
    String client_id = "lk";
    client_id += String(WiFi.macAddress());
    Serial.printf("The client %s connects to the public MQTT broker\n", client_id.c_str());
    if (client.connect(client_id.c_str(), mqtt_username, mqtt_password))
    {
      Serial.println("Public EMQX MQTT broker connected");
    }
    else
    {
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
    }
  }
  // Publish and subscribe
  // client.publish(topic, "Hi, i running.....");
  client.subscribe(topic_);
}

void sentMqtt(String lock_satus)
{
  static unsigned long lastMillis = 0;
  unsigned long currentMillis = millis();
  if (currentMillis - lastMillis >= 1000)
  {
    lastMillis = currentMillis;
    client.publish(topic_, lock_satus.c_str());
  }
}

void handleAccessGranted()
{
  Serial.println("Truy cap duoc chap nhan");
  lcd.clear();
  lcdPrintCentered("Truy cap hop le", 0);

  // digitalWrite(BUZZER_PIN, HIGH); // Bật còi
  delay(500);                    // Chờ 0,5 giây
  digitalWrite(BUZZER_PIN, LOW); // Tắt còi

  openDoor();
  delay(2000);   // Chờ 2 giây
  resetScreen(); // Reset màn hình về trạng thái sẵn sàng
}

void handleAccessDenied()
{
  Serial.println("Truy cap bi tu choi");
  lcd.clear();
  lcdPrintCentered("Truy cap bi tu choi", 0);
}

void checkRFIDCard() // Xử lý thẻ
{
  // Kiểm tra xem có thẻ nào được đặt gần RC522 hay không
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial())
  {
    String content = "";
    for (byte i = 0; i < mfrc522.uid.size; i++)
    {
      content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : ""));
      content.concat(String(mfrc522.uid.uidByte[i], HEX));
    }
    content.toUpperCase();
    Serial.println(content);

    bool access_granted = false;
    for (int i = 0; i < num_accepted_UIDs; i++)
    {
      if (content.equals(accepted_UIDs[i]))
      {
        access_granted = true;
        break;
      }
    }

    if (access_granted)
    {
      handleAccessGranted();
    }
    else
    {
      handleAccessDenied();
    }

    mfrc522.PICC_HaltA(); // Tạm ngừng việc đọc thẻ
  }
}

void handleKeypadInput(char key)
{
  if (key)
  {
    // Serial.println(key);
    lcd.clear();
    lcdPrintCentered("Nhan mat khau:", 0);

    lcd.setCursor(0, 1);
    // Serial.println(maskedPasswordString.c_str);

    if (isChangingPassword)
    {
      if (!oldPasswordConfirmed)
      {
        if (key == 'A')
        {
          if (enteredPassword == correctPassword)
          {
            oldPasswordConfirmed = true;
            lcd.clear();
            lcdPrintCentered("Mat khau cu OK", 0);
            Serial.println("Mat khau cu dung");
            enteredPassword = "";
          }
          else
          {
            lcd.clear();
            lcdPrintCentered("Sai mat khau cu", 0);
            Serial.println("Sai mat khau cu");
            isChangingPassword = false;
            oldPasswordConfirmed = false;
            enteredPassword = "";
          }
        }
        else
        {
          enteredPassword += key;
        }
      }
      else
      {
        if (key == 'A')
        {
          if (confirmNewPassword)
          {
            if (enteredPassword == newPassword)
            {
              correctPassword = newPassword;
              savePasswordToEEPROM(correctPassword); // Lưu mật khẩu mới vào EEPROM
              lcd.clear();
              lcdPrintCentered("Doi mat khau OK", 0);
              Serial.println("Doi mat khau thanh cong");
              isChangingPassword = false;
              confirmNewPassword = false;
              oldPasswordConfirmed = false;
              enteredPassword = "";
              newPassword = "";
            }
            else
            {
              lcd.clear();
              lcdPrintCentered("Khong trung khop", 0);
              Serial.println("Khong trung khop");
              enteredPassword = "";
              confirmNewPassword = true;
            }
          }
          else
          {
            newPassword = enteredPassword;
            enteredPassword = "";
            lcd.clear();
            lcdPrintCentered("Nhap lai mat khau", 0);
            Serial.println("Nhap lai mat khau");
            confirmNewPassword = true;
          }
        }
        else
        {
          enteredPassword += key;
        }
      }
    }
    else
    {
      if (key == 'C')
      {
        isChangingPassword = true;
        lcd.clear();
        lcdPrintCentered("Nhap mat khau cu:", 0);
        enteredPassword = "";
        newPassword = "";
        oldPasswordConfirmed = false;
        confirmNewPassword = false;
      }
      else if (key == 'D')
      {
        if (enteredPassword.length() > 0)
        {
          enteredPassword.remove(enteredPassword.length() - 1);
        }
      }
      else if (key == 'A')
      {
        Serial.print("Nhap mat khau: ");
        Serial.println(enteredPassword);
        Serial.print("Mat khau dung: ");
        Serial.println(correctPassword);

        if (enteredPassword == correctPassword)
        {
          Serial.println("Mat khau dung");
          lcd.clear();
          lcdPrintCentered("Mat khau dung", 0);

          // digitalWrite(BUZZER_PIN, HIGH); // Bật còi
          delay(500);                    // Chờ 0,5 giây
          digitalWrite(BUZZER_PIN, LOW); // Tắt còi
          openDoor();

          delay(2000);   // Chờ 2 giây
          resetScreen(); // Reset màn hình về trạng thái sẵn sàngd
        }
        else
        {
          Serial.println("Sai mat khau");
          lcd.clear();
          lcdPrintCentered("Sai mat khau", 0);
        }
        enteredPassword = ""; // Đặt lại biến lưu trữ mật khẩu đã nhập
      }
      else
      {
        enteredPassword += key;
      }
    }
    std::string maskedPassword(enteredPassword.length(), '*');
    std::string maskedPasswordString = maskedPassword;

    if (enteredPassword.length() > 1)
    {
      std::string maskedPassword(enteredPassword.length() - 1, '*');
      maskedPasswordString = maskedPassword + enteredPassword[enteredPassword.length() - 1];
    }
    lcdPrintCentered(maskedPasswordString.c_str(), 1); // In dấu * thay vì ký tự thực tế
  }
}

void loop()
{
  client.loop();
  checkRFIDCard();
  char key = keypad.getKey();
  handleKeypadInput(key);
}
