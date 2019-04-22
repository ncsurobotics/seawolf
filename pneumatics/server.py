#!/usr/bin/env python2
import sys
import seawolf
import serial
import struct
import time
from api import commands

seawolf.loadConfig("../conf/seawolf.conf")
seawolf.init("Pneumatics")

BAUD = 9600


class Pneumatics(object):
    def __init__(self):
        self.port = None

    """open a serial port with the pneumatics arduino"""
    def connect(self, path):
        print "Connecting to", path
        self.port = serial.Serial(path, BAUD)
        self.port.write(struct.pack("B",0xfe ))
        time.sleep(1.5)
        print "Connected to Pneumatics Arduino"
        
    """fires corresponding pneumatics valve"""
    def fire(self, command):
        if command not in commands:
            raise Exception("Command not in dictionary")
        """ Send command to Arduino"""
        msg = commands[command]
        print("Sending command: ", command, msg)
        self.port.write(struct.pack("B", msg))


def main():
    if len(sys.argv) < 1:
        print("Need filepath to serial device as argument.")
        sys.exit()

    pn = Pneumatics()
    
    #connect via usb
    pn.connect(sys.argv[1])

    #Notify filters
    seawolf.notify.filter(seawolf.FILTER_ACTION, "PNEUMATICS_REQUEST")

    #watch for any notifications
    while True:
        (event, msg) = seawolf.notify.get()

        #handle any "PNEUMATICS_REQUEST,fire n" as a signal to pneumatics
        if (event == "PNEUMATICS_REQUEST"):
            if msg == "Kill":
                break
            print msg
            pn.fire(msg)
    print "Pneumatics Killed!"
       
main()
