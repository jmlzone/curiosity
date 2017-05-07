#!/usr/bin/python
import chassis
import sys
import time
import RPi.GPIO as GPIO

c = chassis.chassis()
c.stop()
GPIO.cleanup()
print("Stopped!")
