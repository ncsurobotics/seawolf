from __future__ import division
import math
import cv2
import cv2.cv as cv
import numpy as np
import svr
from base import VisionEntity, Container
import itertools
from sets import Set
import libvision

BUOY_COLOR_PRINTS = False


class Buoy(object):
    buoy_id = 0
    colors = {"red": (40, 0, 255),
              "green": (0, 255, 0),
              "blue": (255, 0, 0),
              "orange": (0, 200, 255),
              "unknown": (255, 255, 255),
              }

    def __init__(self, xcoor, ycoor, radius, color, id):
        self.type = "buoy"
        self.centerx    = xcoor
        self.centery    = ycoor
        self.radius     = radius
        self.color      = color
        self.area       = 0
        self.id = id        # id identifies which buoy your looking at
        self.lastseen = 2  # how recently you have seen this buoy
        # how many times you have seen this buoy (if you see it enough it
        # becomes confirmed)
        self.seencount = 1

    def get_color(self):
        try:
            return Buoy.colors[self.color]
        except KeyError:
            return Buoy.colors["unknown"]


class BuoyHoughEntity(VisionEntity):

    def init(self):

        # Adaptive threshold variables
        self.adaptive_thresh_blocksize = 49 # 55: yellow, orange, 55: green
        self.adaptive_thresh = 10   # 25: orange 15: yellow, 10-7: green
        
        self.shadow_thresh_blocksize =3 # 45: orange/yellow 55: green
        self.shadow_thresh = 20e6 # 20: orange/yellow, 15: green
        
        #
        self.erode_factor = 10 # 5: orange/yellow 3or7: green
        self.bloom_factor = 3

        # Hough buoy variables
        self.inv_res_ratio = 2
        self.center_sep = 100
        self.upper_canny_thresh = 40 # 40
        self.acc_thresh = 50 # 20, 50 with green settings
        self.min_radius = 5
        self.max_radius = 50

        self.recent_id = 1
        self.trans_thresh = 20

        self.conf_trans_thresh = 150

        self.growth_thresh = 20

        self.candidates = []
        self.confirmed = []

        self.lastseen_thresh = 0
        self.seencount_thresh = 9

        self.next_id = 0

        # frames
        self.debug_frame = None

    def adaptive_threshold(self, in_frame, channel, blk_size, thresh, blur=0):
        frame = in_frame[:,:,channel]

        # Thresholding
        frame = cv2.adaptiveThreshold(frame, 255,
                        cv2.ADAPTIVE_THRESH_MEAN_C,
                        cv2.THRESH_BINARY_INV,
                        blk_size,
                        thresh)
                                                 
        # return
        return frame

    
    def morphology(self, frame, sequence):

        for val in sequence:
            # perform transformation
            if val > 0:
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (val, val))
                frame = cv2.dilate(frame, kernel)
            elif val < 0:
                val = -val
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (val, val))
                frame = cv2.erode(frame, kernel)
            else:
                pass #do nothing

        return frame


    
    def ROI_edge_detection(self, source_img, threshold_img, debug_img=None):
        BB_SIZE = 40
        (buoy_contours,_) = cv2.findContours(threshold_img, 
                                cv2.RETR_LIST, 
                                cv2.CHAIN_APPROX_NONE)

        # Get a bounding box for all blobs in the image
        rect_list = []
        for cnt in buoy_contours:
            rect = cv2.boundingRect(cnt)
            rect_list.append(rect)

        #
        edge_frame = source_img[:,:,0]*0
        blur_frame = cv2.medianBlur(source_img, 7)
        #edge_frame = cv2.Canny(edge_frame, 5, 100, apertureSize=3)
        #self.debug_stream("edgles", edge_frame)

        for rect in rect_list:
            # blank frame
            drawing_frame = source_img[:,:,0]*0

            # get ROI
            (x,y,w,h) = rect
            bloom = int(BB_SIZE/2)
            x1 = x-bloom
            y1 = y-bloom
            x2 = x+w+bloom
            y2 = y+h+bloom
            ROI = blur_frame[y1:y2,x1:x2,:]

            # run canny edge detection on ROI
            ROI = cv2.Canny(ROI, 20, 40)

            # add resuls on to composit image
            drawing_frame[y1:y2,x1:x2] = ROI

            #import pdb; pdb.set_trace()
            edge_frame = cv2.add(edge_frame,drawing_frame)


            if debug_img:
                #import pdb; pdb.set_trace()
                (x,y,w,h) = rect
                bloom = int(BB_SIZE/2)
                pt1 = (x-bloom,y-bloom)
                pt2 = (x+w+bloom,y+h+bloom)
                cv2.rectangle(source_img, pt1,pt2, (255,255,255))
                
        
        if debug_img:
            #svr.debug("rects", source_img)
            self.debug_stream("help", source_img)
            self.debug_stream("edgles", edge_frame)
            
            pass

        return edge_frame

    def process_frame(self, frame):
        # frame directors
        #self.debug_frame -- Frame containing helpful debug information

        # Debug numpy in CV2
        raw_frame        = libvision.cv_to_cv2(frame)
        self.debug_frame = raw_frame

        # CV2 blur
        blur_frame = cv2.medianBlur(self.debug_frame, 5)
        hsv_blur_frame = 


        # collect brightly colored areas
        frame1 = self.adaptive_threshold(blur_frame, 0,
                                self.adaptive_thresh_blocksize,
                                self.adaptive_thresh)

        # collect shadowes under colored areas
        frame2 = self.adaptive_threshold(blur_frame, 1,
                                self.shadow_thresh_blocksize,
                                self.shadow_thresh)
        
        # use composite as the adaptive threshold
        adaptive_frame = cv2.add(frame1, frame2*0)
        frame          = adaptive_frame
        
        #self.debug_stream("help", <frame>)
        

        
        # morphology
        sequence = ([-self.erode_factor, self.erode_factor]*1 
                   +[self.bloom_factor, -self.bloom_factor]*1)

        despeckled_frame = self.morphology(frame, sequence)
        frame            = despeckled_frame

        self.debug_stream("despeckled", despeckled_frame)

        # collect edges
        #a = 800
        # TODO: ROI_edge detection
        edge_frame = self.ROI_edge_detection(raw_frame, frame, True)
   

        #edge_frame = cv2.Canny(frame, 150, 250, apertureSize=3)
        
        
        # collect buoy candidates using hough circles
        self.raw_circles = []
        self.raw_buoys = []
        self.raw_circles = cv2.HoughCircles(
                                edge_frame, 
                                cv2.cv.CV_HOUGH_GRADIENT,
                                self.inv_res_ratio, 
                                self.center_sep,
                                np.array([]),
                                self.upper_canny_thresh,
                                self.acc_thresh,
                                self.min_radius,
                                self.max_radius,
                        )
  
        # create a new buoy object for every circle that is detected
        if self.raw_circles is not None and len(self.raw_circles[0] > 0):
            #print self.confirmed
            for circle in self.raw_circles[0]:
                (x, y, radius) = circle
                new_buoy = Buoy(x, y, radius, "unknown", self.next_id)
                self.next_id += 1
                self.raw_buoys.append(new_buoy) 
                self.match_buoys(new_buoy)

        # sort buoys among confirmed/canditates
        self.sort_buoys()
        
        # self.debug_frame= cv2.add(<HUD_FRAME>,cv2.cvtColor(<annotated_frame>, cv2.COLOR_GRAY2BGR) )
        # perform color detection
        if self.confirmed is not None and len(self.confirmed) > 0:
        
            # vvv start color detection 
            for buoy in self.confirmed:
                # draw a cirle around the confirmed bouy
                cv2.circle(self.debug_frame, (int(buoy.centerx), int(buoy.centery)),
                            int(buoy.radius) + 10, (255, 255, 255), 5)
                           
                # attain hue from a pixel on the buoy
                color_pick_point = ( int(buoy.centerx), int(buoy.centery - buoy.radius/2) )
                _c  = color_pick_point
                # ^^offset a couple pixels upward for some reason
                colorHue = np.mean(self.hsv_frame[_c[1]-buoy.radius/2 : _c[1]+buoy.radius/2, 
                                                  _c[0]-buoy.radius/2 : _c[0]+buoy.radius/2, 
                                                  0])
                
                if BUOY_COLOR_PRINTS:
                    print("buoy%d has a hue of %d" %(buoy.id,int(colorHue)))
                
                # note: color wraps around at 180. Range is 0->180
                if (colorHue >= 0 and colorHue < 45) or colorHue >= 95: # 105->180->45
                    cv2.putText(self.debug_frame,str(buoy.id)+"RED", (int(buoy.centerx), int(buoy.centery)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
                    buoy.color = "red"
                elif (colorHue >= 80 and colorHue < 95): # green is hardest to detect
                    cv2.putText(self.debug_frame,str(buoy.id)+"GRE", (int(buoy.centerx), int(buoy.centery)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
                    
                    #if buoy.color != "red" and buoy.color != "yellow":
                    #print "switched from ", buoy.color
                    buoy.color = "green"
                        
                else: #yellow is about 50->80
                    cv2.putText(self.debug_frame,str(buoy.id)+"YEL", (int(buoy.centerx), int(buoy.centery)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
                    buoy.color = "yellow"
                
                cv2.putText(self.debug_frame,"HUE="+str(int(colorHue)), (int(buoy.centerx), int(buoy.centery-20)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
           
            # ^^^ end color detection

        # debug frames
        self.debug_to_cv = libvision.cv2_to_cv(self.debug_frame)
        #self.numpy_to_cv = libvision.cv2_to_cv(self.numpy_frame)
        self.adaptive_to_cv = libvision.cv2_to_cv(adaptive_frame)
        #svr.debug("processed", self.numpy_to_cv)
        svr.debug("adaptive", self.adaptive_to_cv)
        svr.debug("debug", self.debug_to_cv)

        # generate vision output
        self.output.buoys = []
        if self.confirmed is not None and len(self.confirmed) > 0:
            for buoy in self.confirmed:
                buoy.theta = buoy.centerx #<- a rough approximation
                buoy.phi = buoy.centery   #<- a rough approximation
                buoy.id = buoy.id
                self.output.buoys.append(buoy)

        # publish output
        #print ("%d buoys currently confirmed." % len(self.confirmed))
        if self.output.buoys:
            self.return_output()
        return self.output


    # TODO, CLEAN THIS UP SOME
    def match_buoys(self, target):
        found = 0
        for buoy in self.candidates:
            if math.fabs(buoy.centerx - target.centerx) < self.trans_thresh and \
               math.fabs(buoy.centery - target.centery) < self.trans_thresh:
                #print buoy.seencount
                buoy.centerx = target.centerx
                buoy.centery = target.centery
                #print "still ", buoy.seencount
                buoy.seencount += 1
                #print "new seencount ", buoy.seencount
                buoy.lastseen += 10
                found = 1
                
        for buoy in self.confirmed:
            if math.fabs(buoy.centerx - target.centerx) < self.conf_trans_thresh and \
               math.fabs(buoy.centery - target.centery) < self.conf_trans_thresh:
                target.id = buoy.id
                buoy = target
                buoy.lastseen += 10
                found = 1
                
        if found == 0:
            self.candidates.append(target)
            target.lastseen + 3

    # TODO, CLEAN THIS UP SOME
    def sort_buoys(self):
        # go through all candidate buoys. promote any that have been seen
        # enough times. or remove any that have not been seen in a while.
        for buoy in self.candidates[:]:
            #print "last seen is ", buoy.lastseen
            #print "seencount is ", buoy.seencount
            buoy.lastseen -= 1
            
            if buoy.seencount >= self.seencount_thresh:
                self.confirmed.append(buoy)
                #print "confirmed appended"
                
            if buoy.lastseen < self.lastseen_thresh:
                self.candidates.remove(buoy)
                
        # go through all confirmed buoys, and remove it if it hasn't been
        # seen in a while.
        for buoy in self.confirmed[:]:
            buoy.lastseen -= 1
            
            if buoy.lastseen < self.lastseen_thresh:
                self.confirmed.remove(buoy)
                #self.candidates.append(buoy)
                #print "confirmed removed"
                
 
        # remove easy to catch duplicates
        self.confirmed = list(Set(self.confirmed))

        for (buoy1,buoy2) in itertools.combinations(self.confirmed,2):
        
            # spatially check if any elements are the same
            if math.fabs(buoy1.centerx - buoy2.centerx) < self.conf_trans_thresh and \
                math.fabs(buoy1.centery - buoy2.centery) < self.conf_trans_thresh:
                
                # if buoy 1 was discoverd first, keep it.
                if buoy1.id < buoy2.id:
                    # check if element has already been removed
                    if buoy2 in self.confirmed:
                        self.confirmed.remove(buoy2)
                        #print "removed buoy2"
                        
                # otherwise keep buoy 2.
                else:
                    # check if element has already been removed
                    if buoy1 in self.confirmed:
                        self.confirmed.remove(buoy1)
                        #print "removed buoy1"
        
