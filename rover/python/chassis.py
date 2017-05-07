import RPi.GPIO as GPIO
import time

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

    def forward(self, sec):
        self.mLeft.forward()
        self.mRight.forward()
        time.sleep(float(sec))
        self.mLeft.stop()
        self.mRight.stop()

    def reverse(self, sec):
        self.mLeft.reverse()
        self.mRight.reverse()
        time.sleep(float(sec))
        self.mLeft.stop()
        self.mRight.stop()

    def left(self, sec):
        self.mLeft.reverse()
        self.mRight.forward()
        time.sleep(float(sec))
        self.mLeft.stop()
        self.mRight.stop()

    def right(self, sec):
        self.mLeft.forward()
        self.mRight.reverse()
        time.sleep(float(sec))
        self.mLeft.stop()
        self.mRight.stop()

    def stop(self) :
        self.mLeft.stop()
        self.mRight.stop()

class servo :
    def __init__ (self,pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.period = 20.0 # ms = 50 hz
        frequency = 1000/self.period # 50 hz
        self.pwm=GPIO.PWM(self.pin,frequency)

    def position (self,angle) :
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


class chassis :
    def __init__ (self) :
        self.m = motors (18,23,25,24)
        self.mast = servo(6) # servo 1
        self.cam = servo(13) # servo 2
        #self.stepper1 = stepper([32,40,38,36]) # only need pins
        #self.stepper2 = stepper([32,40,38,36],delay=0.005) # want to adjust delay
        #self.stepper3 = stepper([32,40,38,36],reverse=1) # need direction reberse
        #self.stepper4 = stepper([32,40,38,36],delay=0.008,reverse=1) #set delay and reverse
        self.wiggle = stepper([12,16,20,21])
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
        elif (cmd == 'nod') :
            self.cam.position(amt)
        elif (cmd == 'wig') :
            self.wiggle.go(amt)
        else:
            print "Chassis Error:: Don't know how to do %s %s" % (cmd,amt)

    def stop(self) :
        self.m.stop()
        
