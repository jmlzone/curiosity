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
        self.left = hPair(la,lb)
        self.right = hpair(ra,rb)

    def forward(self, ms):
        self.left.forward()
        self.right.forward()
        time.sleep(float(ms)/1000.0)
        self.left.stop()
        self.right.stop()

    def reverse(self, ms):
        self.left.reverse()
        self.right.reverse()
        time.sleep(float(ms)/1000.0)
        self.left.stop()
        self.right.stop()

    def left(self, ms):
        self.left.reverse()
        self.right.forward()
        time.sleep(float(ms)/1000.0)
        self.left.stop()
        self.right.stop()

    def right(self, ms):
        self.left.forward()
        self.right.reverse()
        time.sleep(float(ms)/1000.0)
        self.left.stop()
        self.right.stop()
