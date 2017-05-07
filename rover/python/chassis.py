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

    def forward(self, ms):
        self.mLeft.forward()
        self.mRight.forward()
        time.sleep(float(ms))
        self.mLeft.stop()
        self.mRight.stop()

    def reverse(self, ms):
        self.mLeft.reverse()
        self.mRight.reverse()
        time.sleep(float(ms))
        self.mLeft.stop()
        self.mRight.stop()

    def left(self, ms):
        self.mLeft.reverse()
        self.mRight.forward()
        time.sleep(float(ms))
        self.mLeft.stop()
        self.mRight.stop()

    def right(self, ms):
        self.mLeft.forward()
        self.mRight.reverse()
        time.sleep(float(ms))
        self.mLeft.stop()
        self.mRight.stop()

    def stop(self) :
        self.mLeft.stop()
        self.mRight.stop()

class chassis :
    def __init__ (self) :
        self.m = self.motors (18,23,25,24)

    def run (self,cmd,dur) :
        if(cmd == 'forward') :
            self.m.forward(dur)
        elif (cmd == 'reverse') :
            self.m.reverse(dur)
        elif (cmd == 'left') :
            self.m.left(dur)
        elif (cmd == 'right') :
            self.m.right(dur)
        else:
            print "Chassis Error:: Dont know how to do %s %s" % (cmd,dur)

    def stop(self) :
        self.m.stop()
        
