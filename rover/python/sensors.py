""" File for all sensor readings on curiosity rover
"""
import ranger
import irTemp
import spidev
import Adafruit_DHT

""" examples of sensors and how to read

r1 = ranger.ranger(17,27)
r2 = ranger.ranger(19,26)
ir=irTemp.irTemp()
forwardDstance = r1.measure()
reverseDistance = r2.measure()
(amb,obj) = ir.measure()
"""
spi = spidev.SpiDev()
spi.open(0, 0)

class adcChan :
    def __init__ (self,chan,scale) :
        self.chan = chan
        self.scale = scale
        if chan > 7 or chan < 0 :
            print "Error bad adc channel number must be 0-7"
            return -1
    def measure(self) :
        r = spi.xfer2([1, 8 + self.chan << 4, 0])
        data = ((r[1] & 3) << 8) + r[2]
        return ( float(data) * self.scale)

class DHT :
    def __init__(self,pin):
        self.pin = pin

    def measure(self) :
        (humidity, temperature) = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, self.pin)
        if humidity is not None and  temperature is not None:
            temperatureF = 9/5.0 * temperature + 32
        else:
            humidity = None
            temperatureF = None
        return (humidity, temperatureF)


class sensors :
    """ All sensors on the Curiosity platform """
    def __init__ (self) :
        self.rFront = ranger.ranger(17,27)
        self.rRear = ranger.ranger(19,26)
        self.ir=irTemp.irTemp()
        self.ht=DHT(22)
        self.voltage = adcChan(0,float(0.02))
        self.gas = adcChan(1,float(0.005))
        self.uv = adcChan(2,float(0.005))
        self.light = adcChan(3,float(1.0/200.0))

    def readAll(self,log) :
        forwardDistance = self.rFront.measure()
        reverseDistance = self.rRear.measure()
        (amb,obj) = self.ir.measure()
        #(hum,temp) = self.ht.measure()
        batVolts = self.voltage.measure()
        uv = self.uv.measure()
        gas = self.gas.measure()
        light = self.light.measure()

        print ("Sensor Readings:")
        print ("Distances: Forward = %f, Reverse = %f" % (forwardDistance, reverseDistance))
        print ("Temperatures: Ambient = %f, Object = %f" % (amb,obj))
        #print ("Relative Humidity = %f, Temperature = %f" % (hum,temp))
        print ("Battery Voltage = %f " % batVolts)
        print ("Gas Level = %f" % gas)
        print ("UV Level = %f" % uv)
        print ("Light Level = %f" %light)

        log.write ("Sensor Readings:<br>")
        log.write ("Distances: Forward = %f, Reverse = %f<br>" % (forwardDistance, reverseDistance))
        log.write ("Temperatures: Ambient = %f, Object = %f<br>" % (amb,obj))
        #log.write ("Relative Humidity = %f, Temperature = %f<br>" % (hum,temp))
        log.write ("Battery Voltage = %f <br>" % batVolts)
        log.write ("Gas Level = %f<br>" % gas)
        log.write ("UV Level = %f<br>" % uv)
        log.write ("Light Level = %f<br>" %light)

        

        
