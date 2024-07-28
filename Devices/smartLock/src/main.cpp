#include <Arduino.h>
#include <Config.h>

WiFiClient espClient;
PubSubClient client(espClient);

void openDoor()
{
  digitalWrite(Relay_PIN, HIGH);
  // sentMqtt("opened");
  delay(5000); // Latch open for 5 seconds
  // sentMqtt("closed");
  digitalWrite(Relay_PIN, LOW); // Close the latch
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
    delay(2000);   // Wait 2 seconds
    resetScreen(); // Reset the screen to ready state
    // Perform actions when the door is opened
  }

  else if (message.equals("closed"))
  {
    Serial.println("Door is closed!");
    // Perform actions when the door is closed
  }
  else
  {
    Serial.println("Unknown message received.");
    // Handle other cases
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
  lcdPrintCentered("Reset Password", 0);
  Serial.println("Reset Password");
}

void resetScreen()
{
  lcd.clear();
  lcdPrintCentered("Ready", 0);
}

void savePasswordToEEPROM(String password)
{
  int len = password.length();
  EEPROM.write(EEPROM_ADDRESS, len); // Write password length to EEPROM
  for (int i = 0; i < len; i++)
  {
    EEPROM.write(EEPROM_ADDRESS + 1 + i, password[i]); // Write each password character to EEPROM
  }
  EEPROM.commit(); // Commit data to EEPROM
}

String readPasswordFromEEPROM()
{
  int len = EEPROM.read(EEPROM_ADDRESS); // Read password length from EEPROM
  String password = "";
  for (int i = 0; i < len; i++)
  {
    password += char(EEPROM.read(EEPROM_ADDRESS + 1 + i)); // Read each password character from EEPROM
  }
  return password;
}

void setup()
{
  Serial.begin(9600); // Initialize Serial with baud rate 9600
  SPI.begin();        // Initialize SPI bus
  mfrc522.PCD_Init(); // Initialize MFRC522

  EEPROM.begin(512);                          // Initialize EEPROM with 512 bytes capacity
  correctPassword = readPasswordFromEEPROM(); // Read password from EEPROM

  pinMode(Relay_PIN, OUTPUT);
  digitalWrite(Relay_PIN, LOW);

  pinMode(BUZZER_PIN, OUTPUT);   // Set buzzer pin as OUTPUT
  digitalWrite(BUZZER_PIN, LOW); // Turn off the buzzer initially

  lcd.init();                   // Initialize LCD
  lcd.backlight();              // Turn on LCD backlight
  lcd.clear();                  // Clear the screen
  lcdPrintCentered("Ready", 0); // Display "Ready" in the center when the system is ready

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
  Serial.println("Access granted");
  lcd.clear();
  lcdPrintCentered("Access granted", 0);

  // digitalWrite(BUZZER_PIN, HIGH); // Turn on the buzzer
  delay(500);                    // Wait 0.5 seconds
  digitalWrite(BUZZER_PIN, LOW); // Turn off the buzzer

  openDoor();
  delay(2000);   // Wait 2 seconds
  resetScreen(); // Reset the screen to ready state
}

void handleAccessDenied()
{
  Serial.println("Access denied");
  lcd.clear();
  lcdPrintCentered("Access denied", 0);
}

void checkRFIDCard() // Handle the card
{
  // Check if there is any card present near the RC522
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

    mfrc522.PICC_HaltA(); // Halt card reading
  }
}

void handleKeypadInput(char key)
{
  if (key)
  {
    // Serial.println(key);
    lcd.clear();
    lcdPrintCentered("Enter Password:", 0);

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
            lcdPrintCentered("Old Password OK", 0);
            Serial.println("Old password correct");
            enteredPassword = "";
          }
          else
          {
            lcd.clear();
            lcdPrintCentered("Wrong Old Password", 0);
            Serial.println("Wrong old password");
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
              savePasswordToEEPROM(correctPassword); // Save new password to EEPROM
              lcd.clear();
              lcdPrintCentered("Password Changed OK", 0);
              Serial.println("Password changed successfully");
              isChangingPassword = false;
              confirmNewPassword = false;
              oldPasswordConfirmed = false;
              enteredPassword = "";
              newPassword = "";
            }
            else
            {
              lcd.clear();
              lcdPrintCentered("Does Not Match", 0);
              Serial.println("Does not match");
              enteredPassword = "";
              confirmNewPassword = true;
            }
          }
          else
          {
            newPassword = enteredPassword;
            enteredPassword = "";
            lcd.clear();
            lcdPrintCentered("Re-enter Password", 0);
            Serial.println("Re-enter password");
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
        lcdPrintCentered("Enter Old Password:", 0);
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
        Serial.print("Enter Password: ");
        Serial.println(enteredPassword);
        Serial.print("Correct Password: ");
        Serial.println(correctPassword);

        if (enteredPassword == correctPassword)
        {
          Serial.println("Correct password");
          lcd.clear();
          lcdPrintCentered("Correct Password", 0);

          // digitalWrite(BUZZER_PIN, HIGH); // Turn on the buzzer
          delay(500);                    // Wait 0.5 seconds
          digitalWrite(BUZZER_PIN, LOW); // Turn off the buzzer
          openDoor();

          delay(2000);   // Wait 2 seconds
          resetScreen(); // Reset the screen to ready state
        }
        else
        {
          Serial.println("Wrong password");
          lcd.clear();
          lcdPrintCentered("Wrong Password", 0);
        }
        enteredPassword = "";
      }
      else
      {
        enteredPassword += key;
      }
    }

    // Print password
    String maskedPassword = "";
    for (int i = 0; i < enteredPassword.length(); i++)
    {
      maskedPassword += "*";
    }
    lcd.setCursor((16 - maskedPassword.length()) / 2, 1);
    lcd.print(maskedPassword);
  }
}

void loop()
{
  if (!client.connected())
  {
    String client_id = "lk";
    client_id += String(WiFi.macAddress());
    Serial.printf("The client %s connects to the public MQTT broker\n", client_id.c_str());
    while (!client.connected())
    {
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
  }
  client.loop();
  checkRFIDCard(); // Check for RFID card input
  char key = keypad.getKey();
  if (key)
  {
    handleKeypadInput(key); // Check for keypad input
  }
  // Regularly send lock status via MQTT
  sentMqtt(digitalRead(Relay_PIN) == HIGH ? "opened" : "closed");
}