import smbus
import time
from math import *

bus = smbus.SMBus(1);            # 0 for R-Pi Rev. 1, 1 for Rev. 2

# General constants
EARTH_GRAVITY_MS2    = 9.80665 # m/s2
STANDARD_PRESSURE    = 1013.25 # hPa

# HMC5883L (Magnetometer) constants
HMC5883L_ADDRESS        =    0x1E  # I2C address
    
HMC5883L_CRA            =    0x00  # write CRA(00), Configuration Register A
HMC5883L_CRB            =    0x01  # write CRB(01), Configuration Register B
HMC5883L_MR             =    0x02  # write Mode(02)
HMC5883L_DO_X_H         =    0x03  # Data Output
HMC5883L_DO_X_L         =    0x04
HMC5883L_DO_Z_H         =    0x05
HMC5883L_DO_Z_L         =    0x06
HMC5883L_DO_Y_H         =    0x07
HMC5883L_DO_Y_L         =    0x08

# L3G4200D constants
L3G4200D_ADDRESS        =    0x69
L3G4200D_CTRL_REG1      =    0x20
L3G4200D_CTRL_REG4      =    0x23
L3G4200D_OUT_X_L        =    0x28
L3G4200D_OUT_X_H        =    0x29
L3G4200D_OUT_Y_L        =    0x2A
L3G4200D_OUT_Y_H        =    0x2B
L3G4200D_OUT_Z_L        =    0x2C
L3G4200D_OUT_Z_H        =    0x2D

# ADXL345 constants
ADXL345_ADDRESS         =    0x53 # I2C address

ADXL345_BW_RATE         =    0x2C # Data rate and power mode control 
ADXL345_POWER_CTL       =    0x2D # Power-saving features control 
ADXL345_DATA_FORMAT     =    0x31 # Data format control 
ADXL345_DATAX0          =    0x32
ADXL345_DATAX1          =    0x33
ADXL345_DATAY0          =    0x34
ADXL345_DATAY1          =    0x35
ADXL345_DATAZ0          =    0x36
ADXL345_DATAZ1          =    0x37

ADXL345_SCALE_MULTIPLIER= 0.00390625    # G/LSP. 1/256 = 0.00390625
ADXL345_BW_RATE_100HZ   = 0x0A          # 0A = 0000 1111
ADXL345_MEASURE         = 0x08          # 08 = 0000 1000

# BMP180 (Barometer) constants
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
        self.compass = HMC5883L()
        self.accel = ADXL345()
        self.gyro = L3G4200D()
        self.baro = BMP180()

class ADXL345(IMU):
    
    ADDRESS = ADXL345_ADDRESS

    def __init__(self) :
        #Class Properties
        self.Xoffset = 0.02  # unit: G, modify by yourself
        self.Yoffset = -0.03  # unit: G, modify by yourself
        self.Zoffset = 0.03  # unit: G, modify by yourself
        self.Xraw = 0.0
        self.Yraw = 0.0
        self.Zraw = 0.0
        self.Xg = 0.0
        self.Yg = 0.0
        self.Zg = 0.0
        self.X = 0.0
        self.Y = 0.0
        self.Z = 0.0
        self.t0x = None
        self.t0y = None
        self.t0z = None

        self.df_value = 0b00001000 
        
        self.Xcalibr = ADXL345_SCALE_MULTIPLIER
        self.Ycalibr = ADXL345_SCALE_MULTIPLIER
        self.Zcalibr = ADXL345_SCALE_MULTIPLIER

        # Register 0x2C: BW_RATE
        self.write_byte(ADXL345_BW_RATE, ADXL345_BW_RATE_100HZ)    
        # write value= 0x0A = 00001111
        # D3-D0: The default value is 0x0A, 
        # which translates to a 100 Hz output data rate.


        # Register 0x2D: POWER_CTL 
        self.write_byte(ADXL345_POWER_CTL, ADXL345_MEASURE)    
        # write value: 0x08 = 00001000
        # D3=1: set 1 for measurement mode.


        # Register 0x31: DATA_FORMAT 
        self.write_byte(ADXL345_DATA_FORMAT, self.df_value)
        # write value=00001000
        # D3 = 1: the device is in full resolution mode, 
        # where the output resolution increases with the g range 
        # set by the range bits to maintain a 4 mg/LSB scale factor. 
        # D1 D0 = range. 00 = +-2g 

    
    # RAW readings in LPS
    # Register 0x32 to Register 0x37:
    # DATAX0, DATAX1, DATAY0, DATAY1, DATAZ0, DATAZ1 (Read Only)
    def getRawX(self) :
        self.Xraw = self.read_word_2c(ADXL345_DATAX0)
        return self.Xraw

    def getRawY(self) :
        self.Yraw = self.read_word_2c(ADXL345_DATAY0)
        return self.Yraw
    
    def getRawZ(self) :
        self.Zraw = self.read_word_2c(ADXL345_DATAZ0)
        return self.Zraw

    # G related readings in g
    # similar to filter. combine current value with previous one.
    # plf = 1 means it only uses "current reading"
    def getXg(self,plf = 1.0) :
        self.Xg = (self.getRawX() * self.Xcalibr - self.Xoffset) * plf + (1.0 - plf) * self.Xg
        return self.Xg

    def getYg(self,plf = 1.0) :
        self.Yg = (self.getRawY() * self.Ycalibr - self.Yoffset) * plf + (1.0 - plf) * self.Yg
        return self.Yg

    def getZg(self,plf = 1.0) :
        self.Zg = (self.getRawZ() * self.Zcalibr - self.Zoffset) * plf + (1.0 - plf) * self.Zg
        return self.Zg
    
    # Absolute reading in m/s2
    def getX(self,plf = 1.0) :
        self.X = self.getXg(plf) * EARTH_GRAVITY_MS2
        return self.X
    
    def getY(self,plf = 1.0) :
        self.Y = self.getYg(plf) * EARTH_GRAVITY_MS2
        return self.Y
    
    def getZ(self,plf = 1.0) :
        self.Z = self.getZg(plf) * EARTH_GRAVITY_MS2
        return self.Z

    def getPitch(self) :
        aX = self.getXg()
        aY = self.getYg()
        aZ = self.getZg()
        self.pitch = atan2(-aX, (pow(pow(aY, 2) + pow(aZ, 2), 0.5)))
        return self.pitch 

    def getRoll(self) :
        aX = self.getXg()
        aY = self.getYg()
        aZ = self.getZg()
        self.roll = atan2(aY, aZ)
        return self.roll

