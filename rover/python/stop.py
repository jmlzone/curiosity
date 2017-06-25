#!/usr/bin/python
import chassis
import sys
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(5,GPIO.OUT)
GPIO.output(5,0)
c = chassis.chassis()
c.stop()
GPIO.cleanup()
print("Stopped!")
