#!/usr/bin/python
import chassis
import sys
import time
import RPi.GPIO as GPIOimport RPi.GPIO as GPIO

m = motors (1,2,3,4)
cmd = sys.argv[1]
dur = sys.argv[2]

if(cmd == 'forward') :
    m.forward(dur)
elif (cmd == 'reverse') :
    m.reverse(dur)
elif (cmd == 'left') :
    m.left(dur)
else:
    m.right(dur)
GPIO.cleanup()
