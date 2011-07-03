import math
import time
import ctypes
import libvision
import cv

from collections import namedtuple
from entities.base import VisionEntity

class Bin(object):
    def __init__(self,type,center,angle,area):
        #ID number used when tracking bins
        self.id = 0

        #decisive type of letter in the bin
        self.type = type

        #center of bin
        self.center = center

        #direction of the bin
        self.angle = angle

        #area of the bin
        self.area = area

        #tracks timeout for bin
        self.timeout = 10

        #tracks our type decisions
        self.type_counts = [0,0,0,0,0]

FILTER_TYPE = cv.CV_GAUSSIAN
FILTER_SIZE = 11
MIN_BLOB_SIZE = 11

class LettersEntity(VisionEntity):

    name = "LettersEntity"
    camera_name = "down"

    def __init__(self):

        self.known_bins = []
        self.candidates = []
        self.missing = []
        self.bins_seen = 0

    def initialize_non_pickleable(self,debug=True):

        if debug:
            #cv.NamedWindow("Filtered")
            #cv.NamedWindow("Binary")
            cv.NamedWindow("Python Debug")
            #cv.NamedWindow("Bins")

    def find(self, frame, debug=True):

        #import pdb 
        #pdb.set_trace()

        if debug:
            debug = cv.CreateImage(cv.GetSize(frame), 8, 3)
            debug = cv.CloneImage(frame)

        #look for bins (the black rectangles, not the X's and O's)
        rects = libvision.letters.find_bins(frame)

        #record rectangles(bins) found
        cur_bins = [Bin(0,(rect.center[0]-frame.width/2,frame.height/2-rect.center[1]),rect.theta,rect.area) for rect in rects]

        #detect correctly colored regions
        binary = libvision.cmodules.target_color_rgb.find_target_color_rgb(frame, 250, 0, 0, 500, 800, .3)
        
        #clean up the color detect
        cv.Dilate(binary,binary,None,1);
        cv.Erode(binary,binary,None,1);

        #collect blobs
        blob_indexed = cv.CreateImage(cv.GetSize(binary), 8, 1)
        blobs = libvision.blob.find_blobs(binary,blob_indexed,50,2)

        #check blobs for letters
        for i, blob in enumerate(blobs):
            #check if the blob is a letter  
            letter = libvision.cmodules.shape_detect.match_letters(blob_indexed, i+1, blob.centroid[0], blob.centroid[1],blob.roi[0],blob.roi[1],blob.roi[2],blob.roi[3])

            if(not letter): 
                continue

            #check to see if this letter is within a known bin
            letter_placed = False 
            for a_bin in cur_bins:
                radius = int( math.sqrt(a_bin.area/2) /2)
                x_dif = (blob.centroid[0]-a_bin.center[0])**2
                y_dif = (blob.centroid[1]-a_bin.center[1])**2
                tot_dif = math.sqrt(x_dif + y_dif)
                if ( tot_dif < radius ):
                    #this letter is in a rectangle!
                    a_bin.type = letter
                    letter_placed = True
                    break

            if( not letter_placed ):
                #make a new bin for this floating letter
                cur_bins.append(Bin(letter,(blob.centroid[0]-frame.width/2,frame.height/2-blob.centroid[1]),0,0))

        # Compare Bins 
        # --- tune-able values --- #
        max_travel = 60
        missing_travel = 100
        timeout_inc = 10
        promo_req = 15
        timeout_dec = 5 
        timeout_cap = 50
        type_count_thresh = 3
        missing_timeout =  200 
        # ------------------------ #

        #decide if we've seen any current bin before
        for a_bin in cur_bins:
            bin_recognized = False;

            # check known bin bins
            for known_bin in self.known_bins:
                #compute distance between bins
                x_dif = a_bin.center[0] - known_bin.center[0]
                y_dif = a_bin.center[1] - known_bin.center[1]
                tot_dif = math.sqrt(x_dif**2 + y_dif**2)
                
                if(tot_dif < max_travel):
                    #update this known_bin 
                    known_bin.timeout += timeout_inc
                    known_bin.type_counts[a_bin.type] += 1
                    known_bin.center = a_bin.center
                    if(a_bin.area):
                        known_bin.area = a_bin.area
                    bin_recognized = True;
                    break

            if(bin_recognized): 
                continue

            # check missing bins 
            for missing_bin in self.missing:
                #compute distance between bins
                x_dif = a_bin.center[0] - missing_bin.center[0]
                y_dif = a_bin.center[1] - missing_bin.center[1]
                tot_dif = math.sqrt(x_dif**2 + y_dif**2)
                
                if(tot_dif < missing_travel):
                    #re-instate this missing bin as a candidate
                    missing_bin.timeout = 10
                    self.candidates.append(missing_bin)
                    self.missing.remove(missing_bin)
                    bin_recognized = True

            if(bin_recognized):
                continue

            # not a known bin, check candidates
            for candidate in self.candidates:
                #compute distance between bins
                x_dif = a_bin.center[0] - candidate.center[0]
                y_dif = a_bin.center[1] - candidate.center[1]
                tot_dif = math.sqrt(x_dif**2 + y_dif**2)
                
                if(tot_dif < max_travel):
                    #update this candidate 
                    candidate.timeout += timeout_inc
                    candidate.type_counts[a_bin.type] += 1
                    candidate.center = a_bin.center
                    if(a_bin.area):
                        candidate.area = a_bin.area
                    bin_recognized = True
                    break;
             
            if(bin_recognized):
                continue

            # add this bin as a new candidate
            a_bin.type_counts[a_bin.type]+=1
            a_bin.type = 0
            self.candidates.append(a_bin)

        # promote / time out candidates 
        for candidate in self.candidates: 
            candidate.timeout -= timeout_dec
            if(candidate.timeout <= 0):
                if(candidate.id):
                    candidate.timeout = missing_timeout
                    self.missing.append(candidate)
                self.candidates.remove(candidate)
                continue
            if(candidate.timeout >= promo_req):
                if(candidate.id == 0):
                    self.bins_seen += 1
                    candidate.id = self.bins_seen  
                self.known_bins.append(candidate)
                self.candidates.remove(candidate)            

        # handle timeout of known bins
        for known_bin in self.known_bins:
            #select max type 
            #if greater than type thresh 
            #assign type
            if(not known_bin.type):
                for i,value in enumerate(known_bin.type_counts):
                    if(i and value >= type_count_thresh):
                        known_bin.type = i

            #decrement timeout
            known_bin.timeout -= timeout_dec
            #remove timed-out bins
            if(known_bin.timeout <= 0):
                known_bin.timeout = missing_timeout
                self.missing.append(known_bin)
                self.known_bins.remove(known_bin)
                continue
            #cap timeout
            if(known_bin.timeout > timeout_cap):
                known_bin.timeout = timeout_cap

        #decrement timeouts on missing bins
        for missing_bin in self.missing:
            missing_bin.timeout -= timeout_dec
            if(missing_bin.timeout <= 0):
                self.missing.remove(missing_bin)

        if debug:
            '''
            #draw circles to mark bins
            for a_bin in cur_bins:
                if(a_bin.area == 0):
                    continue
                radius = int( math.sqrt(a_bin.area/2) / 2);
                if(a_bin.type == 0):
                    bin_color = (255,0,255)
                elif(a_bin.type == 1):
                    bin_color = (0,255,0)
                elif(a_bin.type == 2):
                    bin_color = (0,0,255)
                cv.Circle(debug,a_bin.center,radius,bin_color,2,8,0)
                '''
            #draw circles to mark bins
            for a_bin in self.known_bins:
                if(a_bin.area == 0):
                    radius = 20
                else:
                    radius = int( math.sqrt(a_bin.area/2) / 2);
                if(a_bin.type == 0):
                    bin_color = (255,0,255)
                elif(a_bin.type == 1):
                    bin_color = (0,255,0)
                elif(a_bin.type == 2):
                    bin_color = (0,0,255)
                tmp_center = (a_bin.center[0]+frame.width/2,frame.height/2-a_bin.center[1])
                cv.Circle(debug,tmp_center,radius,bin_color,2,8,0)
                
                if (a_bin.id > 5):
                    self.bins_seen -= 5
                    a_bin.id -= 5
                if(a_bin.id == 1):
                    id_color = (0,0,0)
                elif(a_bin.id == 2):
                    id_color = (255,255,255)
                elif(a_bin.id == 3):
                    id_color = (120,120,120)
                elif(a_bin.id == 4):
                    id_color = (255, 0, 0)
                elif(a_bin.id == 5):
                    id_color = (0, 255, 255)
                else:
                    continue
                cv.Circle(debug,tmp_center,radius-2,id_color,2,8,0)

            #cv.ShowImage("Binary",binary)
            #cv.ShowImage("Bins",bins)
            #cv.ShowImage("Filtered",filtered)
            cv.ShowImage("Python Debug",debug)

        return len(self.known_bins) 

    def __repr__(self):
        '''Convert this object to a string representation.

        This is used when printing the object.  It can be useful for debugging.
        The representation should contain at least all of the position and
        orientation information the object stores.

        '''
        return False # "<ExampleEntity position=%s>" % self.position
