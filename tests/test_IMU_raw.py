import serial

DEVICE_PATH = '/dev/ttyUSB0'

def main():
    dev = serial.Serial(DEVICE_PATH, 57600, timeout=3)

    dev.read() #wait until device comes online

    # configure device for raw sensor values
    dev.write('#osrt')
    while 1:
        a = dev.readline()
        b = dev.readline()
        c = dev.readline()
        print(a+b+c)


main()