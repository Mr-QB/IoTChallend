#include <SPI.h>
#include <MFRC522.h>
#include <Keypad.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <EEPROM.h>
#include <string>
#include <WiFi.h>
#include <PubSubClient.h>


void openDoor();
void callback(char *topic, byte *payload, unsigned int length);
void lcdPrintCentered(String text, int row);
void resetPassword();
void resetScreen();
void savePasswordToEEPROM(String password);
String readPasswordFromEEPROM();
void sentMqtt(String lock_satus);
void handleAccessGranted();
void handleAccessDenied();
void checkRFIDCard();
void handleKeypadInput(char key);