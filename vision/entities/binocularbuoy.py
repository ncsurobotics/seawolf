
from __future__ import division
import math
import entities
import cv

import libvision
from sw3.util import circular_average

#maximum buoy translation allowed between frames
MAX_X_TRANS = 40
MAX_Y_TRANS = 40

#maximum allowed change in width
MAX_CHANGE_WIDTH = 40

#how many frames a buoy may go missing before flagged as lost
CONFIRMED_BUOY_TIMEOUT = 5

#how many consequtive frames a candidate is allowed to go missing
CANDIDATE_BUOY_TIMEOUT = 3

#required seen threshold to accept a buoy
CANDIDATE_SEEN_THRESH = 3

#dictionaries of colors
COLORS = {0: cv.RGB(127, 127, 127),1:cv.RGB(255, 0, 0), 2: cv.RGB(0, 255, 0), 3: cv.RGB(255, 255, 0)}

class WorkerData(object):
    ''' used to pass data from worker to manager '''
    def __init__(self):
        pass

class ManagerData(object):
    ''' used to pass data from a manager to a class '''
    def __init__(self):
        pass

class Buoy(object):
    '''an imaged buoy'''
    def __init__(self):

        #Identification Number
        self.id = None

        #coordinates used by monocular algorithms
        self.x = None
        self.y = None

        #coordinate of upper left corner from left camera
        self.lx = None
        self.ly = None

        #coordinate of upper left corner from right camera
        self.rx = None
        self.ry = None

        #distance from robot
        self.distance = None

        #width
        self.width = None

        #Which Color we believe the buoy to be
        self.color = None

        #Frames since last sighting
        self.last_seen = None

        #Keeps track of how often we have seen this buoy
        self.seen_count = None

        #Color used in debug windows
        self.debug_color = None

class BinocularBuoyWorker(entities.VisionEntity):

    def init(self):

        # Thresholds
        self.minsize = 20
        self.maxsize = 60

        # List we store found buoys in
        self.new = []

        if self.debug:
            #windows
            cv.NamedWindow("Buoy Debug")

            #random number generator used for choosing debug colors
            self.rng = cv.RNG()

    def process_frame(self,frame):

        #----------- BLOCK 1: FIND NEW BUOYS ---------- #

        #find new buoys
        new_buoys = self.find_buoys(frame)

        #send found buoys back to manager
        buoy_data = WorkerData()
        buoy_data.new_buoys = new_buoys
        self.send_message(buoy_data)

        #---------- BLOCK 2: DEBUG ----------- #

        '''
        #######  DEBUG #######
        if self.debug:

            #display confirmed buoys
            for confirmed in self.confirmed:
                x = confirmed.x
                y = confirmed.y
                w = confirmed.width

                #draw rectangles on frame
                cv.Rectangle(frame, (x,y), (x+w, y+w), confirmed.debug_color, thickness = 6)
                cv.Rectangle(frame, (x,y), (x+w, y+w), COLORS[confirmed.color], thickness = -1)

            #show debug frame
            cv.ShowImage("Buoy Debug", frame)

        ####### END DEBUG #######
        '''

    def find_buoys(self, frame):
        # Get Channels
        hsv = cv.CreateImage(cv.GetSize(frame), 8, 3)
        cv.CvtColor(frame, hsv, cv.CV_BGR2HSV)
        grey = libvision.misc.get_channel(hsv, 2)

        # load a haar classifier
        hc = cv.Load("/home/seawolf/software/seawolf5/vision/buoy_cascade_4.xml")

        #use classifier to detect buoys
        minsize = (int(self.minsize), int(self.minsize))
        maxsize = (int(self.maxsize), int(self.maxsize))
        buoys = cv.HaarDetectObjects(grey, hc, cv.CreateMemStorage(), min_size = minsize, max_size = maxsize)

        #compute average buoy size and extract to a list
        new = []
        avg_w = 0
        for (x,y,w,h),n in buoys:

            #create a buoy class for this new buoys
            new_buoy = self.new_buoy(x,y,w)

            #make note of size
            avg_w = avg_w + w

            #add this buoy to our list of new buoys
            new.append(new_buoy)

        #update search size based on sizes found this frame
        if buoys:
            avg_w = avg_w / len(buoys)
            self.minsize = int(avg_w * .7)
            self.maxsize = int(avg_w * 1.3)

            #determine color of new buoys (if possible)
            #libvision.buoy_analyzer(frame, self.new)

        return new

    def new_buoy(self,x,y,w):
        '''intialize a new buoy'''
        new_buoy = Buoy()
        new_buoy.x = x
        new_buoy.y = y
        new_buoy.width = w
        new_buoy.last_seen = 0
        new_buoy.seen_count = 0

        return new_buoy

