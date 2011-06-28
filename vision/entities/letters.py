import math
import time
import ctypes
import libvision
import cv

from collections import namedtuple
from entities.base import VisionEntity

class Bin(object):
    def __init__(self,type,center,angle,area):
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

    def initialize_non_pickleable(self,debug=True):

        if debug:
            #cv.NamedWindow("Filtered")
            cv.NamedWindow("Binary")
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
        cur_bins = [Bin(0,rect.center,rect.theta,rect.area) for rect in rects]

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
                cur_bins.append(Bin(letter,(blob.centroid[0],blob.centroid[1]),0,0))
            '''
            if debug and letter:
                #mark letters
                center = (blob.roi[0] + blob.roi[2]/2 , blob.roi[1] + blob.roi[3]/2)
                color = (0,0,0)
                if letter == 1:
                    color = (0,255,0)
                if letter == 2:
                    color = (0,0,255)
                cv.Circle(debug,center, 5, color, 2, 8, 0) 
            '''

        # Compare Bins 
        # --- tune-able values --- #
        max_travel = 50
        timeout_inc = 10
        promo_req = 15
        timeout_dec = 5 
        timeout_cap = 50
        type_count_thresh = 3
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

            # not a known bin, check candidates
            for candidate in self.candidates:
                #compute distance between bins
                x_dif = a_bin.center[0] - candidate.center[0]
                y_dif = a_bin.center[1] - candidate.center[1]
                tot_dif = math.sqrt(x_dif**2 + y_dif**2)
                
                if(tot_dif < max_travel):
                    #update this known_bin 
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
                self.candidates.remove(candidate)
            if(candidate.timeout >= promo_req):
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
                self.known_bins.remove(known_bin)
            #cap timeout
            if(known_bin.timeout > timeout_cap):
                known_bin.timeout = timeout_cap

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
                cv.Circle(debug,a_bin.center,radius,bin_color,2,8,0)

            cv.ShowImage("Binary",binary)
            #cv.ShowImage("Bins",bins)
            #cv.ShowImage("Filtered",filtered)
            cv.ShowImage("Python Debug",debug)

        return False 

    def __repr__(self):
        '''Convert this object to a string representation.

        This is used when printing the object.  It can be useful for debugging.
        The representation should contain at least all of the position and
        orientation information the object stores.

        '''
        return False # "<ExampleEntity position=%s>" % self.position
