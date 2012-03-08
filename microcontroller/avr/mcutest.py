
import time
import sys
import seawolf as sw

serial = sw.Serial("/dev/ttyUSB1")
serial.setBaud(57600)
serial.setBlocking()

# Signal reset. 5 bytes will guarantee a reset with 3 byte commands if the chip
# is running. If the chip is already reset these will be ignored
for i in range(0, 5):
    serial.sendByte(ord('r'))

# Wait for 16 consecutuve 0xff bytes. This is not a valid command byte so this
# will only happen on reset
i = 0
while i < 16:
    if serial.getByte() == 0xFF:
        i += 1
    else:
        i = 0
    sys.stdout.write(".")
    sys.stdout.flush()

# Send zero to terminate initialization
serial.sendByte(0x00)

# Wait for 0xF0 to indicate end of initialization
while serial.getByte() != 0xF0:
    pass

# Set servo duty cycle to 25%
for n in range(0, 2):
    for b in [0x02, n, 250]:
        serial.sendByte(b)

def read_string():
    l = []
    while True:
        n = chr(serial.getByte())
        if n == '\n':
            break
        l.append(n)
    return ''.join(l)

vl = []

def read_depth():
    global vl
    message = serial.getByte(), serial.getByte(), serial.getByte()

    adc_res = message[1] << 8 | message[2]
    voltage = ((float(adc_res - 200) / (4095 - 200)) * 0.95)
    psi = 100 * ((2 * voltage - 0.5) / 4)
    depth = (psi - 14.73) / 0.4335

    vl.append(voltage)
    stddev = 0
    mean = 0
    if len(vl) > 1:
        mean = sum(vl) / len(vl)
        stddev = (sum([(v - mean) ** 2 for v in vl]) / (len(vl) - 1))**0.5

    print "0x%02x 0x%03x %6.3f (%6.3f %6.3f) %6.2f %6.2f" % (message[0], adc_res, voltage, mean, stddev, psi, depth)

print "Connected"

while True:
    read_depth()
