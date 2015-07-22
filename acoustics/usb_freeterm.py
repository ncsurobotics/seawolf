import sys
sys.path.insert(0, '../')

import serial as s
import uart  # enable_uart()

# ###########################
##### Global Constants ######
#############################

PORT_NAME = "/dev/ttyUSB0"

# Designate Port object
print("Opening Port %s." % PORT_NAME)
pUSB = s.Serial(PORT_NAME, 9600, timeout=10)


def send(msg):
    pUSB.write(msg + '\n')


def read():
    input = pUSB.readline()
    if input:
        if (input[-1] != '\n'):
            print("String is missing \\n terminator!")

        return input.rstrip('\n')

    return None


def main():
    # Initialize ports

    # Listen for texts and echo them ba
    print("USB terminal active. Any data you enter will be sent"
          + "Out over serial via the FT232RL.")
    while 1:
        try:
            input = raw_input('>> ')
            send(input)

            # Read the data back in
            result = read()
            if not (result):
                print("TIMEOUT!!!!")
            else:
                print("Returned message: %s" % result)

        except KeyboardInterrupt:
            print("Closing Port %s." % PORT_NAME)
            pUSB.close()
            break


if __name__ == '__main__':
    main()
