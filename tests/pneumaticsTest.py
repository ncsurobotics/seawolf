import sys
import seawolf

sys.path.insert(0,'../mission_control')

import sw3

sys.path.insert(0,'../mission_control/sw3')
from pneumatics import missiles

seawolf.loadConfig("../conf/local-seawolf.conf")
seawolf.init("Pneumatics Test")

x = 1;

while x:
   x = raw_input('Number of the pin to test or the name of the part to test or q to quit: ')
   if (x == 'q'):
	   break
   if len(x) < 2:
     x = int(x)
   sw3.nav.do(sw3.Fire(x))


