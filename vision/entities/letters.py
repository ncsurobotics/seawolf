import math
import time
import ctypes
import libvision
import cv

from entities.base import VisionEntity

FILTER_TYPE = cv.CV_GAUSSIAN
FILTER_SIZE = 11
MIN_BLOB_SIZE = 11

class LettersEntity(VisionEntity):

    name = "LettersEntity"
    camera_name = "down"

    def __init__(self):

        self.xcenter = None 
        self.ocenter = None
        self.xscale = None
        self.oscale = None

    def initialize_non_pickleable(self,debug=True):

        if debug:
            cv.NamedWindow("Binary")
            cv.NamedWindow("Filtered")

    def find(self, frame, debug=True):

        #import pdb 
        #pdb.set_trace()

        filtered = cv.CreateImage(cv.GetSize(frame), 8, 3)
        cv.Smooth(frame, filtered, FILTER_TYPE, FILTER_SIZE, FILTER_SIZE) 
        
        #detect correctly colored regions
        binary = libvision.cmodules.target_color_hsv.find_target_color_hsv(frame, 179, 250, 250, 1, 800, 1.6)

        libvision.cmodules.shape_detect.detect_letters(binary)

        ''' #step through image, populatibg a list of found pixels
        pixels = []
        xsums = [0 for _ in xrange(binary.width)]
        ysums = [0 for _ in xrange(binary.height)]
        centroid = (0,0)
        pixelsum = 0
        data = binary.tostring()
        for y in xrange(0, binary.height):
            for x in xrange(0, binary.width): 
                index = y * binary.width * 3 + x
                b = ord(data[0 + index])
                g = ord(data[1 + index])
                r = ord(data[2 + index])
                
                #check to make sure this pixel was flagged by color detect 
                if b != 0xff or g != 0xff or r != 0xff: continue  

                #add this pixel to the list of found pixels
                pixels.append((x,y)) 

                #update the centroid calculation 
                centroid = (centroid[0] + x, centroid[1] + y)

                #update the pixel sums
                pixelsum += 1
                xsums[x] += 1
                ysums[y] += 1

        #finish the centroid calculation 
        centroid = (centroid[0] / pixelsum, centroid[1] / pixelsum)
        
        #collect upper and lower quartiles for x and y values
        up_y_quartile = -1
        low_y_quartile = -1
        up_x_quartile = -1
        low_x_quartile = -1 
        y_mid = -1
        x_mid = -1

        temp_ysum = 0
        for y in xrange(0, binary.height):
            temp_ysum += ysums[y] 
            if ( temp_ysum >= pixelsum / 4 and low_y_quartile == -1 ): 
                low_y_quartile = y 
            if ( temp_ysum >= pixelsum / 2 and y_mid == -1):
                y_mid = y
            if ( temp_ysum >= pixelsum * 3 / 4 and up_y_quartile == -1 ):
                up_y_quartile = y
                break         

        temp_xsum = 0
        for x in xrange(0, binary.width):
            temp_xsum += xsums[x]
            if ( temp_xsum >= pixelsum / 4 and low_x_quartile == -1 ):
                low_x_quartile = x
            if ( temp_xsum >= pixelsum / 2 and x_mid == -1):
                x_mid = x
            if ( temp_xsum >= pixelsum / 4 and up_x_quartile == -1):
                up_x_quartile = x
                break
        
        #use quartile data to compute an average radius 
        r1 =  x_mid - low_x_quartile 
        r2 = up_x_quartile - x_mid
        r3 = y_mid - low_y_quartile
        r4 = up_y_quartile - y_mid
        avg_radius = (r1 + r2 + r3 + r4) / 4         

        radii = []
        small_radii_count = 0
        #collect statistical data about found pixels reletive to middle
        for i, px in enumerate(pixels): 

            #compute radius 
            r = math.floor(((px[0] - x_mid) ** 2 + (px[1] - y_mid) ** 2) ** .5)    

            #add this to a list of the radii 
            radii.append(r) 

            #if this radius is 'small', make a note of it 
            if r < avg_radius / 2: 
                small_radii_count += 1

             #TODO: gather angular distribution data 
        '''   
        if debug:
            cv.ShowImage("Binary",binary)
            cv.ShowImage("Filtered",filtered)

        return False 

    def __repr__(self):
        '''Convert this object to a string representation.

        This is used when printing the object.  It can be useful for debugging.
        The representation should contain at least all of the position and
        orientation information the object stores.

        '''
        return False # "<ExampleEntity position=%s>" % self.position
