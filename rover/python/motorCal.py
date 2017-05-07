#!/usr/bin/python
import chassis
import sys
import time
import RPi.GPIO as GPIO

m = chassis.motors (18,23,25,24)
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
print("Complete moved %s for %s ms" %(cmd,dur) )
