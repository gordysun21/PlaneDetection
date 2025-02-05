import time
import serial

def getLat():
    getData()
    return lat

def getLon():
    getData()
    return lon

def getOrientation():
    getData()
    return orientation

def getPitch():
    getData()
    return pitch

def getRoll():
    getData()
    return roll

def getData():
    global lat
    global lon
    global orientation
    global pitch
    global roll
    arduinoData = serial.Serial('/dev/tty.usbmodem1201', 9600)
    time.sleep(1) #make sure that 
    while True:
        while arduinoData.in_waiting == 0:
            pass
        dataPacket = arduinoData.readline()
        dataPacket = str(dataPacket, 'utf-8')
        dataPacket = dataPacket.strip('\r\n')
        dataPacket = dataPacket.split(',')
        try:
            lat = float(dataPacket[0])
            lon = float(dataPacket[1])
            pitch = float(dataPacket[2])
            roll = float(dataPacket[3])
            orientation = float(dataPacket[4])
            break
        except IndexError:
            pass