class BinocularBuoy(entities.MultiCameraVisionEntity):
    subprocess = BinocularBuoyWorker

    def init(self):
        # Total Number of Buoys Found
        self.buoy_count = 0

        # Average disparity across cameras
        self.avg_disparity = 0

        # Buoy Classes
        self.newLeft = []
        self.newRight = []
        self.candidates = []
        self.confirmed  = []
        self.lost = []

        if self.debug:
            #random number generator used for choosing debug colors
            self.rng = cv.RNG()

    def manage_workers(self):
        ''' walk workers through processing this frame'''

        #send capture singals to workers
        self.sync_capture()

        #wait for all workers to return new buoys
        worker_data = self.wait_for_workers()

        #assign new buoy data to self.newLeft and self.newRight
        #NOTE: FIRST CAMERA SPECIFIED == LEFT, SECOND CAMERA == RIGHT
        self.newLeft = worker_data[self.cameras_to_use[0]].new_buoys
        self.newRight = worker_data[self.cameras_to_use[1]].new_buoys

        print self.newLeft, self.newRight

        #sort new buoys into existing buoys
        self.sort_buoys()

        #make remaining new buoys candidates.  Pair buoys if possible.
        self.create_candidates()

        #compute the distance from confirmed buoys
        #update average disparity

        #pass debug information to workers for display

        #return the output attribute
        self.return_output()

    def sort_buoys(self):

        #perform upkeep on confirmed buoys
        for confirmed in self.confirmed:

            #increment how long ago we saw this buoy.  If it gets
            # matched, this number will be reset
            confirmed.last_seen += 1
            confirmed.seen_count -= 1

            #check if this buoy can be matched to a new buoy
            self.match_buoys(confirmed)

            #if this buoy hasn't been seen recently, mark it as lost
            if confirmed.last_seen > CONFIRMED_BUOY_TIMEOUT:
                self.lost.append(confirmed)
                self.confirmed.remove(confirmed)

        #perform upkeep on candidates
        for candidate in self.candidates:

            #increment how long ago we saw this buoy.  If it gets
            # matched, this number will be reset
            candidate.last_seen += 1
            candidate.seen_count -= 1

            #check if this buoy can be matched to a new buoy
            self.match_buoys(candidate)

            #if this buoy hasn't been seen recently, stop tracking
            if candidate.last_seen > CANDIDATE_BUOY_TIMEOUT:
                self.candidates.remove(candidate)

            #if seen count has grown large enough, accept this buoy
            if candidate.seen_count >= CANDIDATE_SEEN_THRESH:
                if self.debug:
                    #assign this buoy a debug color
                    r = int(cv.RandReal(self.rng)*255)
                    g = int(cv.RandReal(self.rng)*255)
                    b = int(cv.RandReal(self.rng)*255)
                    candidate.debug_color = cv.RGB(r,g,b)
                candidate.id = self.buoy_count
                self.buoy_count += 1
                self.confirmed.append(candidate)
                self.candidates.remove(candidate)

        #perform upkeep on lost buoys
        #TODO use lost buoys for anything, likely will depend on color

    def create_candidates(self):
        '''creates candidates out of new buoys, matching pairs if possible'''

        for lbuoy in self.newLeft:
            matched = False
            for rbuoy in self.newRight:
                if abs(lbuoy.x - rbuoy.x - self.avg_disparity) > MAX_X_TRANS:
                    continue
                if abs(lbuoy.y - rbuoy.y) > MAX_Y_TRANS:
                    continue
                if abs(lbuoy.width - rbuoy.width) > MAX_CHANGE_WIDTH:
                    continue

                #this is a match, create candidate buoy
                rbuoy.rx = rbuoy.x
                rbuoy.ry = rbuoy.y
                rbuoy.lx = lbuoy.x
                rbuoy.ly = lbuoy.y
                rbuoy.last_seen = 0
                rbuoy.seen_count = 2
                #TODO handle color
                self.candidates.append(rbuoy)
                self.newLeft.remove(lbuoy)
                self.newRight.remove(rbuoy)

                matched = True
                break

            if matched == False:
                #this left buoy didn't match anything, make it its own candidate
                lbuoy.lx = lbuoy.x
                lbuoy.ly = lbuoy.y
                lbuoy.rx = lbuoy.x - self.avg_disparity
                lbuoy.ry = lbuoy.y
                lbuoy.last_seen = 0
                lbuoy.seen_count = 1
                self.candidates.append(lbuoy)
                self.newLeft.remove(lbuoy)

        for rbuoy in self.newRight:
            #this right buoy didn't get matched, make it it's own candidate
            rbuoy.rx = rbuoy.x
            rbuoy.ry = rbuoy.y
            rbuoy.lx = rbuoy.x + self.avg_disparity
            rbuoy.ly = rbuoy.y
            rbuoy.last_seen = 0
            rbuoy.seen_count = 1
            self.candidates.append(rbuoy)
            self.newRight.remove(rbuoy)

    def match_buoys(self, target):
        '''matches buoys in the self.new list to a target buoy'''

        #check if any of the new buoys from left cam match target buoy
        for buoy in self.newLeft:
            if abs(buoy.x - target.lx) > MAX_X_TRANS:
                continue
            if abs(buoy.y - target.ly) > MAX_Y_TRANS:
                continue
            if abs(buoy.width - target.width) > MAX_CHANGE_WIDTH:
                continue

            #this is a match, update confirmed buoy
            target.color = buoy.color
            target.lx = buoy.x
            target.ly = buoy.y
            target.last_seen = 0
            target.seen_count += 2 #effectually increase by 1 if seen, -1 if not seen
            #TODO handle color

            #remove this new buoy that has been matched
            self.newLeft.remove(buoy)

        #check if any of the new buoys from right cam match target buoy
        for buoy in self.newRight:
            if abs(buoy.x - target.rx) > MAX_X_TRANS:
                continue
            if abs(buoy.y - target.ry) > MAX_Y_TRANS:
                continue
            if abs(buoy.width - target.width) > MAX_CHANGE_WIDTH:
                continue

            #this is a match, update confirmed buoy
            target.color = buoy.color
            target.rx = buoy.x
            target.ry = buoy.y
            target.width = buoy.width
            target.last_seen = 0
            target.seen_count += 2 #effectually increase by 1 if seen, -1 if not seen
            #TODO handle color

            #remove this new buoy that has been matched
            self.newRight.remove(buoy)
            break
