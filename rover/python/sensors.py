""" File for all sensor readings on curiosity rover
"""
import ranger
import irTemp
import spidev

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

class sensors :
    """ All sensors on the Curiosity platform """
    def __init__ (self) :
        self.rFront = ranger.ranger(17,27)
        self.rRear = ranger.ranger(19,26)
        self.ir=irTemp.irTemp()
        self.voltage = self.adcChan(0,float(5.12/1023.0))
        self.gas = self.adcChan(1,float(1/200))
        self.uv = self.adcChan(2,float(1/200))
        self.light = self.adcChan(3,float(1/200))

    def readAll(self) :
        forwardDstance = self.rFront.measure()
        reverseDistance = self.rRear.measure()
        (amb,obj) = self.ir.measure()
        batVolts = self.voltage.measure()
        uv = self.uv.measure()
        gas = self.gas.measure()
        light = self.light.measure()

        print "Sensor Readings:"
        print "Distances: Forward = %f, Reverse = %f" % (forwardDistance, reverseDistance)
        print "Temperatures: Ambient = %f, Object = %f" % (amb,obj)
        print "Battery Voltage = %f " % batVolts
        print "UV Level = %f" % uv
        print "Light Level = %f" %light


        
