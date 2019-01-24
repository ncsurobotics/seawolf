#!/usr/bin/env python2


import time
import sys
import seawolf

# Names of all the thrusters to be tested
THRUSTERS = ["Bow", "Stern", "Port", "Star", "StrafeB", "StrafeT"]
VAL = .7

def main(args):
    # Connect to hub
    seawolf.loadConfig("../conf/seawolf.conf")
    seawolf.init("Thruster Test")


    #setting value
    global VAL
    if len(sys.argv) == 2:
      VAL = sys.argv[1]
    
    #print values:
    out =""
    for txt in THRUSTERS:
      out+= "\n\t" +txt
    print("INPUTS: " + out)
    

    # Arguments
    try:
      while True:
        selected = raw_input("Thruster to test (q to quit): ")
        if selected == 'q':
          print("quitting")
          break
        found = False
        for thrust in THRUSTERS:
          if str(thrust).lower() == str(selected).lower():
            found = True
            test_thruster(thrust, VAL)
        
        if not found:
          print("input not found")
          print("accepted values are: " + out)
        

    except Exception as e:
      print(e)
    finally:
      for thrust in THRUSTERS:
        seawolf.var.set(thrust, 0)
      seawolf.close()


def test_thruster(name, val=-.3):
    """ Test a named thruster at a given value ::val between -1 and 1
    """

    assert(-1 <= val <= 1)
    print("--------------Start-----------------")
    print("Testing  %s " % (name))
    
    print("Setting %s to %3.2f " % (name, val))
    sys.stdout.flush()
    seawolf.var.set(name, float(val))
    raw_input("press_enter to stop thruster: ")
    seawolf.var.set(name, 0)
    print("Thruster Zeroed")
    print("------------- END--------------------")


if __name__ == '__main__':
    main(sys.argv[1:])
