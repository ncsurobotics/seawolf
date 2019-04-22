import serial

import time
import struct

print ("start")

ser = serial.Serial("/dev/ttyUSB0",9600)

time.sleep(1)

i=0



print "msg", msg

#connect
while i<21:

  print(i)

  ser.write(msg)
  msg = struct.pack("B",0xfe )

  i=i+1

  time.sleep(1.5)

  x = ser.read()
  print('........')
  print(x)

"""
print "Testing pneumatics"
#from sw3.pneumatics import missiles
from sw3.routines import Fire
print "Firing missiles"
Fire('Torpedo1').start()
#missiles.fire(0)
"""