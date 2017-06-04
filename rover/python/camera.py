#!/usr/bin/python
#
# copyleft 2017 James Lee jml@jmlzone.com
# This file is one of many created by or found by James Lee
# <jml@jmlzone.com> to help with the curiosity rover model for stellafane 2017.
#
# All the original files are CopyLeft 2017 James Lee permission is here
# by given to use these files for educational and non-commercial use.
# For commercial or other use please contact the author as indicated in
# the file or jml@jmlzone.com
#
#
# use onboard pi camera
#
import picamera
import os.path
import RPi.GPIO as GPIO
import sys
import re

class camera:
    def __init__ (self,hostname,seq, htmlRoot, imagePath, rangerPin) :
        self.hostname = hostname
        self.seq = seq
        self.htmlRoot = htmlRoot
        self.imagePath = imagePath
        self.rangerPin = rangerPin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.rangerPin, GPIO.OUT)
        GPIO.output(self.rangerPin,GPIO.LOW)    
        self.camera = picamera.PiCamera()
    	self.camera.sharpness = 0
    	self.camera.contrast = 0
    	self.camera.brightness = 50
    	self.camera.saturation = 0
    	self.camera.ISO = 0
    	self.camera.video_stabilization = False
    	self.camera.exposure_compensation = 0
    	self.camera.exposure_mode = 'auto'
    	self.camera.meter_mode = 'average'
    	self.camera.awb_mode = 'auto'
    	self.camera.image_effect = 'none'
    	self.camera.color_effects = None
    	self.camera.rotation = 0
    	self.camera.hflip = False
    	self.camera.vflip = False
    	self.camera.crop = (0.0, 0.0, 1.0, 1.0)
        self.camera.framerate = 30
        self.camera.start_preview()

    def capture(self,camHs, numPic, useRanger) :
        pname = self.htmlRoot + self.imagePath + self.seq + "_" + "%d" + ".jpg"
        print ("capturing %d images" % numPic)
        if(useRanger) :
            GPIO.output(self.rangerPin,GPIO.HIGH)
        self.camera.capture_sequence([pname %i for i in range(numPic)], use_video_port=camHs)
        if(useRanger) :
            GPIO.output(self.rangerPin,GPIO.LOW)

    def taskCapture(self,task,numStr):
        num = int(numStr)
        useRanger = (task.find("RF") != -1)
        camHs = (task.find("HS") != -1)
        self.capture(camHs,num,useRanger)
        pbase = self.imagePath + self.seq + "_"
        for i in range(num) :
            print("<img src=%s%d.jpg ><br>" % (pbase,i))

