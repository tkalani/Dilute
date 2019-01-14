import sys
import RPi.GPIO as gpio

gpio.setwarnings(False)
def runMotor(flag, pin):
    gpio.setmode(gpio.BCM)
    gpio.setup(pin, gpio.OUT)
    if(flag == 1):
        gpio.output(pin, gpio.HIGH) 
    else:
        gpio.output(pin, gpio.LOW)
    return 

if __name__ == "__main__":
        print "ACTUATOR SCRIPT CALLED"
        args = sys.argv
        if len(args) < 3:
                exit()
        else:
                print "FLAG: %d, ACT_ID: %d"%(int(args[1]), int(args[2]))
                runMotor(int(args[1]), int(args[2]))
