#include <Servo.h>
#include <Wire.h>
//https://github.com/sparkfun/MPU-9150_Breakout
#include "I2Cdev.h"
#include "MPU6050.h"

double analogValue;
int angle;
Servo servo1;

MPU6050 accelgyro; // address = 0x68, the default, on MPU6050 EVB

int16_t ax, ay, az;
int16_t gx, gy, gz;
int16_t mx, my, mz;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(38400);
  //servo1.attach(9);
  //servo1.write(0);
  while(1){
    Wire.begin();
    accelgyro.initialize();
    accelgyro.setI2CBypassEnabled(true);
    if(accelgyro.testConnection()){
      Serial.println("Connected");
    }else{
      Serial.println("Retry");
      delay(1000);
    }
  }
}

void loop() {
  accelgyro.getMotion9(&ax, &ay, &az, &gx, &gy, &gz, &mx, &my, &mz);
  
  analogValue = double(analogRead(0));
  angle = int(analogValue/1024.0 * 180);
  //servo1.write(angle);
  Serial.println(ax);
}
