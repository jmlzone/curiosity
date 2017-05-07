#!/usr/bin/python
import chassis
import sys
import time
import RPi.GPIO as GPIO

c = chassis.chassis()
cmd = sys.argv[1]
dur = sys.argv[2]
c.run(cmd,dur)
GPIO.cleanup()
print("Complete moved %s for %s seconds" %(cmd,dur) )
