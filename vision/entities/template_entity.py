import cv
import cv2
import svr
from base import VisionEntity
import libvision

#add any other imports here

class ???Entity(VisionEntity):

    def init(self):
        #Define thresholds
        #Define objects lists (examples: this.candidates, this.confirmed, etc)
        self.candidates = []
        self.confirmed = []

    def groupTarget(self, target):
        #Use this function to group the target into the appropriate group

    def groupCandidates(self): '''Optional'''
        #check candidates to see if they should be used to update a confirmed
    
    def track(self):
        #Check confirmed list and move to candidates if lastseen is too high

        #Check candidates list and upgrade to confirmed if seencount is high

        #Check candidates and remove from list if lastseen is too high

        #Update lastseen on candidates and confirmed (add designated amount)

    def returnToMissionControl(self):
        #Goes through confirmed list and returns necessary info to mission control

    def display(self):
        #Draws objects on frames


    def process_frame(self, frame): 

        #Image treatment here (frame is input picture in cv format)

        targets = cv.???(frame) #Find objects using an opencv function

        for target in targets: #Look at each target
            groupTarget(self, target) #Group each target

        track() #Track objects using confirmed and candidate lists

        returnToMissionControl() #Return information to mission control

        display() #Draw objects and display frames


