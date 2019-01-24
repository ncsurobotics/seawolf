"""
GUI for testing seawolf
To kill program, hit k
Written by Ben Fisher
"""

import cv2
import numpy as np
import math
import seawolf as sw

import sys

sys.path.append('components')
from Dial_GUI_3 import *
from Slider_GUI_3 import *
from Button_GUI_3 import *
from Graphics_GUI_3 import *
from Conversions_GUI_3 import *

import time


sys.path.append('../../mission_control')
import sw3

"""
Initializes the desired roll, pitch, yaw, depth values by reading the PID variable values. Sets forward to 0.
"""
def initializeValues():
        Roll.desiredBearing = realToDisplayRadians(math.radians(sw.var.get("RollPID.Heading")))
        Pitch.desiredBearing = realToDisplayRadians(math.radians(sw.var.get("PitchPID.Heading")))
        Yaw.desiredBearing = realToDisplayRadians(math.radians(sw.var.get("YawPID.Heading")))
        Depth.setSlideValueForDepthReadOnlySlider(sw.var.get("Depth"))
        Forward.setSlideValue(0)
"""
Called in each loop of main, this function sets GUI variables to their HUD counterparts by reading them using sw.var.get(var).
Sets the desired and actual bow, stern, and port values by reading from HUD. Also uses HUD to set depth and thruster values.
"""
def setVars():
            Bow.setSlideValue(sw.var.get("Bow"))
            Stern.setSlideValue(sw.var.get("Stern"))
            Port.setSlideValue( sw.var.get("Port"))
            Star.setSlideValue( sw.var.get("Star"))
            StrafeT.setSlideValue( sw.var.get("StrafeT"))
            StrafeB.setSlideValue( sw.var.get("StrafeB"))
            ActualDepth.setSlideValueForDepthReadOnlySlider( sw.var.get("Depth") )
            Roll.desiredBearing = realToDisplayRadians(math.radians(sw.var.get("RollPID.Heading")))
            Pitch.desiredBearing = realToDisplayRadians(math.radians(sw.var.get("PitchPID.Heading")))
            Yaw.desiredBearing = realToDisplayRadians(math.radians(sw.var.get("YawPID.Heading")))
            Depth.setSlideValue( sw.var.get("DepthPID.Heading"))
"""
Sets all the horizontal sliders to their counterparts.
"""
def setSlidersToHubValues():
        Bow.setSlideValue( sw.var.get("Bow" ) )
        Stern.setSlideValue(sw.var.get("Stern"))
        Port.setSlideValue(sw.var.get("Port"))
        Star.setSlideValue(sw.var.get("Star"))
        StrafeT.setSlideValue(sw.var.get("StrafeT"))
        StrafeB.setSlideValue(sw.var.get("StrafeB"))
"""
GUI class contains a list of components such as dials, sliders, and buttons.
In the loop of the main program, move is called whenever a mouse event happens.
This checks how all components react when the program is clicked.
Draw draws each component. Titles are only drawn once.
"""
class GUI:
    def __init__(self):
        self.components = []

    def move(self, event, x, y, flags, param):
        global mouseX,mouseY
        for c in self.components:
                c.move(event, x, y, flags, param)

    def drawAll(self):
        for c in self.components:
                c.draw()

    def drawTitles(self):
            for c in self.components:
                c.drawTitle()

    def draw(self,i):
        x = self.X[i]
        y = self.Y[i]
"""
Writes a component's value to hub.
The component being written has a hub name, such as "RollPID.Heading"
and a value it is writing to hub. Dials write their desired bearing to hub,
sliders write their slide value to hub.
"""
def writeHub( component ):
        if component.change:
                if isinstance(component, Dial):
                        sw.var.set( component.hubName, float(displayToRealRadians(component.desiredBearing)))
                        component.change = False
                if isinstance(component, Slider):
                        sw.var.set( component.hubName, float(component.slideValue()))
                        component.change = False
                return True
        return False
"""
Sets all the sliders to zero, including forward and depth. Depth is set to actual depth.
"""
def zeroSliders():
        Depth.change = True
        Depth.setSlideValue(0)
        writeHub(Depth)
        Forward.setSlideValue(0)
        a = sw3.Forward(0)
        a.start()
        sw3.ZeroThrusters().start()
        setSlidersToHubValues()

"""
Main section of the program.
"""

seawolfIsRunning = True
delay = 5
             
if(seawolfIsRunning):
        sw.loadConfig("../../conf/seawolf.conf")
        sw.init("GUI") 
WIDTH = 500
HEIGHT = 1000
cv2.namedWindow('Control Panel')

rect(0, 0, WIDTH, HEIGHT, BACKGROUND_COLOR)
#limits of horizontal sliders
up = 1.0
down = -1.0


#Creating the components of the GUI.

