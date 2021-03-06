import RPi.GPIO as GPIO
import time
import os.path

class hPair :
    """ class for a pair of channels on the hbridge for a motor """
    def __init__ (self, a, b ) :
        self.pins = [a,b]
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pins,GPIO.OUT)
        self.stop()

    def forward(self):
        GPIO.output(self.pins, [1,0])

    def reverse(self):
        GPIO.output(self.pins, [0,1])

    def stop(self):
        GPIO.output(self.pins, [0,0])

class motors :
    """ class to encapsulate 2 motors and 4 direction controls """
    def __init__ (self, la,lb, ra, rb) :
        self.mLeft = hPair(la,lb)
        self.mRight = hPair(ra,rb)
        self.limit = 300.0 # 5 minute maximum.

    def run(self,sec) :
        t = float(sec)
        if(t > self.limit) :
            t = self.limit
        time.sleep(t)

    def forward(self, sec):
        self.mLeft.forward()
        self.mRight.forward()
        self.run(sec)
        self.mLeft.stop()
        self.mRight.stop()

    def reverse(self, sec):
        self.mLeft.reverse()
        self.mRight.reverse()
        self.run(sec)
        self.mLeft.stop()
        self.mRight.stop()

    def left(self, sec):
        self.mLeft.reverse()
        self.mRight.forward()
        self.run(sec)
        self.mLeft.stop()
        self.mRight.stop()

    def right(self, sec):
        self.mLeft.forward()
        self.mRight.reverse()
        self.run(sec)
        self.mLeft.stop()
        self.mRight.stop()

    def stop(self) :
        self.mLeft.stop()
        self.mRight.stop()

class servo :
    def __init__ (self,pin):
        self.pin = pin
        self.turnOn()
    def position (self,angle) :
        if(not self.on) :
            self.turnOn()
        # 0 degrees = 0.6 ms
        # 180 degrees = 2.6 ms
        deg0 = 0.6
        deg180 = 2.6
        span = deg180-deg0
        angle = float(angle)
        #print "angle = %f" %angle
        if(angle >=0 and angle <=180) :
            ap=angle/180.0
            pw=(ap*span) + deg0;
            pp = (pw * 100.0)/self.period
            #print "angle %d period %f pulse width %f precent %f" %(angle, self.period, pw, pp)
            self.pwm.start(pp)
            time.sleep(0.1)
            self.pwm.ChangeDutyCycle(pp)
            time.sleep(1.0)
            #self.pwm.stop()
        else :
            print "Error can't go to angle %f" % angle

    def off(self) :
        self.pwm.stop()
        self.on = False

    def turnOn(self):
        GPIO.setup(self.pin, GPIO.OUT)
        self.period = 20.0 # ms = 50 hz
        frequency = 1000/self.period # 50 hz
        self.pwm=GPIO.PWM(self.pin,frequency)
        self.on = True

class stepper :
    def __init__ (self,pins, delay=0.002, reverse=0) :
        self.pins = pins
        GPIO.setup(self.pins, GPIO.OUT)
        GPIO.output(self.pins,GPIO.LOW)    
        self.step=0;
        self.stepDelay = delay # in seconds not lower than 0.002
        self.steps=[[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1]]
        self.reverse = reverse # set directtion to be the other way
    def go(self,num) :
        GPIO.output(self.pins,self.steps[self.step])
        num = int(num)
        if num < 0 :
            num = num *-1
            dir = -1
        else :
            dir = 1
        if(self.reverse==0) :
            dir = - dir
        for i in range(num) :
            self.step = (self.step + dir) % 8
            GPIO.output(self.pins,self.steps[self.step])
            time.sleep(self.stepDelay)
        GPIO.output(self.pins,GPIO.LOW)    
    def off(self) :
        GPIO.output(self.pins,[0,0,0,0])
class mast:
    def __init__(self,chan,down,up):
        self.installPath = os.path.dirname(os.path.realpath(__file__))
        self.saveFile = os.path.abspath(self.installPath + "/../mastAngle.txt")
        self.pos = down
        self.down = down
        self.up = up
        self.servo = servo(chan)
        self.hold()
    def Raise(self):
        for angle in range(self.pos, self.up, 5) :
           self.servo.position(angle)
           self.pos = angle
           time.sleep(0.06)
        #self.servo.off()
    def Lower(self):
        for angle in range(self.pos, self.down, -5) :
           self.servo.position(angle)
           self.pos = angle
           time.sleep(0.06)
        self.servo.off()
    def getLastPos(self) :
        if os.path.isfile(self.saveFile):
            file = open(self.saveFile)
            pos = int(file.read())
            file.close()
        else:
            pos = 20
        return(pos)
    def savePos(self,pos):
        file = open(self.saveFile,"w")
        file.write(str(pos))
        file.close()
    def position(self,newpos) :
        newpos = int(newpos)
        self.pos=self.getLastPos()
        if(newpos > self.pos) :
            step = 5
        else :
            step = -5    
        for angle in range(self.pos, newpos, step) :
           self.servo.position(angle)
           self.savePos(angle)
           self.pos = angle
           time.sleep(0.04)
        if( step < 0) :
            self.servo.off()
    def hold(self):
        """ hold position if we were in the up poistion """
        lastPos = self.getLastPos()
        if(lastPos > 90 ) : # in the up position
            self.servo.position(lastPos)
        
class arm:
    def __init__(self,chan2):
        self.installPath = os.path.dirname(os.path.realpath(__file__))
        self.saveFile = os.path.abspath(self.installPath + "/../armAngle.txt")
        self.servo2 = servo(chan2)
        self.pos2 = 125
    def getLastPos(self) :
        if os.path.isfile(self.saveFile):
            file = open(self.saveFile)
            pos = int(file.read())
            file.close()
        else:
            pos = 180
        return(pos)
    def savePos(self,pos):
        file = open(self.saveFile,"w")
        file.write(str(pos))
        file.close()
    def position(self,newpos) :
        self.pos2 = self.getLastPos()
        newpos = int(newpos)
        if(newpos > self.pos2) :
            step = 5
        else :
            step = -5    
        for angle in range(self.pos2, newpos, step) :
           self.servo2.position(angle)
           time.sleep(0.04)
           self.pos2 = angle
           self.savePos(angle)
        if( step > 0) :
            #self.servo1.off()
            self.servo2.off()
        
class chassis :
    def __init__ (self) :
        self.m = motors (16,12,20,21)
        self.mast = mast(6,40,120) # mast class, channel, down position, up position
        self.arm = arm(13) # 2 servo
        self.nod = stepper([18,23,24,25], delay=0.020)
    def run (self,cmd,amt) :
        if(cmd == 'forward') :
            self.m.forward(amt)
        elif (cmd == 'reverse') :
            self.m.reverse(amt)
        elif (cmd == 'left') :
            self.m.left(amt)
        elif (cmd == 'right') :
            self.m.right(amt)
        elif (cmd == 'mast') :
            self.mast.position(amt)
        elif (cmd == 'arm') :
            self.arm.position(amt)
        elif (cmd == 'nod') :
            self.nod.go(amt)
        else:
            print "Chassis Error:: Don't know how to do %s %s" % (cmd,amt)

    def stop(self) :
        self.m.stop()
        
