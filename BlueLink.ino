/*
  BlueLink Arduino Firmware - Advanced
  Version: 2.0
  Author: NerdsCorp
  
  Features:
    - Digital pin control (HIGH/LOW)
    - PWM support for analog outputs
    - Stepper motor control (4-wire)
    - Servo support
    - Real-time command processing
*/

#include <Arduino.h>

// -----------------------------
// CONFIGURATION
// -----------------------------
const int MAX_DIGITAL_PINS = 14; // Arduino Uno pins 0-13
const int MAX_ANALOG_PINS = 6;   // A0-A5
const int BAUD_RATE = 115200;

// Stepper motor state
struct StepperMotor {
  int pins[4];
  int currentStep;
  int stepsPerRev;
  unsigned long lastStepTime;
  int stepDelay;
  bool active;
};

StepperMotor stepper;
const int STEPPER_SEQUENCE[8][4] = {
  {1, 0, 0, 0},
  {1, 1, 0, 0},
  {0, 1, 0, 0},
  {0, 1, 1, 0},
  {0, 0, 1, 0},
  {0, 0, 1, 1},
  {0, 0, 0, 1},
  {1, 0, 0, 1}
};

// -----------------------------
// HELPERS
// -----------------------------
void sendStatus(const String &message) {
  Serial.println("STATUS:" + message);
}

void setPinValue(int pin, int value) {
  if (pin >= 0 && pin < MAX_DIGITAL_PINS) {
    pinMode(pin, OUTPUT);
    digitalWrite(pin, value > 0 ? HIGH : LOW);
  }
}

void setPWMValue(int pin, int value) {
  // PWM pins on Uno: 3, 5, 6, 9, 10, 11
  if (pin == 3 || pin == 5 || pin == 6 || pin == 9 || pin == 10 || pin == 11) {
    pinMode(pin, OUTPUT);
    analogWrite(pin, constrain(value, 0, 255));
  } else {
    sendStatus("ERROR: Pin " + String(pin) + " does not support PWM");
  }
}

void initStepper(int pin1, int pin2, int pin3, int pin4, int stepsPerRev) {
  stepper.pins[0] = pin1;
  stepper.pins[1] = pin2;
  stepper.pins[2] = pin3;
  stepper.pins[3] = pin4;
  stepper.stepsPerRev = stepsPerRev;
  stepper.currentStep = 0;
  stepper.active = true;
  
  for (int i = 0; i < 4; i++) {
    pinMode(stepper.pins[i], OUTPUT);
    digitalWrite(stepper.pins[i], LOW);
  }
  
  sendStatus("Stepper initialized on pins " + String(pin1) + "," + String(pin2) + "," + String(pin3) + "," + String(pin4));
}

void stepMotor(int steps, int speed) {
  if (!stepper.active) {
    sendStatus("ERROR: Stepper not initialized");
    return;
  }
  
  // Calculate delay between steps (RPM to microseconds)
  int stepsPerSecond = (speed * stepper.stepsPerRev) / 60;
  int stepDelay = 1000000 / stepsPerSecond;
  
  int direction = (steps > 0) ? 1 : -1;
  steps = abs(steps);
  
  for (int i = 0; i < steps; i++) {
    // Get current step in sequence
    int stepIndex = stepper.currentStep % 8;
    
    // Set pins according to sequence
    for (int j = 0; j < 4; j++) {
      digitalWrite(stepper.pins[j], STEPPER_SEQUENCE[stepIndex][j]);
    }
    
    stepper.currentStep += direction;
    if (stepper.currentStep < 0) stepper.currentStep = 7;
    if (stepper.currentStep > 7) stepper.currentStep = 0;
    
    delayMicroseconds(stepDelay);
  }
  
  // Turn off all coils
  for (int i = 0; i < 4; i++) {
    digitalWrite(stepper.pins[i], LOW);
  }
  
  sendStatus("Moved " + String(steps) + " steps");
}

// Parse comma-separated values
void parseCSV(String input, int* values, int maxValues) {
  int index = 0;
  int startPos = 0;
  int commaPos = input.indexOf(',');
  
  while (commaPos >= 0 && index < maxValues) {
    values[index++] = input.substring(startPos, commaPos).toInt();
    startPos = commaPos + 1;
    commaPos = input.indexOf(',', startPos);
  }
  
  if (index < maxValues && startPos < input.length()) {
    values[index] = input.substring(startPos).toInt();
  }
}

// -----------------------------
// SETUP
// -----------------------------
void setup() {
  Serial.begin(BAUD_RATE);
  sendStatus("BlueLink Advanced Initialized");
  sendStatus("PWM pins: 3,5,6,9,10,11");
  
  // Initialize all digital pins as outputs (LOW)
  for (int i = 2; i < MAX_DIGITAL_PINS; i++) {
    pinMode(i, OUTPUT);
    digitalWrite(i, LOW);
  }
  
  stepper.active = false;
}

// -----------------------------
// MAIN LOOP
// -----------------------------
void loop() {
  if (Serial.available() > 0) {
    String line = Serial.readStringUntil('\n');
    line.trim();

    // Commands:
    // SET:<pin>:<value>              -> Digital write (0/1)
    // PWM:<pin>:<value>              -> PWM write (0-255)
    // TEST:<pin>                     -> Blink test
    // STEPPER:<p1>,<p2>,<p3>,<p4>:<steps>:<speed>  -> Control stepper
    // INFO                           -> Get info
    
    if (line.startsWith("SET:")) {
      int firstColon = line.indexOf(':');
      int secondColon = line.indexOf(':', firstColon + 1);
      int pin = line.substring(firstColon + 1, secondColon).toInt();
      int value = line.substring(secondColon + 1).toInt();
      
      setPinValue(pin, value);
      sendStatus("SET PIN " + String(pin) + " TO " + String(value));
      
    } else if (line.startsWith("PWM:")) {
      int firstColon = line.indexOf(':');
      int secondColon = line.indexOf(':', firstColon + 1);
      int pin = line.substring(firstColon + 1, secondColon).toInt();
      int value = line.substring(secondColon + 1).toInt();
      
      setPWMValue(pin, value);
      sendStatus("PWM PIN " + String(pin) + " TO " + String(value));
      
    } else if (line.startsWith("TEST:")) {
      int colon = line.indexOf(':');
      int pin = line.substring(colon + 1).toInt();
      
      setPinValue(pin, 1);
      delay(200);
      setPinValue(pin, 0);
      sendStatus("TESTED PIN " + String(pin));
      
    } else if (line.startsWith("STEPPER:")) {
      // Format: STEPPER:pin1,pin2,pin3,pin4:steps:speed
      int firstColon = line.indexOf(':');
      int secondColon = line.indexOf(':', firstColon + 1);
      int thirdColon = line.indexOf(':', secondColon + 1);
      
      String pinsStr = line.substring(firstColon + 1, secondColon);
      int steps = line.substring(secondColon + 1, thirdColon).toInt();
      int speed = line.substring(thirdColon + 1).toInt();
      
      // Parse pins
      int pins[4];
      parseCSV(pinsStr, pins, 4);
      
      // Initialize stepper if not already done
      if (!stepper.active || stepper.pins[0] != pins[0]) {
        initStepper(pins[0], pins[1], pins[2], pins[3], 200);
      }
      
      stepMotor(steps, speed);
      
    } else if (line.equals("INFO")) {
      sendStatus("DIGITAL_PINS:2-13");
      sendStatus("PWM_PINS:3,5,6,9,10,11");
      sendStatus("ANALOG_PINS:A0-A5");
      
    } else {
      sendStatus("UNKNOWN COMMAND: " + line);
    }
  }
}