Roll = Dial( 100, 460, 50, RED, "Roll", "RollPID.Heading")
Pitch = Dial( 300, 460, 50, RED, "Pitch", "PitchPID.Heading")
Yaw = Dial(100, 650, 50, RED, "Yaw", "YawPID.Heading" )

Bow = Slider( 40, 100, 150, 20, 100, 50, Horizontal, down, up, True, "Bow", "Bow" )

Stern = Slider( 240, 100, 150, 20, 100, 50, Horizontal, down, up, True, "Stern", "Stern" )
Port = Slider( 40, 200, 150, 20, 100, 50, Horizontal, down, up, True, "Port", "Port" )
Star = Slider( 240, 200, 150, 20, 100, 50, Horizontal, down, up, True, "Star", "Star" )
StrafeT = Slider( 40, 300, 150, 20, 100, 50, Horizontal, down, up, True, "StafeT", "StrafeT" )
StrafeB = Slider( 240, 300, 150, 20, 100, 50, Horizontal, down, up, True, "StrafeB", "StrafeB" )

Depth = Slider( 290, 590, 20, 150, 100, 50, Vertical, -3.0, .5, True, "Depth", "DepthPID.Heading" )
ActualDepth = Slider( 290, 590, 20, 150, 100, 50, Vertical, down, up, False, "", "" )
Forward = Slider( 40, 800, 150, 20, 100, 50, Horizontal, down, up, True, "Forward", "Forward" )

Pause = Button(250, 800, 100, 100)

Gui = GUI()

#adding named components to gui
Gui.components.append(Roll)
Gui.components.append(Pitch)
Gui.components.append(Yaw)

Gui.components.append(Bow)
Gui.components.append(Stern)
Gui.components.append(Port)
Gui.components.append(Star)
Gui.components.append(StrafeT)
Gui.components.append(StrafeB)

Gui.components.append(Depth)
Gui.components.append(ActualDepth)
Gui.components.append(Forward)

Gui.components.append(Pause)

Gui.drawTitles()

cv2.setMouseCallback('Control Panel', Gui.move)

count = 0

initializeValues()

reZeroSliders = False

#main loop of the gui
while( True ):
    #time.sleep(1)
    cv2.imshow('Control Panel', GUI_IMG)
    Gui.drawAll()
    k = cv2.waitKey(20) & 0xFF
    count += 1
    if count >= delay:
            count = 0

    if(seawolfIsRunning and count == 0):
            #setting values in seawolf to change

            #thruster sliders
            writeHub( Bow )
            writeHub( Stern )
            writeHub( Port )
            writeHub( Star )
            writeHub( StrafeT )
            writeHub( StrafeB )
            writeHub( Depth )
            #dials
            if Forward.change:
                a = sw3.Forward(Forward.slideValue())
                a.start()
                if abs(Forward.slideValue()) < 0.01:
                        a.cancel()
                Forward.change = False

            if( writeHub( Roll ) ):
                    setSlidersToHubValues()
            if( writeHub( Pitch ) ):
                    setSlidersToHubValues()
            if( writeHub( Yaw ) ):
                    setSlidersToHubValues()
            #changing values in gui read from seawolf
            Roll.actualBearing = realToDisplayRadians(math.radians(sw.var.get("SEA.Roll")))
            Pitch.actualBearing = realToDisplayRadians(math.radians(sw.var.get("SEA.Pitch")))
            Yaw.actualBearing = realToDisplayRadians(math.radians(sw.var.get("SEA.Yaw")))
            Roll.paused = sw.var.get("RollPID.Paused")
            Pitch.paused = sw.var.get("PitchPID.Paused")
            Yaw.paused = sw.var.get("YawPID.Paused")
            Depth.paused = sw.var.get("DepthPID.Paused")
            setVars()

            #print actual depth in red
            rect(330, 555, 80, 30, BACKGROUND_COLOR)
            textAt(330,580, str(round(sw.var.get("Depth"),2)), RED )
            #if sliders need to be reZeroed (for if zeroing the thrusters came undone)
            if reZeroSliders:
                    zeroSliders()
                    reZeroSliders = False
            if Pause.change:
                    Pause.change = False
                    if Pause.pressed == True:
                            #zero out dials

                            Roll.change = True
                            Roll.desiredBearing = -math.pi/2
                            writeHub(Roll)

                            Pitch.change = True
                            Pitch.desiredBearing = -math.pi/2
                            writeHub(Pitch)

                            Yaw.change = True
                            Yaw.desiredBearing = Yaw.actualBearing
                            writeHub(Yaw)
                            #zero out other sliders
                            zeroSliders()
                            reZeroSliders = True
    #if the k key is hit
    if k == 107 or k == 27 or cv2.getWindowProperty('Control Panel',1) < 1:
            sw.close()
            cv2.destroyWindow('Control Panel')
            break

