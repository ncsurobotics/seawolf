#!/usr/bin/env python
import sys
import seawolf
import serial

seawolf.loadConfig("../conf/hub.conf")
seawolf.init("Pneumatics")

BAUD = 9600
N_ACTUATORS = 6

class Pneumatics(object):
    def __init__(self):
        self.serial = None

    """open a serial port with the pneumatics arduino"""
    def connect(self, path):
        self.serial = serial.Serial(path, BAUD)
        
    """fires corresponding pneumatics valve"""
    def fire(self,actuator):
        if (0 < actuator) && (actuator < 6):
            self.serial.write(chr(actuator))
            seawolf.logging(seawolf.INFO, "Actuator {} fired!".format(actuator))
        else:
            seawolf.logging(seawolf.ERROR, "Invalid Actuator Command")


def main():
    if len(argv) < 1:
        print("Need filepath to serial device as argument.")
        sys.exit()

    pn = Pneumatics()
    
    #connect via usb
    pn.connect(sys.argv[1])

    #Notify filters
    Notify_filter(FILTER_ACTION, "PNEUMATICS_REQUEST");

    #watch for any notifications
    while 1:
        (event, msg) = seawolf.notify.get()

        #handle any "PNEUMATICS_REQUEST,fire n" as a signal to pneumatics
        if (event == "PNEUMATICS_REQUEST"):
            (action,actuator) = msg.split(' ')

            if (action == 'fire'):
                pn.fire(actuator)

        pass
            
main()
        

        
    
