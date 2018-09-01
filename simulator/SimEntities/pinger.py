import numpy as np
import math
import seawolf as sw
from dbEntity import dbEntity
import time


DB = False
NAME = "Pinger"

# speed of sound in ft/sec
SPEED_OF_SOUND = 1484;

pingerLength = 1
pingerWidth = .5
pingerDiameter = .5

# Location of each hydrophone in 3d space

cd = np.array([[0,       -0.1,   0],
               [0,       -0.119, 0],
               [0.0095,   0,     0],
               [-0.0095,  0,     0]])
                  
class Pinger(object):
    def __init__(self, at = [0, 0, 0]):
        self.location = np.float32(at)
        self.name = NAME
        length = np.float32([0, 0, 1]) * pingerLength
        width = np.float32([1, 0, 0]) * pingerWidth
        self.time= time.time()
        self.poles = []
        p1 = self.location - width/2
        p2 = self.location + width/2
        self.poles.append([p1, p2])
        
        self.color = (0, 255, 255)
        
        if DB:
            self.db = dbEntity(self.location, name = self.name)
    
        return

    
    def getAngle(self, location):
    
        pingerLoc = location

        (rows, cols) = np.shape(cd)
        distance = np.ones(rows)

        for i in range(rows):
            distance[i] = np.linalg.norm(cd[i] - pingerLoc)
            

        toa = np.divide(distance, SPEED_OF_SOUND)
        tdoa = np.array([[toa[1] - toa[0]], [toa[2] - toa[3]]])

        sideToSideDistance = np.linalg.norm(cd[3] - cd[2]) / 2
        inlineDistance = np.linalg.norm(cd[1] - cd[0]) /2 

        sideToSideA = tdoa[1] * SPEED_OF_SOUND / 2
        sideToSideB = math.sqrt(sideToSideDistance ** 2 - sideToSideA ** 2)

        inlineA = tdoa[0] * SPEED_OF_SOUND / 2
        inlineB = math.sqrt(inlineDistance ** 2 - inlineA ** 2)

        front = np.sign(inlineA)

        yaw = math.atan2(-sideToSideA, front * sideToSideB)
        pitch = math.atan2(inlineA, inlineB)
        
        return (np.rad2deg(yaw), np.rad2deg(pitch))

    def draw(self, roboPos, COBM, camera):
        #update yaw every 2 seconds
        if DB:
            print("TimeSinceLast: %.2f" % (time.time() - self.time))
        if time.time() - self.time > 2:
            self.time = time.time()
            (yaw, pitch) = self.getAngle(np.dot(COBM, self.location - roboPos))
            # Update the values in hub. Should this be moved to another function?
            sw.var.set("Acoustics.Pitch", pitch)
            sw.var.set("Acoustics.Yaw", yaw)
        
            if DB:
                self.db.draw(roboPos, COBM, camera)
                print("Yaw: " + str(yaw))
                print("Pitch: " + str(pitch))
            
        for pole in self.poles:
          pts  = []
          for pt in pole:
            pts.append(np.dot(COBM, pt - roboPos))
          camera.drawLine(pts[0], pts[1], color = self.color, thickness = pingerDiameter)
        return
     
     
    def loc(self):
        return self.location 


    def getName(self):
        return self.name 
