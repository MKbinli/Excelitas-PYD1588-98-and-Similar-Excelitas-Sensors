# Untitled - By: MKComp - Mon Nov 13 2023
import utime
from machine import Pin
import machine
from time import ticks_ms, ticks_diff, sleep_ms



def configSensor(pinPIRSL,configVal):#configVal:binary 25 bit
    regmask = 0x1000000
    utime.sleep_us(1000)
    bitCount = 25

    for i in range(bitCount):
        bit = (configVal&regmask)!=0
        regmask >>= 1

        if bit == True:
            pinPIRSL.value(0)
            pinPIRSL.value(1)
            pinPIRSL.value(1)
            utime.sleep_us(100)#at least 80us delay

        else:
            pinPIRSL.value(0)
            pinPIRSL.value(1)
            pinPIRSL.value(0)
            utime.sleep_us(100)#at least 80us delay

    pinPIRSL.value(0)
    utime.sleep_us(650)
    return

def readSensorForcedMode(pinPIRDL,waitForBitTime=5):
    #waitForBitTime typically between 2-10ms
    fixedBitSize=15
    fixedBitSizeConfigVal=25;
    uibitmask = 0x4000  # Set BitPos
    PIRval = 0
    statcfg = 0
    pinPIRDL.value(0)
    pinPIRDL.init(pinPIRDL.OUT)
    pinPIRDL.value(1)
    utime.sleep_us(140)
    
    for i in range(fixedBitSize):
        pinPIRDL.value(0)
        pinPIRDL.init(pinPIRDL.OUT)
        utime.sleep_us(1)#at least 200ns delay NOT more than 2000ns
        pinPIRDL.value(1)
        
        pinPIRDL.init(pinPIRDL.IN)
        utime.sleep_us(waitForBitTime)# 2-10us bit comes
        
        if pinPIRDL.value():
            PIRval |= uibitmask
            
        uibitmask >>= 1

        

    ulbitmask = 0x1000000  # Set BitPos

    for k in range(fixedBitSizeConfigVal):
        pinPIRDL.value(0)
        pinPIRDL.init(pinPIRDL.OUT)
        utime.sleep_us(1)#at least 200ns delay NOT more than 2000ns
        pinPIRDL.value(1)
        
        pinPIRDL.init(pinPIRDL.IN)
        utime.sleep_us(waitForBitTime)# 2-10us bit comes

        # If DL High set masked bit
        if pinPIRDL.value():
            statcfg |= ulbitmask
        ulbitmask >>= 1


    pinPIRDL.value(0)
    pinPIRDL.init(pinPIRDL.OUT)
    utime.sleep_us(170)# 160us delay
    pinPIRDL.init(pinPIRDL.IN)###???
    #utime.sleep_us(1250)# 1250us delay
    return PIRval, statcfg


def readSensorInterruptMode(pinPIRDL):
    fixedBitSize=15
    fixedBitSizeConfigVal=25;
    uibitmask = 0x4000  # Set BitPos
    PIRval = 0
    statcfg = 0
    utime.sleep_us(160)# 160us wait after interrupt in order to begin to fetch

    for i in range(fixedBitSize):
        pinPIRDL.value(0)
        pinPIRDL.init(pinPIRDL.OUT)
        utime.sleep_us(1)#at least 200ns delay NOT more than 2000ns
        pinPIRDL.value(1)
        
        pinPIRDL.init(pinPIRDL.IN)
        utime.sleep_us(5)# 2-10us bit comes
        
        if pinPIRDL.value():
            PIRval |= uibitmask
            
        uibitmask >>= 1

    
    ulbitmask = 0x1000000  # Set BitPos

    for k in range(fixedBitSizeConfigVal):
        pinPIRDL.value(0)
        pinPIRDL.init(pinPIRDL.OUT)
        utime.sleep_us(1)#at least 200ns delay NOT more than 2000ns
        pinPIRDL.value(1)
        
        pinPIRDL.init(pinPIRDL.IN)
        utime.sleep_us(5)# 2-10us bit comes

        # If DL High set masked bit
        if pinPIRDL.value():
            statcfg |= ulbitmask
        ulbitmask >>= 1

    pinPIRDL.value(0)
    pinPIRDL.init(pinPIRDL.OUT)
    utime.sleep_us(170)# 160us wait
    pinPIRDL.init(pinPIRDL.IN)
    return PIRval, statcfg

