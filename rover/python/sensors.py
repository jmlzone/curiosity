""" File for all sensor readings on curiosity rover
"""
import ranger
import irTemp
import spidev
import Adafruit_DHT
import mag
import os

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
    def __init__ (self,log) :
        self.installPath = os.path.dirname(os.path.realpath(__file__))
        self.saveFile = os.path.abspath(self.installPath + "/../sensorStatus.py")
        self.saveSensorList = ['rFrontOnline','rRearOnline','irOnline','htOnline']
        if os.path.isfile(self.saveFile):
            execfile(self.saveFile)
            for sensor in self.saveSensorList :
                self.__dict__[sensor] = dict(**locals())[sensor]
                if(not dict(**locals())[sensor]) :
                    print("Warning %s sensor is offline" % sensor)
                    log.write("Warning %s sensor is offline<br>" % sensor)
        else:
            for sensor in self.saveSensorList :
                self.__dict__[sensor] = True
        if(self.rFrontOnline) :
            self.rFront = ranger.ranger(17,27)
        if(self.rRearOnline) :
            self.rRear = ranger.ranger(19,26)
        if(self.irOnline) :
            self.ir=irTemp.irTemp()
        if(self.htOnline) :
            self.ht=DHT(22)
        self.voltage = adcChan(0,float(0.02))
        self.gas = adcChan(1,float(0.005))
        self.uv = adcChan(6,float(0.005))
        self.light = adcChan(7,float(1.0/200.0))
        self.mag=mag.mag()

    def saveStatus(self) :
        self.installPath = os.path.dirname(os.path.realpath(__file__))
        self.saveFile = os.path.abspath(self.installPath + "/../sensorStatus.py")
        f = open(self.saveFile,"w") 
        for sensor in self.saveSensorList :
            f.write("%s = %s\n" % (sensor, str(self.__dict__[sensor])))
        f.close()

    def readAll(self,log) :
        if(self.rFrontOnline) :
            forwardDistance = self.rFront.measure() / 100.0
        else :
            forwardDistance = 0
        if(forwardDistance < 0 ) :
            self.rFrontOnline = False
            self.saveStatus()
        if(self.rRearOnline) :
            reverseDistance = self.rRear.measure() / 100.0
        else :
            reverseDistance = 0
        if(reverseDistance < 0 ) :
            self.rRearOnline = False
            self.saveStatus()
        if(self.irOnline) :
            (amb,obj) = self.ir.measure()
            if(amb < 0 or obj <0 ) :
                self.irOnline = False
                self.saveStatus()

        if(self.htOnline) :
            (hum,temp) = self.ht.measure()
            if(hum == None) :
                hum = -1
                self.htOnline = False
                self.saveStatus()
            if(temp == None) :
                if(self.htOnline) :
                    self.htOnline = False
                    self.saveStatus()
                temp = -273
        batVolts = self.voltage.measure()
        uv = self.uv.measure()
        gas = self.gas.measure()
        light = self.light.measure()
        absMag=self.mag.measure()

        print ("Sensor Readings:")
        log.write ("Sensor Readings:<br>")
        if(self.rFrontOnline or self.rRearOnline) :
            print ("Distances: Forward = %4.2f Meters, Reverse = %4.2f Meters" % (forwardDistance, reverseDistance))
            log.write ("Distances: Forward = %4.2f Meters, Reverse = %4.2f Meters<br>" % (forwardDistance, reverseDistance))
        if(self.irOnline) :
            print ("Temperatures: Ambient = %4.1f C, Object = %4.1f C" % (amb,obj))
            log.write ("Temperatures: Ambient = %4.1f C, Object = %4.1f C<br>" % (amb,obj))
        if(self.htOnline) :
            print ("Relative Humidity = %4.1f, Temperature = %4.1f" % (hum,temp))
            log.write ("Relative Humidity = %4.1f, Temperature = %4.1f<br>" % (hum,temp))
        print ("Battery Voltage = %4.1f V" % batVolts)
        log.write ("Battery Voltage = %4.1f V<br>" % batVolts)
        print ("Gas Level = %5.2f" % gas)
        log.write ("Gas Level = %5.2f<br>" % gas)
        print ("UV Level = %5.2f" % uv)
        log.write ("UV Level = %5.2f<br>" % uv)
        print ("Light Level = %5.2f" %light)
        log.write ("Light Level = %5.2f<br>" %light)
        print ("Magnetic Field = %2.2f Guass" % absMag)
        log.write ("Magnetic Field = %2.2f Guass<br>" % absMag)

        

        
