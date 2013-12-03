from __future__ import division
import math
import time
import itertools

import cv

import svr

from base import VisionEntity
import libvision

import sw3
from sw3.util import circular_average


class Path(object):
    def __init__(self, arg1, arg2):
        self.loc = arg1
        self.angle = arg2
        self.theta = arg2
        self.id = 0
        self.last_seen = 2
        self.seencount = 1
        


class PathManager(object):
    def __init__(self):
        self.paths = []       
        

    def get_paths(self):
        paths = filter(lambda path: path.count() >= self.min_path_count, self.paths)

        pairs = list(itertools.combinations(paths, 2))
        pairs.sort(key=lambda pair: pair[0].count() + pair[1].count(), reverse=True)

        for paths in pairs:
            if abs(circular_distance(paths[0].angle, paths[1].angle)) < self.max_angle_distance:
                return list(paths)

        return []

    def classify(self, lines):
        """ Segment the given lines and assign the line clusters to paths """

        paths = self.get_paths()

        if len(paths) < 2:
            return None

        for path in self.paths:
            path.lines = list()

        relative_lines = [(line, line[1]) for line in lines]

        for line, relative_angle in relative_lines:
            paths.sort(key=lambda path: abs(circular_distance(relative_angle, path.angle)))
            path = paths[0]
            if abs(circular_distance(relative_angle, path.angle)) < self.grouping_angle_threshold:
                path.lines.append(line)

        for path in paths:
            path.theta = sw3.util.circular_average([line[1] for line in path.lines], pi, 0)
            #print path, path.angle, path.lines, path.angles

        return paths

    def blob_in_path(self, path, x, y):
        if len(path.lines) == 0:
            return False

        rho_max = max([line[0] for line in path.lines])
        rho_min = min([line[0] for line in path.lines])
        r = sw3.util.euclid_distance((x, y), (0, 0))
        rho = r * math.cos(path.theta - math.atan2(y, x))

        if rho_min < rho < rho_max:
            return True

        return False

    def assign_blobs(self, paths, blobs):
        for path in paths:
            path.blobs = list()

        for blob in blobs:
            x, y = blob.centroid
            for path in paths:
                if self.blob_in_path(path, x, y):
                    path.blobs.append(blob)
                    path.verified = True
                    break

        return paths

    def process(self, lines, blobs):
        paths = self.classify(lines)

        if not paths:
            return None

        paths = self.assign_blobs(paths, blobs)
        paths = filter(lambda path: path.verified, paths)

        if len(paths) == 2:
            return paths
        else:
            return None

