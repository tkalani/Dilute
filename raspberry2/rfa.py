import serial
import time
ser1 = serial.Serial('/dev/ttyACM0',9600) #ph
ser2 = serial.Serial('/dev/ttyACM1', 9600) # turbidity

def readPH():
    return -1
def readTurb():
    for i in range(20):
	ser2.readline()
    return ser2.readline()
def getVal():
    return readPH(), readTurb()[:-2]
if __name__ == "__main__":
    print readPH(), readTurb()[:-2]

