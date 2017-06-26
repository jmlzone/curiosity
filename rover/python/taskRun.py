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
import os
import string

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
        name = file.read().rstrip()
        file.close()
    else:
        name = "testing"
    return name

def getLock(path,tasks):
    lockFile = os.path.abspath(path + "/lock.txt")
    if os.path.isfile(lockFile):
        file = open(lockFile)
        taskList = file.read()
        file.close()
        print("ERROR Can not send new tasks to this rover, it is busy")
        print("ERROR Did you click 'Run' twice?")
        print("ERROR I am currently running %s" % taskList)
        print("ERROR Please wait until I complete my current tasks")
        exit(-1)
    else:
        file = open(lockFile,"w")
        file.write(string.join(tasks," "))
        file.close()
def releaseLock(path):
    lockFile = os.path.abspath(path + "/lock.txt")
    if os.path.isfile(lockFile):
        os.remove(lockFile)
    else :
        print("Warning, no lock to remove after mission %s" % lockFile)

hostname = socket.gethostname()
htmlRoot = "/var/www/html"
configRoot = htmlRoot + "/curiosity/missions"
seq = sequenceNumber()
missionName = getMissionName()
imgBaseName =  "/curiosity/missions/" + hostname + "_" + missionName + "_"
getLock(configRoot,sys.argv)
missionLog = open( configRoot + "/" + missionName + "_log.html", "a")
c = chassis.chassis()
s = sensors.sensors()
cam = camera.camera(hostname,seq,htmlRoot,imgBaseName,4,missionLog)
missionLog.write("<h2>Sequence %s</h2><br>" % seq)
print("<h2>Mission: %s sequence %s</h2><br>" %(missionName, seq))
argNum = 1;
while (argNum < len(sys.argv)) :
    task = sys.argv[argNum]
    missionLog.write("<h3>%s %s</h3><br>" % (task, sys.argv[argNum+1]))
    print("<h3>%s %s</h3><br>" % (task, sys.argv[argNum+1]))
    if(task.find("cam") != -1):
        cam.taskCapture(task, sys.argv[argNum+1])
    else:
        c.run(task, sys.argv[argNum+1])
    s.readAll(missionLog)
    argNum = argNum + 2

cam.vidStop()
cam.close()
missionLog.write("<hr>")
print ("</pre>")
print ("    View <a href=\"/curiosity/missions/mission.html\">most recent mission</a><br>")
print ("    View all <a href=\"/curiosity/missions/index.html\">Mission Index</a><br>")
print ("    <a href=\"/cgi-bin/newMission.pl\">Start a new Mission</a><br>")
print ("    <a href=\"/cgi-bin/missionBuild.pl\">Build Mission Task List</a><br>")
print ("    <a href=\"/cgi-bin/motorCal.pl\">Motor Calibration</a>")
print ("    <br>")
print ("    <img src=/curiosity.jpg>")
print ("    <hr>")

GPIO.cleanup()
releaseLock(configRoot)