class DoublePath2Entity(VisionEntity):
    name = "DoublePath"
    
    def init(self):
        self.path_id = 0 
        self.path = None
        self.path_manager = PathManager()

        self.hough_threshold = 140
        self.lines_to_consider = 10
        print "it updated"

        path = []
        self.confirmed = []
        self.candidates = []
        self.min_seencount = 1
        self.max_lastseen = 5
        
        #Grouping Thresholds
        self.distance_threshold = 50
        self.angle_threshold = 1*math.pi

        #Transition Thresholds
        self.distance_trans = 1000
        self.angle_trans = 4*math.pi

        self.min_center_distance = 50
        


    def process_frame(self, frame):
        
        self.output.found = False

        cv.Smooth(frame, frame, cv.CV_MEDIAN, 7, 7)

        # Use RGB color finder
        binary = libvision.cmodules.target_color_rgb.find_target_color_rgb(frame, 250, 125, 0, 1500, 500, .3)
        color_filtered = cv.CloneImage(binary)

        blob_map = cv.CloneImage(binary)
        blobs = libvision.blob.find_blobs(binary, blob_map, min_blob_size=50, max_blobs=10)

        if not blobs:
            return

        binary = cv.CloneImage(blob_map)
        mapping = [0] * 256
        for blob in blobs:
            mapping[blob.id] = 255
        libvision.greymap.greymap(blob_map, binary, mapping)

        # Get Edges
        cv.Canny(binary, binary, 30, 40)

        # Hough Transform
        line_storage = cv.CreateMemStorage()
        lines = cv.HoughLines2(binary, line_storage, cv.CV_HOUGH_STANDARD,
                               rho=1,
                               theta=math.pi/180,
                               threshold=self.hough_threshold,
                               param1=0,
                               param2=0
        )
        print "hough transform found", len(lines), " lines"
        lines = lines[:self.lines_to_consider] # Limit number of lines

        #if not lines:
        #    return

        paths = self.path_manager.process(lines, blobs)

        if paths and not self.path:
            # If path[1] is clockwise of paths[0]
            distance = circular_distance(paths[0].angle, paths[1].angle)
            
            if distance > 0:
                self.path = paths[self.which_path]
            else:
                self.path = paths[1 - self.which_path]

            
        if paths and self.path in paths and self.path.blobs:
        
            temp_map = cv.CloneImage(blob_map)

            mapping = [0] * 256
            for blob in self.path.blobs:
                mapping[blob.id] = 255
            libvision.greymap.greymap(blob_map, temp_map, mapping)
            center = self.find_centroid(temp_map)

            svr.debug("map", temp_map)

            self.path.center = (
                 center[0] - (frame.width / 2),
                -center[1] + (frame.height / 2)
            )

            
        random = 0
        if random == 0:
            # Show color filtered
            color_filtered_rgb = cv.CreateImage(cv.GetSize(frame), 8, 3)
            cv.CvtColor(color_filtered, color_filtered_rgb, cv.CV_GRAY2RGB)
            cv.SubS(color_filtered_rgb, (255, 0, 0), color_filtered_rgb)
            cv.Sub(frame, color_filtered_rgb, frame)

            # Show edges
            binary_rgb = cv.CreateImage(cv.GetSize(frame), 8, 3)
            cv.CvtColor(binary, binary_rgb, cv.CV_GRAY2RGB)
            cv.Add(frame, binary_rgb, frame) # Add white to edge pixels
            cv.SubS(binary_rgb, (0, 0, 255), binary_rgb)
            cv.Sub(frame, binary_rgb, frame) # Remove all but Red
            test_lines = []
            new_path = None
            
            for line in lines[:]:
                if self.candidates == []:
                    new_path = Path(line[0], line[1])
                    new_path.id= self.path_id
                    self.path_id += 1
                    new_path.last_seen += 1
                    self.candidates.append(new_path)
                    print "got a candidate"
            for candidate in self.candidates:
                if len(self.confirmed) == 0:
                    self.confirmed.append(candidate)
                    
            for line in lines[:]:
                for candidate in self.candidates:
                    if math.fabs(line[0]-candidate.loc) < self.distance_threshold and \
                       math.fabs(line[1]-candidate.angle) < self.angle_threshold:
                        candidate.loc = (candidate.loc+line[0])/2
                        candidate.angle = (candidate.angle+line[1])/2
                        if candidate.last_seen < self.max_lastseen:
                                candidate.last_seen += 1
                        #print line1
                        
                        if line in lines:
                            lines.remove(line)
                    else: 
                        new_path = Path(line[0], line[1])
                        new_path.id= self.path_id
                        self.path_id += 1
                        new_path.last_seen += 1
                        new_path.seencount +=5
                        self.candidates.append(new_path)
                        
            for candidate in self.candidates [:]:
                candidate.last_seen -= 1
                if candidate.seencount > self.min_seencount:
                    self.confirmed.append(candidate)
                    self.candidates.remove(candidate)
                if candidate.last_seen == -1:
                    self.candidates.remove(candidate)

            for confirmed in self.confirmed:
                for line in lines[:]:
                    if math.fabs(line[0]-confirmed.loc) < self.distance_trans and \
                       math.fabs(line[1]-confirmed.angle) < self.angle_trans: 
                        confirmed.loc = line[0]
                        confirmed.angle = line[1]
                        if confirmed.last_seen < self.max_lastseen:
                                confirmed.last_seen += 2
                        
                        if line in lines:
                            self.lines.remove(line)
                            print "line removed"
            
            for confirmed in self.confirmed:
                for candidate in self.candidates[:]:
                    if math.fabs(candidate.loc-confirmed.loc) < self.distance_trans and \
                       math.fabs(candidate.angle-confirmed.angle) < self.angle_trans: 
                        confirmed.loc = candidate.loc
                        confirmed.angle = candidate.angle
                        if confirmed.last_seen < self.max_lastseen:
                                confirmed.last_seen += 2
                        
                        print "lines"
                        if candidate in self.candidates:
                            self.candidates.remove(candidate)
                            print "line removed"
            
            for confirmed1 in self.confirmed[:]:
                for confirmed2 in self.confirmed[:]:
                    if math.fabs(confirmed1.loc-confirmed2.loc) < self.distance_threshold and \
                       math.fabs(confirmed1.angle-confirmed2.angle) < self.angle_threshold: 
                        if confirmed1.id > confirmed2.id and confirmed1 in self.confirmed:
                            confirmed2.loc == (confirmed2.loc+confirmed1.loc)/2
                            confirmed2.angle == (confirmed2.angle + confirmed1.angle)/2
                            self.confirmed.remove(confirmed1)
                            if confirmed2.last_seen < self.max_lastseen:
                                confirmed2.last_seen += 2
                        if confirmed2.id > confirmed1.id and confirmed2 in self.confirmed:
                            confirmed2.loc == (confirmed2.loc+confirmed1.loc)/2
                            confirmed2.angle == (confirmed2.angle + confirmed1.angle)/2
                            self.confirmed.remove(confirmed2)
                            if confirmed1.last_seen < self.max_lastseen:
                                confirmed1.last_seen += 2
            
    

            for confirmed in self.confirmed[:]:
                confirmed.last_seen -= 1
                if confirmed.last_seen < -10:
                    self.confirmed.remove(confirmed)
                         
            

            final_lines = []
            for confirmed in self.confirmed:
                final_line = [confirmed.loc, confirmed.angle]
                final_lines.append(final_line)
                print confirmed.id
            candidate_ids = []
            for candidate in self.candidates:
                new_id = candidate.id
                candidate_ids.append(new_id)
            print candidate_ids
            print len(self.candidates)
            

            libvision.misc.draw_lines(frame, final_lines)
            #libvision.misc.draw_lines2(frame, lines)              
            print "Number of Paths:", len(self.confirmed)
            print "Number of Candidates:",len(self.candidates)
            #type -s after the command to run vision for this to work and not produce errors.
            #if len(self.confirmed)>1:
            #    raw_input()
            

            self.output.paths = []
            center_x = 0
            center_y = 0
            self.output.paths = self.confirmed
            
            for path in self.output.paths:
                path.theta = path.angle
                center_x = frame.width/2
                path.x = center_x
                center_y = (-math.cos(path.angle)/(math.sin(path.angle)+.001))*center_x+(path.loc/((math.sin(path.angle)+.001)))
                path.y = center_y
                if center_y > frame.height or center_y < 0 or \
                   center_y < self.min_center_distance or \
                   frame.height-center_y < self.min_center_distance:
                    center_y2 = frame.height/2
                    center_x2 = (center_y2-(path.loc/(math.sin(path.angle)+.0001)))/(-math.cos(path.angle)/(math.sin(path.angle)+.0001)) 
             
                    if center_x2 > frame.width or center_x2 < 0:
                        path.center = [center_x, center_y]
                    else:
                        path.center = [center_x2, center_y2]
                else: path.center = [center_x, center_y]

                cv.Circle(frame, (int(path.center[0]),int(path.center[1])), 15, (255,255,255), 2,8,0)
                
            

            self.return_output()
            svr.debug("Path", frame)

            
    def find_centroid(self, binary):
        mat = cv.GetMat(binary)
        moments = cv.Moments(mat)
        return (int(moments.m10/moments.m00),
                int(moments.m01/moments.m00))