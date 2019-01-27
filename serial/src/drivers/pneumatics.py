#!/usr/bin/env python2
import sys
import seawolf
import serial

seawolf.loadConfig("../conf/seawolf.conf")
seawolf.init("Pneumatics")

BAUD = 9600
N_ACTUATORS = 6

class Pneumatics(object):
    def __init__(self):
        self.port = None

    """open a serial port with the pneumatics arduino"""
    def connect(self, path):
        self.port = serial.Serial(path, BAUD)
        
    """fires corresponding pneumatics valve"""
    def fire(self,actuator):
        if (0 < actuator) and (actuator < 7):
            self.port.write(chr(actuator))
            seawolf.logging.log(seawolf.INFO, "Actuator {} fired!".format(actuator))
        else:
            seawolf.logging.log(seawolf.ERROR, "Invalid Actuator Command")


def main():
    if len(sys.argv) < 1:
        print("Need filepath to serial device as argument.")
        sys.exit()

    pn = Pneumatics()
    
    #connect via usb
    pn.connect(sys.argv[1])

    #Notify filters
    seawolf.notify.filter(seawolf.FILTER_ACTION, "PNEUMATICS_REQUEST");

    #watch for any notifications
    while 1:
        (event, msg) = seawolf.notify.get()

        #handle any "PNEUMATICS_REQUEST,fire n" as a signal to pneumatics
        if (event == "PNEUMATICS_REQUEST"):
            (action,actuator) = msg.split(' ')
            actuator = eval(actuator)

            if (action == 'fire'):
                pn.fire( actuator )

        pass
            
main()
        

        
    
