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
import os
import RPi.GPIO as GPIO
import sys
import subprocess

class camera:
    def __init__ (self,hostname,seq, htmlRoot, imagePath, rangerPin, log) :
        self.hostname = hostname
        self.seq = seq
        self.htmlRoot = htmlRoot
        self.imagePath = imagePath
        self.camLock = os.path.dirname(self.htmlRoot + self.imagePath) + "/camLock"
        self.rangerPin = rangerPin
        self.log=log
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
    	self.camera.hflip = True
    	self.camera.vflip = True
    	self.camera.crop = (0.0, 0.0, 1.0, 1.0)
        self.camera.framerate = 30
        self.camera.start_preview()
        self.vidRunning = False
        self.view = 0
        self.vid = 0

    def capture(self,camHs, numPic, useRanger) :
        if(self.getCamLock()) :
            pname = self.htmlRoot + self.imagePath + self.seq + ("_%d_" % self.view) + "%d" + ".jpg"
            # print ("pname = %s" % pname)
            print ("capturing %d images" % numPic)
            if(useRanger) :
                GPIO.output(self.rangerPin,GPIO.HIGH)
            self.camera.capture_sequence([pname %i for i in range(numPic)], use_video_port=camHs)
            if(useRanger) :
                GPIO.output(self.rangerPin,GPIO.LOW)
            self.releaseCamLock()
            return(True)
        else:
            return(False)

    def vidStart(self) :
        if(self.getCamLock()) :
            vname = self.htmlRoot + self.imagePath + self.seq + ("_%d" % self.vid) + ".h264"
            self.camera.start_recording(vname,format='h264')
            self.vidRunning=True

    def vidStop(self) :
        if(self.vidRunning) :
            self.camera.stop_recording()
            self.releaseCamLock()
            h264path = self.htmlRoot + self.imagePath + self.seq + ("_%d" % self.vid) + ".h264"
            mp4path = self.htmlRoot + self.imagePath + self.seq + ("_%d" % self.vid) + ".mp4"
            args = ['MP4Box',  '-fps', '30', '-add', h264path, mp4path]
            convPid = subprocess.call(args)
            vbase = self.imagePath + self.seq + ("_%d" % self.vid) + ".mp4"
            print("<video id=\"curiosityVideo\" src=%s preload controls ></video>" % vbase)
            self.log.write("<video id=\"curiosityVideo\" src=%s preload controls ></video>" % vbase)
            self.vidRunning=False
            self.vid = self.vid + 1

    def taskCapture(self,task,numStr):
        num = int(numStr)
        useRanger = (task.find("RF") != -1)
        camHs = (task.find("HS") != -1)
        vid = (task.find("Vid") != -1)
        if(vid) :
            if(num >=1) :
                self.vidStart()
            else:
                self.vidStop()
        else:
            success = self.capture(camHs,num,useRanger)
            if(success) :
                pbase = self.imagePath + self.seq + ("_%d_" % self.view)
                for i in range(num) :
                    print("<img src=%s%d.jpg ><br>" % (pbase,i))
                    self.log.write("<img src=%s%d.jpg ><br>" % (pbase,i))
                self.view = self.view +1
    def getCamLock(self) :
        if( os.path.isfile(self.camLock ) ):
            print("Error, Camera already in use")
            return(False)
        else :
            file = open(self.camLock,"w")
            file.write("Locked")
            return(True)
            
    def releaseCamLock(self) :
        if( os.path.isfile(self.camLock ) ):
            os.remove(self.camLock)
    def close(self) :
        self.camera.close()
