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

def in_range(n, minn, maxn):
    return max(min(maxn, n), minn)

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
        self.adaptive_thresh = 8   # 25: orange 15: yellow, 10-7: green
        
        self.shadow_thresh_blocksize =3 # 45: orange/yellow 55: green
        self.shadow_thresh = 20e6 # 20: orange/yellow, 15: green
        
        # Morphology variables
        self.erode_factor = 8 # 5: orange/yellow 3or7: green
        self.bloom_factor = 3

        # edge detection variables
        self.edge_threshold = 15    

        # Hough buoy variables
        self.inv_res_ratio = 2
        self.center_sep = 100
        self.upper_canny_thresh = 40 # 40
        self.acc_thresh = 75 # 20, 50 with green settings
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
        self.MAX_SEEN = 100

        self.next_id = 0

        # frames
        self.debug_frame = None

    def adaptive_threshold(self, in_frame, channel, blk_size, thresh, blur=0):
        if channel >= 3:
            in_frame = cv2.cvtColor(in_frame, cv2.COLOR_BGR2HSV) 
            channel -= 3

        # isolate channel
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


    
    def ROI_edge_detection(self, source_img, threshold_img, edge_threshold, channel, debug_img=None):
        # aquire edge detection target image.
        if channel > 5:
            raise IOError("channel %d unavailable" % channel)

        elif channel >= 3:
            channel      -= 3
            target_img = cv2.cvtColor(source_img, cv2.COLOR_BGR2HSV)
            target_img = target_img[:,:,channel]
        else:
            target_img = source_img[:,:,channel]

        BB_SIZE = 40
        drop = 5

        (buoy_contours,_) = cv2.findContours(threshold_img, 
                                cv2.RETR_LIST, 
                                cv2.CHAIN_APPROX_NONE)

        # Get a bounding box for all blobs in the image
        rect_list = []
        for cnt in buoy_contours:
            rect = cv2.boundingRect(cnt)
            rect_list.append(rect)

        # 
        edge_frame = target_img[:,:]*0
        blur_frame = cv2.medianBlur(target_img, 5)
        #edge_frame = cv2.Canny(edge_frame, 5, 100, apertureSize=3)
        #self.debug_stream("edgles", edge_frame)

        # get width and height
        (total_height, total_width, _) = source_img.shape
        for rect in rect_list:
            # blank frame
            drawing_frame = target_img[:,:]*0

            # get ROI
            (x,y,w,h) = rect
            bloom = int(BB_SIZE/2)
            x1 = in_range(x-bloom, 0, total_width)
            y1 = in_range(y-bloom, 0, total_height)
            x2 = in_range(x+w+bloom, 0, total_width)
            y2 = in_range(y+h+bloom+drop, 0, total_height)
            ROI = blur_frame[y1:y2,x1:x2]

            # run canny edge detection on ROI
            ROI = cv2.Canny(ROI, 0, edge_threshold)

            # add resuls on to composit image
            drawing_frame[y1:y2,x1:x2] = ROI

            #import pdb; pdb.set_trace()
            edge_frame = cv2.add(edge_frame,drawing_frame)


            if debug_img:
                (x,y,w,h) = rect
                bloom = int(BB_SIZE/2)
                pt1 = (x-bloom,y-bloom)
                pt2 = (x+w+bloom,y+h+bloom+drop)
                cv2.rectangle(source_img, pt1,pt2, (255,255,255))
                
        
        

        # final processing of the edge frame
        #edge_frame = self.morphology(edge_frame, [1,-1])

        if debug_img:
            #svr.debug("rects", source_img)
            self.debug_stream("help", source_img)
            self.debug_stream("edges", edge_frame)


        return edge_frame

    def detect_buoy(self,buoy,raw_frame,detection_frame):
        # generate some important variables
        buoy_centerx = int(buoy.centerx)
        buoy_centery = int(buoy.centery)
        buoy_radius = int(buoy.radius)
        buoy_id = str(buoy.id)

        white = (255,255,255)
        red = (0,0,255)
        green = (0,255,0)
        yellow = (0,255,255)
        
        standard_thickness = 5

        (frame_height, frame_width,_) = raw_frame.shape

        # draw a white cirle around the buoy, (assuming it's confirmed)
        (x,y) = (buoy_centerx,buoy_centery)
        cv2.circle(raw_frame, (x,y), buoy_radius+10, 
            color=white,
            thickness=5)
        
        # generate some other important variables
        sample_span = 1
        colorHue = None

        # generate the color pick point
        x = (in_range(buoy_centerx              , 0, frame_width))
        y = (in_range(buoy_centery-int(buoy_radius/2), 0, frame_height))

        # Generate ROI for average color detection
        x1 = in_range(x-sample_span, 0 , frame_width)
        x2 = in_range(x+sample_span, 0 , frame_width)
        y1 = in_range(y-sample_span, 0 , frame_height)
        y2 = in_range(y+sample_span, 0 , frame_height)
        color_ROI = detection_frame[y1:y2,x1:x2]
        cv2.rectangle( raw_frame, (x1,y1), (x2,y2), ( 0, 255, 255 ), -1,  8 );

        # detect color of buoy
        colorHue = np.mean(color_ROI)

        # print color if requested
        if BUOY_COLOR_PRINTS:
            print("buoy%d has a hue of %d" %(buoy.id,int(colorHue)))

        # generate some more variables
        (x,y) = (buoy_centerx,buoy_centery)
        if ((colorHue >= 0) and (colorHue < 45)) or (colorHue >= 95):
            buoy.color = "red"
            cv2.putText(raw_frame,
                text=buoy_id+'RED',
                org=(x,y),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5,
                color=red)
        elif (colorHue >= 80 and colorHue < 95):
            buoy.color = "green"
            cv2.putText(raw_frame,
                text=buoy_id+'GREEN',
                org=(x,y),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5,
                color=green)
        else:
            buoy.color = "yellow"
            cv2.putText(raw_frame,
                text=buoy_id+'YELLOW',
                org=(x,y),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5,
                color=yellow)
            
        # print general information
        cv2.putText(raw_frame,"HUE="+str(int(colorHue)), (x,y-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
        
        # return
        return raw_frame


    def process_frame(self, frame):
        # frame types:
        #self.debug_frame -- Frame containing helpful debug information

        # Debug numpy in CV2
        raw_frame        = libvision.cv_to_cv2(frame)
        self.debug_frame = raw_frame

        # CV2 blur
        blur_frame = cv2.medianBlur(self.debug_frame, 5)

        # collect brightly colored areas
        frame1 = self.adaptive_threshold(blur_frame, 4,
                                self.adaptive_thresh_blocksize,
                                self.adaptive_thresh)

        # collect shadowes under colored areas
        frame2 = self.adaptive_threshold(blur_frame, 1,
                                self.shadow_thresh_blocksize,
                                self.shadow_thresh)
        
        # use composite as the adaptive threshold
        adaptive_frame = cv2.add(frame1, frame2*0)
        frame          = adaptive_frame
        
        # morphology
        sequence = ([-self.erode_factor, self.erode_factor]*1 
                   +[self.bloom_factor, -self.bloom_factor]*1)

        despeckled_frame = self.morphology(frame, sequence)
        frame            = despeckled_frame

        self.debug_stream("despeckled", despeckled_frame)

        # collect edges
        # ROI_edge detection
        edge_frame = self.ROI_edge_detection(raw_frame, frame, self.edge_threshold, 0, True)
        
        # collect buoy candidates using hough circles
        self.raw_circles = []
        self.raw_buoys = []
        self.raw_circles = cv2.HoughCircles(
                                image   =edge_frame, 
                                method  =cv2.cv.CV_HOUGH_GRADIENT,
                                dp      =self.inv_res_ratio, 
                                minDist =self.center_sep,
                                param1  =self.upper_canny_thresh,
                                param2  =self.acc_thresh,
                                minRadius=self.min_radius,
                                maxRadius=self.max_radius,
                        )
        if self.raw_circles is not None:
            self.raw_circles = np.round(self.raw_circles[:,0]).astype(int)


        # create a new buoy object for every circle that is detected
        #print(self.raw_circles)
        if self.raw_circles is not None:
            #print self.confirmed
            for circle in self.raw_circles:
                (x, y, radius) = circle
                new_buoy = Buoy(x, y, radius, "unknown", self.next_id)
                self.next_id += 1
                self.raw_buoys.append(new_buoy) 
                self.match_buoys(new_buoy)

                cv2.circle(self.debug_frame, (x, y),
                            int(radius), (0, 255, 0), 5)

        # sort buoys among confirmed/canditates
        self.sort_buoys()
        
        # self.debug_frame= cv2.add(<HUD_FRAME>,cv2.cvtColor(<annotated_frame>, cv2.COLOR_GRAY2BGR) )
        # perform color detection
        self.hsv_frame = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2HSV)[:,:,:]
        if self.confirmed is not None and len(self.confirmed) > 0:
        
            # vvv start color detection 
            for buoy in self.confirmed:
                self.debug_frame = self.detect_buoy(buoy,self.debug_frame,self.hsv_frame)
                """
                # draw a cirle around the confirmed bouy
                cv2.circle(self.debug_frame, (int(buoy.centerx), int(buoy.centery)),
                            int(buoy.radius) + 10, (255, 255, 255), 5)
                           
                # attain hue from a pixel on the buoy
                color_pick_point = ( int(buoy.centerx), int(buoy.centery - buoy.radius/2) )
                _c  = color_pick_point
                # ^^offset a couple pixels upward for some reason
                (total_height, total_width, _) = self.hsv_frame.shape
                colorHue = np.mean(self.hsv_frame[in_range(_c[1]-buoy.radius/2,0,total_width) 
                                                    : in_range(_c[1]+buoy.radius/2, 0, total_width),
                                                  in_range(_c[0]-buoy.radius/2, 0, total_height) 
                                                    : in_range(_c[0]+buoy.radius/2, 0, total_height),
                                                     
                                                  0])
                print(_c[0],_c[1], buoy.radius/2)
                print(buoy.centery-20, buoy.centerx)
                
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
                
                
                #print(buoy.centerx)
                
                cv2.putText(self.debug_frame,"HUE="+str(int(colorHue)), (int(buoy.centerx), int(buoy.centery-20)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
                cv2.putText(self.debug_frame,"last_seen="+str(int(buoy.lastseen)), (int(buoy.centerx), int(buoy.centery-40)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
                cv2.putText(self.debug_frame,"candidate="+str(int(buoy in self.candidates)), (int(buoy.centerx), int(buoy.centery-60)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
           
            # ^^^ end color detection
                """

        # debug frames
        self.debug_to_cv = libvision.cv2_to_cv(self.debug_frame)
        #self.numpy_to_cv = libvision.cv2_to_cv(self.numpy_frame)
        self.adaptive_to_cv = libvision.cv2_to_cv(adaptive_frame)
        #svr.debug("processed", self.numpy_to_cv)
        svr.debug("adaptive", self.adaptive_to_cv)
        svr.debug("debug", self.debug_to_cv)

        # generate vision output
        FOV_x = 71.0
        FOV_y = 40.0
        x_resolution = frame.shape[1]
        y_resolution = frame.shape[0]


        self.output.buoys = []
        if self.confirmed is not None and len(self.confirmed) > 0:
            for buoy in self.confirmed:

                buoy.theta = (buoy.centerx - x_resolution/2.0) / (x_resolution/2.0) * (FOV_x/2.0) #<- a rough approximation
                buoy.phi = -(buoy.centery - y_resolution/2.0) / (y_resolution/2.0) * (FOV_y/2.0)  #<- a rough approximation
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
                buoy.lastseen = in_range(buoy.lastseen+10, -1, self.MAX_SEEN)
                found = 1
                
        for buoy in self.confirmed:
            if math.fabs(buoy.centerx - target.centerx) < self.conf_trans_thresh and \
               math.fabs(buoy.centery - target.centery) < self.conf_trans_thresh:
                buoy.centerx = target.centerx
                buoy.centery = target.centery
                buoy.lastseen = in_range(buoy.lastseen+10, -1, self.MAX_SEEN) #+ self.conf_trans_thresh
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
            
            if buoy.lastseen < (self.lastseen_thresh):
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
        
