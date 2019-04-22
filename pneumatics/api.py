import seawolf
import time

commands = {
    'CloseGrabber'  : 1,
    'OpenGrabber'   : 2 ,
    'Torpedo2'      : 3,
    'Torpedo1'      : 4,
    'Dropper2'      : 5,
    'Dropper1'      : 6,
    #kills pneumatics server
    'Kill'          : None,
    #ascii for 'r'
    'Reset'         : 0x72
}

seawolf.loadConfig("../conf/seawolf.conf")
seawolf.init("PneumaticsClient")

def fire(command):
  if command not in commands:
    raise Exception("Invalid Pneumatics Command:", command)
  
  seawolf.notify.send("PNEUMATICS_REQUEST", command)
