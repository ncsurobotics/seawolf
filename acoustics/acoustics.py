import sys
import os
import serial
from ConfigParser import SafeConfigParser
import glob

PORT_BASE = "/dev/ttyUSB"

# ###########################
# Global Settings ###########
#############################
# Load parser
config = SafeConfigParser()
config.read('./sw_config.ini')

def list_ports():
    # Detect if running on a supported platform
    if sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    else:
        raise EnvironmentError('Unsupported platform')
        
    # Search for USB like ports
    result = []
    for port in ports:
        if 'USB' in port:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
    
    # Return a list of all acceptable ports that were found.
    return result


# ###########################
#### Main Class #############
#############################
class Acoustics:
        
    def connect(self, port_name):
        # Open the specified port
        print("Opening Port %s." % port_name)
        self.s_port = serial.Serial(port_name, 9600, timeout=10)
        
        # Listen for texts and echo them ba
        print("USB terminal active. Any data you enter will be sent "
        + "out over serial via the FT232RL.")
    
    def send(self, msg):
        self.s_port.write(msg + '\n')
        
    def read(self):
        # Read the raw data
        input =  self.s_port.readline()
        
        if input:
            # Catch exception when user (BBB) forgets to append newline to msg
            if (input[-1] != '\n'):
                print("String is missing \\n terminator!")
        
            # return successfully with msg
            return input.rstrip('\n')
    
        # readline function timed out. No msg to read. return
        # None in response
        return None
        
    def get_data(self):
        self.send('get_data')
        data = self.read()
        return ast.literal_eval(data)

    def start_logger(self, log_filename):
        # send the correct command to BBB
        self.send('start_log,'+log_filename)

        # Recieve Response
        return self.read()

    def kill(self):
        # dummy method to trick mission into thinking this is a process_manager
        pass

    def ping(self):
        # dummy method to trick mission into thinking this is a process_manager
        pass
        
def test():
    def query_user_for_port():
        # Show human user list of possible acoustics ports
        print('Active ports potentially connected to acoustics:')
        print( '\n'.join(list_ports()) )
    
        # Query user to pick the right port
        print("\nPlease identify which usb port is the correct one for acoustics")
        port_num = raw_input('  >> '+PORT_BASE)
        
        # Parse user's query
        return PORT_BASE+port_num
         
        
    # Clear the screen
    os.system('clear')
    print("BEGGINING ACOUSTICS TEST")
    
    # initial acoustics object
    acoustics = Acoustics()
    
    # Query user for correct port
    port_name = query_user_for_port()
    
    # Connect to acoustics
    acoustics.connect(port_name)
    
    # Get a single data point from acoustics
    data = acoustics.get_data()
    
    # Show user the data and end test
    print data
    print("ENDING ACOUSTICS TEST")
    
