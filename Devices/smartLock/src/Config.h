#include <Arduino.h>
#include <Lib.h>

#define RST_PIN 4     // GPIO4 for RESET pin of RC522
#define SS_PIN 5      // GPIO5 for SS (Slave Select) pin of RC522
#define BUZZER_PIN 15 // GPIO15 for buzzer
#define Relay_PIN 2   // GPIO2 for relay
#define EEPROM_ADDRESS 0

MFRC522 mfrc522(SS_PIN, RST_PIN);   // Initialize MFRC522
LiquidCrystal_I2C lcd(0x27, 16, 2); // LCD address is 0x27, size 16x2

// Array to store accepted UIDs
String accepted_UIDs[] = {"B1B9DB1D", "5371AFFE"};
const int num_accepted_UIDs = 2; // Number of accepted UIDs

const byte ROWS = 4; // Number of rows in the keypad
const byte COLS = 4; // Number of columns in the keypad
char keys[ROWS][COLS] = {
    {'1', '2', '3', 'A'},
    {'4', '5', '6', 'B'},
    {'7', '8', '9', 'C'},
    {'*', '0', '#', 'D'}};
byte rowPins[ROWS] = {13, 12, 14, 27}; // Define pins for the rows
byte colPins[COLS] = {26, 25, 33, 32}; // Define pins for the columns
Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

String correctPassword = "1234";   // Correct password
String enteredPassword = "";       // Variable to store entered password
String newPassword = "";           // Variable to store new password
bool isChangingPassword = false;   // Variable to check if changing password
bool confirmNewPassword = false;   // Variable to confirm new password
bool oldPasswordConfirmed = false; // Variable to confirm old password

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
