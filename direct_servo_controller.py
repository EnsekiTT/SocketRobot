#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import signal
import sys

def exit_handler(signal, frame):
    print("\nBye")
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, exit_handler)

class DirectServo():
    def __init__(self, pin):
        print("Direct Servo")
        self.pin = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)
        self.servo = GPIO.PWM(self.pin, 50)
        self.servo.start(0.0)

    def set_duty_cycle(self, dc):
        self.servo.ChangeDutyCycle(dc)
    

if __name__ == '__main__':
    ds1 = DirectServo(37)
    ds2 = DirectServo(35)
    ds1.set_duty_cycle(0)
    ds2.set_duty_cycle(0)
    y = [i / 10.0 for i in range(20,120,5)]
    while(1):
        for dc in y:
            ds1.set_duty_cycle(dc)
            ds2.set_duty_cycle(12.0-dc)
            time.sleep(0.05)
        y.reverse()
