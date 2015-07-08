#include <Servo.h>

double analogValue;
int angle;
Servo servo1;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  servo1.attach(9);
  servo1.write(0);
}

void loop() {
  analogValue = double(analogRead(0));
  angle = int(analogValue/1024.0 * 180);
  servo1.write(angle);
  Serial.println(angle);
}
