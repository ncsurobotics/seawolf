from dbEntity import dbEntity
from path import Path
from buoy import Buoy
from gate import Gate
from hedge import Hedge
from pinger import Pinger
from wheel import Wheel
from dice import Dice
from slots import Slots
from goldchip import GoldChip
from cashin import CashIn

entities = {
              "dbEntity"  :   dbEntity,
              "Path"      :   Path,
              "Buoy"      :   Buoy,
              "Gate"      :   Gate,
              "Hedge"     :   Hedge,
              "Pinger"    :   Pinger,
	            "Wheel"     :   Wheel,
              "Dice"      :   Dice,
              "Slots"     :   Slots,
              "GoldChip"  :   GoldChip,
	            "CashIn"    :   CashIn
           }
