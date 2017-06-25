import smbus
import math
import time
"""----------------------------------------------------------------------
HMC5883L
Register Addresses
----------------------------------------------------------------------"""
CONF_A  = 0x00 # Configuration A (Bits below)
AVG1 = 0 <<5   # Average 1 sample per reading  (don't avaerage)
AVG2 = 1 <<5   # Average 2 samples per reading  
AVG4 = 2 <<5   # Average 4 samples per reading  
AVG8 = 3 <<5   # Average 8 samples per reading
ODR0_75 = 0 << 2 # output data rate 0.75 hz
ODR1_5  = 1 << 2 # output data rate 1.5 hz
ODR3    = 2 << 2 # output data rate 3 hz
ODR7_5  = 3 << 2 # output data rate 7.5 hz
ODR15   = 4 << 2 # output data rate 15 hz
ODR30   = 5 << 2 # output data rate 30 hz
ODR75   = 6 << 2 # output data rate 75 hz
ODRRSVD = 7 << 2 # output data rate reserved
MMNORM  = 0      # normal measurment mode
MMPOS   = 1      # positive bias forced
MMNEG   = 2      # Negative bias forced
MMRSVD  = 3      # reserved mode
CONF_B  = 0x01 # Configuration B (Bits below)
GAIN0_88 = 0 << 5 # +/- 0.88 Ga field
GAIN1_3  = 1 << 5 # +/- 1.3 Ga field
GAIN1_9  = 2 << 5 # +/- 1.9 Ga field
GAIN2_5  = 3 << 5 # +/- 2.5 Ga field
GAIN4    = 4 << 5 # +/- 4 Ga field
GAIN4_7  = 5 << 5 # +/- 4.7 Ga field
GAIN5_6  = 6 << 5 # +/- 5.6 Ga field
GAIN8_1  = 7 << 5 # +/- 8.1 Ga field
LSBSCALE=[0.73,0.92,1.22,1.52,2.27,2.56,3.03,4.35]
MODE    = 0x02 # Mode (bits below)
HS     = 1<<1 # high speed (3.4MHZ I2C) enable
CONT   = 0 # continuous measurement
SINGLE = 1 # take a signle reading (one reading latency)
IDLE   = 2 # device is set idle
IDLE3  = 3 # alternate idle mode
DATA_XH = 0x03 # X MSBs
DATA_XL = 0x04 # X LSBs
DATA_ZH = 0x05 # Z MSBs
DATA_ZL = 0x06 # Z LSBs
DATA_YH = 0x07 # Y MSBs
DATA_YL = 0x08 # Y LSBs
STATUS  = 0x09
ID_A    = 0x0A # indentification
ID_B    = 0x0B # indentification
ID_C    = 0x0C # indentification
class mag:
    def __init__(self, bus=1, addr=0x1e):
        self.i2cBus = smbus.SMBus(bus)
        self.addr=addr
        self.busnum = bus
        self.online = True
        self.lsb = 1
        try:
            self.i2cBus.write_byte_data(self.addr, CONF_A, (AVG8 + ODR30 + MMNORM))
        except:
            #print("unable to write CONF_A")
            self.online = False
        try:
            self.i2cBus.write_byte_data(self.addr, CONF_B, GAIN1_9)
            self.lsb=LSBSCALE[2]
        except:
            #print("unable to write CONF_B")
            self.online = False
        try:
            self.i2cBus.write_byte_data(self.addr, MODE, CONT)
        except:
            #print("unable to write MODE")
            self.online = False
        if(self.online) :
            print("Magnetometer initialized OK")
        else:
            print("Magnetometer initialized Failed")
    def signCorrect(self,val) :
        if (val & (1<<15)) :
            val = val - (1<<16)
        return(val)
    def readXYZ(self) :
        if(self.online) :
            try:
                [xh,xl,zh,zl,yh,yl] = self.i2cBus.read_i2c_block_data(self.addr,DATA_XH,6)
                #print(" %x %x %x %x %x %x" % (xh,xl,zh,zl,yh,yl))
                xraw = ((xh & 0xff) <<8) + (xl & 0xff)
                yraw = ((yh & 0xff) <<8) + (yl & 0xff)
                zraw = ((zh & 0xff) <<8) + (zl & 0xff)
            except:
                print("Warning unable to read magnetometer at address %x on bus %x" % (self.addr,self.busnum))
        else :
            xraw = 0
            yraw = 0
            zraw = 0
        x = self.signCorrect(xraw)
        y = self.signCorrect(yraw)
        z = self.signCorrect(zraw)
        return(x,y,z)
    def absMag(self) :
        (x,y,z) = self.readXYZ()
        mag =( math.sqrt((x*x) + (y*y) + (z*z))  / self.lsb)/1000
        return(mag)
    def measure(self) :
        return(self.absMag())
if __name__ == "__main__":
    s = mag()
    for i in range(40) :
        (x,y,z) = s.readXYZ()
        print("raw x=%d, y=%d,z=%d" %(x,y,z))
        absMag = s.measure()
        print("absMag = %2.2f" % absMag)
        time.sleep(0.5)