class L3G4200D(IMU):
    
    ADDRESS = L3G4200D_ADDRESS

    def __init__(self) :
        #Class Properties
        self.Xraw = 0.0
        self.Yraw = 0.0
        self.Zraw = 0.0
        self.X = 0.0
        self.Y = 0.0
        self.Z = 0.0
        self.Xangle = 0.0
        self.Yangle = 0.0
        self.Zangle = 0.0
        self.t0x = None
        self.t0y = None
        self.t0z = None

        # set value
        self.gain_std = 0.00875    # dps/digit
        
        self.write_byte(L3G4200D_CTRL_REG1, 0x0F)
        self.write_byte(L3G4200D_CTRL_REG4, 0x80)

        self.setCalibration()

    def setCalibration(self) :
        gyr_r = self.read_byte(L3G4200D_CTRL_REG4)
        
        self.gain = 2 ** ( gyr_r & 48 >> 4) * self.gain_std

    def getRawX(self):
        self.Xraw = self.read_word_2c(L3G4200D_OUT_X_L)
        return self.Xraw

    def getRawY(self):
        self.Yraw = self.read_word_2c(L3G4200D_OUT_Y_L)
        return self.Yraw

    def getRawZ(self):
        self.Zraw = self.read_word_2c(L3G4200D_OUT_Z_L)
        return self.Zraw

    def getX(self,plf = 1.0):
        self.X = ( self.getRawX() * self.gain ) * plf + (1.0 - plf) * self.X
        return self.X

    def getY(self,plf = 1.0):
        self.Y = ( self.getRawY() * self.gain ) * plf + (1.0 - plf) * self.Y
        return self.Y

    def getZ(self,plf = 1.0):
        self.Z = ( self.getRawZ() * self.gain ) * plf + (1.0 - plf) * self.Z
        return self.Z
    
    def getXangle(self,plf = 1.0) :
        if self.t0x is None : self.t0x = time.time()
        t1x = time.time()
        LP = t1x - self.t0x
        self.t0x = t1x
        self.Xangle = self.getX(plf) * LP
        return self.Xangle
    
    def getYangle(self,plf = 1.0) :
        if self.t0y is None : self.t0y = time.time()
        t1y = time.time()
        LP = t1y - self.t0y
        self.t0y = t1y
        self.Yangle = self.getY(plf) * LP
        return self.Yangle
    
    def getZangle(self,plf = 1.0) :
        if self.t0z is None : self.t0z = time.time()
        t1z = time.time()
        LP = t1z - self.t0z
        self.t0z = t1z
        self.Zangle = self.getZ(plf) * LP
        return self.Zangle

