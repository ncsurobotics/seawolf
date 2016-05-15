import serial
from time import sleep
s = serial.Serial("/dev/ttyUSB1", 57600)

i = 0
while 1:
    print(s.read())
    print i
    i += 1
    sleep(0.01)
