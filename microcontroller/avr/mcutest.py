
import time
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

while True:
    print read_string()
