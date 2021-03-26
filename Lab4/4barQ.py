import smbus
import time
from math import *

bus = smbus.SMBus(1);            # 0 for R-Pi Rev. 1, 1 for Rev. 2

STANDARD_PRESSURE    = 1013.25 # hPa

#BMP180 (Barometer) constants
BMP180_ADDRESS            = 0x77

# Calibration coefficients
BMP180_AC1                = 0xAA
BMP180_AC2                = 0xAC
BMP180_AC3                = 0xAE
BMP180_AC4                = 0xB0
BMP180_AC5                = 0xB2
BMP180_AC6                = 0xB4
BMP180_B1                = 0xB6 
BMP180_B2                = 0xB8 
BMP180_MB                = 0xBA 
BMP180_MC                = 0xBC 
BMP180_MD                = 0xBE 

class IMU(object):

    def write_byte(self,adr, value):
        bus.write_byte_data(self.ADDRESS, adr, value)
    
    def read_byte(self,adr):
        return bus.read_byte_data(self.ADDRESS, adr)

    def read_word(self,adr,rf=1):
        # rf=1 Little Endian Format, rf=0 Big Endian Format
        if (rf == 1):
            low = self.read_byte(adr)
            high = self.read_byte(adr+1)
        else:
            high = self.read_byte(adr)
            low = self.read_byte(adr+1)
        val = (high << 8) + low
        return val

    def read_word_2c(self,adr,rf=1):
        val = self.read_word(adr,rf)
        if(val & (1 << 16 - 1)):
            return val - (1<<16)
        else:
            return val

class gy801(object):
    def __init__(self) :
        self.baro = BMP180()


class BMP180(IMU):
    
    ADDRESS = BMP180_ADDRESS
    
    def __init__(self) :
        #Class Properties
        self.tempC = None
        self.tempF = None
        self.press = None
        self.altitude = None
        
        self.oversampling = 0 
        
        self._read_calibratio_params()
        
    # read calibration data
    def _read_calibratio_params(self) :
        self.ac1_val = self.read_word_2c(BMP180_AC1,0)
        self.ac2_val = self.read_word_2c(BMP180_AC2,0)
        self.ac3_val = self.read_word_2c(BMP180_AC3,0)
        self.ac4_val = self.read_word(BMP180_AC4,0)
        self.ac5_val = self.read_word(BMP180_AC5,0)
        self.ac6_val = self.read_word(BMP180_AC6,0)
        self.b1_val = self.read_word_2c(BMP180_B1,0)
        self.b2_val = self.read_word_2c(BMP180_B2,0)
        self.mc_val = self.read_word_2c(BMP180_MC,0)
        self.md_val = self.read_word_2c(BMP180_MD,0)

    # read uncompensated temperature value
    def getTempC(self) :
        # print ("Calculating temperature...")
        self.write_byte(0xF4, 0x??)
        time.sleep(0.005)
        
        ut = self.read_word(0xF6,0)

        # calculate true temperature
        x1 = ((ut - self.ac6_val) * self.ac5_val) >> 15
        x2 = (self.mc_val << 11) // (x1 + self.md_val)
        b5 = x1 + x2 
        self.tempC = ((b5 + 8) >> 4) / 10.0
        
        return self.tempC

    def getTempF(self) :
        #print ("Calculating temperature (Fahrenheit)...")
        self.tempF = self.getTempC() * 1.8 + 32

        return self.tempF

    # read uncompensated pressure value
    def getPress(self) :
        # print ("Calculating temperature...")
        self.write_byte(0xF4, 0x??)
        time.sleep(0.005)
        
        ut = self.read_word(0xF6,0)

        x1 = ((ut - self.ac6_val) * self.ac5_val) >> 15
        x2 = (self.mc_val << 11) // (x1 + self.md_val)
        b5 = x1 + x2 

        #print ("Calculating pressure...")
        self.write_byte(0xF4, 0x?? + (self.oversampling << 6))
        time.sleep(0.04)

        msb = self.read_byte(0xF6)
        lsb = self.read_byte(0xF7)
        xsb = self.read_byte(0xF8)
        
        up = ((msb << 16) + (lsb << 8) + xsb) >> (8 - self.oversampling)

        # calculate true pressure
        b6 = b5 - 4000
        b62 = b6 * b6 >> 12
        x1 = (self.b2_val * b62) >> 11
        x2 = self.ac2_val * b6 >> 11
        x3 = x1 + x2
        b3 = (((self.ac1_val * 4 + x3) << self.oversampling) + 2) >> 2

        x1 = self.ac3_val * b6 >> 13
        x2 = (self.b1_val * b62) >> 16
        x3 = ((x1 + x2) + 2) >> 2
        b4 = (self.ac4_val * (x3 + 32768)) >> 15
        b7 = (up - b3) * (50000 >> self.oversampling)

        press = (b7 * 2) // b4
        #press = (b7 / b4) * 2

        x1 = (press >> 8) * (press >> 8)
        x1 = (x1 * 3038) >> 16
        x2 = (-7357 * press) >> 16
        self.press = ( press + ((x1 + x2 + 3791) >> 4) ) / 100.0
        
        return self.press

    # calculate absolute altitude
    def getAltitude(self) :
        #    print ("Calculating altitude...")
        self.altitude = 44330 * (1 - ((self.getPress() / STANDARD_PRESSURE) ** 0.1903))
        return self.altitude

try:
    # if run directly we'll just create an instance of the class and output 
    # the current readings
    
    sensors = gy801()

    barometer = sensors.baro
    
    tempC = barometer.getTempC()
    tempF = barometer.getTempF()
    press = barometer.getPress()
    altitude = barometer.getAltitude()
   
    print ("Barometer:" )
    print ("   Temp: %f C (%f F)" %(tempC,tempF))
    print ("   Press: %f (hPa)" %(press))
    print ("   Altitude: %f m s.l.m" %(altitude))

        
except KeyboardInterrupt:
    print("Cleanup")
