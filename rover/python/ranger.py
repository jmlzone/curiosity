import RPi.GPIO as GPIO
import time
import gpTimer
class ranger:
    """ Class defining an Ultrasonic Ranger
    take in the pin number in BCM mode 
    has a single function measure to get the distance
    """
    def __init__ (self, trigPin, echoPin) :
        self.trigPin = trigPin
        self.echoPin = echoPin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigPin,GPIO.OUT)
        GPIO.setup(self.echoPin,GPIO.IN)
        self.timeOut = gpTimer.gpTimer(1) 

    def measure (self) :
        """ Returns the ditance measured in CM
        """
        self.timeOut.reset()
        GPIO.output(self.trigPin, GPIO.LOW)
        #print "Waiting For Sensor To Settle"
        time.sleep(0.05)
        GPIO.output(self.trigPin, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.trigPin, GPIO.LOW)

        while GPIO.input(self.echoPin and not self.timeOut.expired)==0:
            pulse_start = time.time()

        while GPIO.input(self.echoPin and not self.timeOut.expired)==1:
            pulse_end = time.time()

        if(self.timeOut.expired) :
            distance =-1
        else :
            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            distance = round(distance, 2)
        return (distance)
    