class HMC5883L(IMU):
    
    ADDRESS = HMC5883L_ADDRESS

    def __init__(self) :
        #Class Properties
        self.X = None
        self.Y = None
        self.Z = None
        self.angle = None
        self.Xoffset = -245.0
        self.Yoffset = 453.5
        self.Zoffset = -594.5
        
        # Declination Angle
        self.angle_offset = ( -1 * (4 + (32/60))) / (180 / pi)
        # Formula: (deg + (min / 60.0)) / (180 / M_PI);
        # ex: Hsinchu = Magnetic Declination: -4 deg, 32 min
        # declinationAngle = ( -1 * (4 + (32/60))) / (180 / pi)
        # http://www.magnetic-declination.com/
        
        self.scale = 0.92 # convert bit value(LSB) to gauss. DigitalResolution

        # Configuration Register A
        self.write_byte(HMC5883L_CRA, 0b01110000)

        # Configuration Register B
        self.write_byte(HMC5883L_CRB, 0b00100000)
        
        # Mode Register
        self.write_byte(HMC5883L_MR, 0b00000000)

    def getX(self):
        self.X = (self.read_word_2c(HMC5883L_DO_X_H, rf=0) - self.Xoffset) * self.scale
        return self.X

    def getY(self):
        self.Y = (self.read_word_2c(HMC5883L_DO_Y_H, rf=0) - self.Yoffset) * self.scale
        return self.Y

    def getZ(self):
        self.Z = (self.read_word_2c(HMC5883L_DO_Z_H, rf=0) - self.Zoffset) * self.scale
        return self.Z
    
    def getHeading(self):
        bearing  = degrees(atan2(self.getY(), self.getX()))

        if (bearing < 0):
            bearing += 360
        if (bearing > 360):
            bearing -= 360
        self.angle = bearing + self.angle_offset
        return self.angle

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
        self.write_byte(0xF4, 0x2E)
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
        self.write_byte(0xF4, 0x2E)
        time.sleep(0.005)
        
        ut = self.read_word(0xF6,0)

        x1 = ((ut - self.ac6_val) * self.ac5_val) >> 15
        x2 = (self.mc_val << 11) // (x1 + self.md_val)
        b5 = x1 + x2 

        #print ("Calculating pressure...")
        self.write_byte(0xF4, 0x34 + (self.oversampling << 6))
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

def tilt_compensated_heading(y, x):
    if x > 0:
        return atan2(y, x)
    if y >= 0 and x < 0:
        return atan2(y, x) + pi
    if y < 0 and x < 0:
        return atan2(y, x) - pi
    if y > 0 and x == 0:
        return pi / 2
    if y < 0 and x == 0:
        return -pi / 2
    if y == 0 and x == 0:
        return None

try:
    sensors = gy801()
    compass = sensors.compass
    adxl345 = sensors.accel
    gyro = sensors.gyro
    barometer = sensors.baro

    pitch_pre = adxl345.getPitch()
    roll_pre = adxl345.getRoll()

    while True:
        magx = compass.getX()
        magy = compass.getY()
        magz = compass.getZ()
    
        # --------------------------------------------------
        # calculate pitch, roll, tilt
        pitch = (pitch_pre + gyro.getXangle()) * 0.98 + adxl345.getPitch() * 0.02
        roll = (roll_pre + gyro.getYangle()) * 0.98 + adxl345.getRoll() * 0.02

        pitch_pre = pitch
        roll_pre = roll
        # --------------------------------------------------
        
        
        # --------------------------------------------------
        # Heading
        bearing1 = degrees(atan2(magy, magx))

        if (bearing1 < 0):
            bearing1 += 360
        if (bearing1 > 360):
            bearing1 -= 360
        bearing1 = bearing1 + compass.angle_offset
        
        # Tilt compensate
        compx = magx * cos(pitch) + magz * sin(pitch)
        compy = magx * sin(roll) * sin(pitch) \
                + magy * cos(roll) \
                - magz * sin(roll) * cos(pitch)

        bearing2  = degrees(atan2(compy, compx))
        if (bearing2 < 0):
            bearing2 += 360
        if (bearing2 > 360):
            bearing2 -= 360
        bearing2 = bearing2 + compass.angle_offset
        # --------------------------------------------------

        altitude = barometer.getAltitude()

        print(f"Roll: {roll:.3f}, Pitch: {pitch:.3f}, Heading: {degrees(tilt_compensated_heading(compy, compx)):.3f}, Altitude: {altitude:.3f}")
        time.sleep(1)

        
except KeyboardInterrupt:
    print("Cleanup")       