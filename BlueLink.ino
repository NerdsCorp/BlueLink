/*
  BlueLink Arduino Firmware
  Version: 1.0
  Author: NerdsCorp
  Description:
    - Receives controller input commands over Serial
    - Maps them to Arduino pins (digital/analog)
    - Responds with status messages for UI
*/

#include <Arduino.h>

// -----------------------------
// CONFIGURATION
// -----------------------------

// Maximum number of digital pins we can control
const int MAX_DIGITAL_PINS = 14; // Arduino Uno digital pins 0-13
const int MAX_ANALOG_PINS = 6;   // A0-A5

// Define arrays for pin modes (0 = unused, 1 = digital, 2 = analog)
int pinModeMapping[MAX_DIGITAL_PINS + MAX_ANALOG_PINS] = {0};

// -----------------------------
// HELPERS
// -----------------------------

void sendStatus(const String &message) {
  Serial.println("STATUS:" + message); // prefixed for frontend parsing
}

void setPinValue(int pin, int value) {
  if (pin < MAX_DIGITAL_PINS) {
    digitalWrite(pin, value > 0 ? HIGH : LOW);
  } else {
    int analogPin = pin - MAX_DIGITAL_PINS;
    if (analogPin < MAX_ANALOG_PINS) {
      analogWrite(analogPin + A0, value);
    }
  }
}

// -----------------------------
// SETUP
// -----------------------------
void setup() {
  Serial.begin(115200);
  sendStatus("Arduino Initialized");

  // Set default pin modes
  for (int i = 0; i < MAX_DIGITAL_PINS; i++) {
    pinMode(i, OUTPUT);
    digitalWrite(i, LOW);
  }
  for (int i = 0; i < MAX_ANALOG_PINS; i++) {
    pinMode(A0 + i, OUTPUT);
    analogWrite(A0 + i, 0);
  }
}

// -----------------------------
// MAIN LOOP
// -----------------------------
void loop() {
  if (Serial.available() > 0) {
    String line = Serial.readStringUntil('\n');
    line.trim();

    // Expected format from BlueLink backend:
    // SET:<pin>:<value>    e.g. SET:5:1   -> digital pin 5 HIGH
    // TEST:<pin>           e.g. TEST:3    -> toggle pin 3 for testing
    // INFO                 -> return pin mapping info
    if (line.startsWith("SET:")) {
      int firstColon = line.indexOf(':');
      int secondColon = line.indexOf(':', firstColon + 1);
      int pin = line.substring(firstColon + 1, secondColon).toInt();
      int value = line.substring(secondColon + 1).toInt();
      setPinValue(pin, value);
      sendStatus("SET PIN " + String(pin) + " TO " + String(value));
    } else if (line.startsWith("TEST:")) {
      int colon = line.indexOf(':');
      int pin = line.substring(colon + 1).toInt();
      // simple blink for test
      setPinValue(pin, 1);
      delay(200);
      setPinValue(pin, 0);
      sendStatus("TESTED PIN " + String(pin));
    } else if (line.equals("INFO")) {
      String info = "PINS:";
      for (int i = 0; i < MAX_DIGITAL_PINS; i++) info += String(i) + ",";
      for (int i = 0; i < MAX_ANALOG_PINS; i++) info += "A" + String(i) + ",";
      sendStatus(info);
    } else {
      sendStatus("UNKNOWN COMMAND: " + line);
    }
  }
}
