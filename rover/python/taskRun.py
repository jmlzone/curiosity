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
import os.path

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

def getMissionName():
    namePath = configRoot + "/name.txt"
    if os.path.isfile(namePath):
        file = open(namePath)
        name = file.read()
        file.close()
    else:
        name = "testing"
    return name


hostname = socket.gethostname()
htmlRoot = "/var/www/html"
configRoot = htmlRoot + "/curiosity/missions"
seq = sequenceNumber()
missionName = getMissionName()
imgBaseName =  "/curiosity/missions/" + hostname + "_" + missionName + "_"
missionLog = open( configRoot + missionName + "_log.html", "a")
c = chassis.chassis()
s = sensors.sensors()
cam = camera.camera(hostname,seq,htmlRoot,imgBaseName,22,missionLog)
missionLog.write("<h2>Sequence %d</h2><br>" % seq)

argNum = 1;
while (argNum < len(sys.argv)) :
    task = sys.argv[argNum]
    missionLog.Write("%s %s<br>" % (task, sys.argv[argNum+1]))
    if(task.find("cam") != -1):
        cam.taskCapture(task, sys.argv[argNum+1])
    else:
        c.run(task, sys.argv[argNum+1])
    s.readAll(missionLog)
    argNum = argNum + 2

cam.vidStop()
missionLog.write("<hr>")

GPIO.cleanup()
