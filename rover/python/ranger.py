import RPi.GPIO as GPIO
import time

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

    def measure (self) :
        """ Retrurns the ditance measured in CM
        """
        GPIO.output(self.trigPin, GPIO.LOW)
        #print "Waiting For Sensor To Settle"
        time.sleep(0.05)
        GPIO.output(self.trigPin, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.trigPin, GPIO.LOW)

        while GPIO.input(self.echoPin)==0:
            pulse_start = time.time()

        while GPIO.input(self.echoPin)==1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        return (distance)
    
