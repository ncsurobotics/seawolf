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

    def display(self,frame):
        #Draws objects on frame


    def process_frame(self, frame): 

        #Image treatment here (frame is input picture in cv format)

        #Identify Objects

        
        #Group objects


        #Track Objects


        #Return objects to mission control


        #Display output