def activateInterruptMode():#It isnot appropriate to simultenaously use for 3 PIRs
    global pinPIRLeftDL
    pinPIRLeftDL = Pin("P9",  mode = Pin.IN)
    pinPIRLeftDL.irq(trigger=Pin.IRQ_RISING, handler=readSensorInterruptMode)

def wakeUpMode(pinPIRDL):
    pinPIRDL.init(pinPIRDL.OUT)
    pinPIRDL.value(0)
    pinPIRDL.init(pinPIRDL.IN)
    pinPIRDL.irq(trigger=pinPIRDL.IRQ_RISING, handler=handleWakeUpMode)

def handleWakeUpMode(pinPIRDL):
    global triggerFlag
    pinPIRDL.init(pinPIRDL.OUT)
    pinPIRDL.value(0)
    pinPIRDL.init(pinPIRDL.IN)
    triggerFlag=True

def beginingCondition(pinPIRSL,pinPIRDL):

    pinPIRSL.init(pinPIRSL.OUT)
    pinPIRSL.value(0)
    pinPIRDL.init(pinPIRDL.OUT)
    pinPIRDL.value(0)

def afterConfigCondition(pinPIRSL,pinPIRDL):
    pinPIRSL.init(pinPIRSL.OUT)
    pinPIRSL.value(0)
    pinPIRDL.init(pinPIRDL.IN)
    utime.sleep_ms(3)
    return

def getSensorValue(PIRval, statcfg, printIt=False):
    PIRval &= 0x3FFF  # clear unused bit
    if not (statcfg & 0x60):
        # ADC source to PIR band pass
        # number in 14bit two's complement
        if PIRval & 0x2000:
            PIRval -= 0x4000
    if printIt==True:
        print(" EXTRACTED SENSOR VALUE ")
        print("14bit Sersor Val Dec: " + str(PIRval))
        print("14bit Sersor Val BIN: " + str(bin(PIRval)))
    return PIRval

def printSensorValues(PIRval,statcfg):
    print(" SENSOR VALUE   ")
    print("15Bit PIR DEC : "+str(PIRval))
    print("15Bit PIR BIN : "+str(bin(PIRval)))
    print("15Bit PIR HEX : "+str(hex(PIRval)))
    print(" CONFIG VALUE  ")
    print("25Bit CONFIG DEC : "+str(statcfg))
    print("25Bit CONFIG BIN : "+str(bin(statcfg)))
    print("25Bit CONFIG HEX : "+str(hex(statcfg)))

def delayAfterReadMs(val=3):
    #Interrupt mode 16ms wait
    #Forced Mode at least 2.4ms wait but during 20ms it is possible to fetch correlated values
    val=int(val)
    utime.sleep_ms(val)

def setUpPinForSensorReading(pinSerialIn, pinDirectLink, configurationValue):
    pinPIRSL = Pin(pinSerialIn,  mode = Pin.OUT)
    pinPIRDL = Pin(pinDirectLink,  mode = Pin.IN)
    beginingCondition(pinPIRSL,pinPIRDL)
    configSensor(pinPIRSL,configurationValue)
    afterConfigCondition(pinPIRSL,pinPIRDL)
    return pinPIRSL, pinPIRDL

#########SETUP############
#////PIN DEFS/////#





LEFTPIRCONFIG=0x00000010#16777232 #0x100E230 #0x00000010
pinSerialIn=16
pinDirectLink=17
pinPIRSL, pinPIRDL=setUpPinForSensorReading(pinSerialIn, pinDirectLink, LEFTPIRCONFIG)


while True:

    PIRval, statcfg=readSensorForcedMode(pinPIRDL,waitForBitTime=5)
    printSensorValues(PIRval,statcfg)
    extractedVal=getSensorValue(PIRval, statcfg, printIt=True)
    delayAfterReadMs(val=3)


"""
wakeUpMode(pinPIRLeftDL)

while True:
    if triggerFlag==True:
        triggerFlag=False
        print("Left PIR Waked Up!!!")

"""

