import sys
import os
import serial
from ConfigParser import SafeConfigParser
import glob
import ast
import csv
import datetime
from os import path

PORT_BASE       = "/dev/ttyUSB"
LOG_DIR         = path.join(path.dirname(path.realpath(__file__)), "saved_data/")

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
    def __init__(self):
        self.logger = logger()
        
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
        """gets the data containing a yaw heading.
        """
        self.send('get_data')
        data = self.read()
        data = ast.literal_eval(data)
        
        # Log data if logger is active... and if data was aquired
        if data['data']['heading']:
            self.logger.log_check( ['ab'], [data['data']['heading']['ab']] )
            
        # else log
        else:
            self.logger.log_check( ['ab'], [None])
        
        return data

    def start_logger(self, log_filename):
        """Starts logger on the beaglebone and the seawolf
        """
        # send the correct command to BBB
        self.send('start_log,'+log_filename)

        # Recieve Response
        logger_reply = self.read()
        
        # stop logging if it's already active
        if self.logger.active:
            self.logger.stop_logging()
            
        # Start seawolf-side logger
        self.logger.start_logging(logger_reply)
        
    def stop_logger(self):
        """Stops the logger on the beaglebone and seawolf"""
        
        # send the correct command to BBB
        self.send('stop_log')
        
        # Stop the seawolf logger
        self.logger.stop_logging()
        
        # read logger confirmation output
        if self.read() == None:
            print("acoustics.py: No return response from stop_logger() cmd!")
        
    def help(self):
        """ Prints all the methods and attributes which the caller will have
        access to. Useful when writing new code or debugging a program
        using this class
        """
    
        print("You can call the following attributes: ")
        for item in self.__dict__.keys():
            print("  *.{}".format(item))
    
        print()
        print("You also have access to the following methods: ")
        for item in [method for method in dir(self) if callable(getattr(self, method))]:
            print("  *.{}()".format(item))
        print()
        
        
# ###########################
#### Logger Class ###########
#############################
    
    
class logger():
    def __init__(self):
        # init parameters
        self.active = False
        self.base_path = LOG_DIR
        self.base_name = None
        
    def start_logging(self, data_filename):
        # Exit early if recording is already in progress
        if self.active:
            print("acoustics.py: Already recording %s" % self.base_name)
            return None
            
        # Get base path name
        self.base_name = data_filename
            
        # Create filenames
        #self.sig_fn = self.base_name + " - sig.csv"
        #self.rsig_fn = self.base_name + " - rsig.csv"
        self.ping_fn = self.base_name + " - ping.csv"

        # Create file for signals (w/ record markers), recorded signals,
        # and direction data.
        #self.sig_f = open(path.join(self.base_path, self.sig_fn), 'w')
        #self.rsig_f = open(path.join(self.base_path, self.rsig_fn), 'w')
        self.ping_f = open(path.join(self.base_path, self.ping_fn), 'w')

        # print confirmation
        self.active = True
        print("acoustics.py: Logging is now enabled. Opening '%s' csv file" % self.base_name)
        
        return self.base_name
        
    def stop_logging(self):
        # Release base name
        saved_name = self.base_name
        self.base_name = None

        # Close files
        #self.sig_f.close()
        #self.rsig_f.close()
        self.ping_f.close()

        # set flag
        self.active = False

        # print confirmation
        print("acoustics.py: Logging disabled. '%s' csv files have been closed" % saved_name)
        
    def log_check(self, headers, data):
        if self.active:
            self.log(headers, data)
    
    def log(self, headers, data):
        # init csv writer
        writer = csv.writer(self.ping_f)

        # init variables
        timestamp = get_date_str()

        # If file is empty, write headers at top.
        if self.ping_f.tell() == 0:
            header = ["timestamp"] + headers
            writer.writerow(header)
        
        # Create a row with each point of data
        row = []
        
        # Added timestamp data point
        row.append(get_date_str())
        
        # Add rest of the data points
        for item in data:
            row.append(item)

        # Write data to csv file
        writer.writerow(row)
        
# ###########################
#### Global Functions #######
#############################
def get_date_str():
    return str(datetime.datetime.now()).split('.')[0]

# ###########################
#### Test ###################
#############################
        
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


def start_logger():
    ac = Acoustics()
    ac.connect('/dev/ttyUSB4')
    ac.start_logger('surveys')
