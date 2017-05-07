#!/usr/bin/python
""" try this as an example
 sudo ./taskRun.py reverse 2 left 2 right 2  forward 2
"""
import chassis
import sys
import time
import RPi.GPIO as GPIO
import sensors

c = chassis.chassis()
s = sensors.sensors()

argNum = 1;
while (argNum < len(sys.argv)) :
    c.run(sys.argv[argNum], sys.argv[argNum+1])
    s.readAll()
    argNum = argNum + 2

GPIO.cleanup()
