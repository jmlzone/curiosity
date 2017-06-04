#!/usr/bin/python
""" try this as an example
 sudo ./taskRun.py reverse 2 left 2 right 2  forward 2
"""
import chassis
import sys
import time
import RPi.GPIO as GPIO
import sensors
import camera
import socket

def sequenceNumber():
    sequencePath = configRoot + "/sequence.txt"
    if os.path.isfile(sequencePath):
        file = open(sequencePath)
        sequence = file.read()
        file.close()
        sequence = str(int(sequence) + 1)
    else:
        sequence = "1"
    file = open(sequencePath,"w")
    file.write(sequence)
    file.close()
    return sequence


hostname = socket.gethostname()
htmlRoot = "/var/www/html/curiosity"
configRoot = htmlRoot + "/missions"
htmlBaseName = htmlRoot + "/" + hostname + "_"

seq = sequenceNumber()

c = chassis.chassis()
s = sensors.sensors()
cam = camera(hostname,seq,htmlBaseName,40)


argNum = 1;
while (argNum < len(sys.argv)) :
    task = sys.argv[argNum]
    if(task.find("cam") != -1):
        cam.taskCapture(task, sys.argv[argNum+1])
    else:
        c.run(task, sys.argv[argNum+1])
    s.readAll()
    argNum = argNum + 2

GPIO.cleanup()
