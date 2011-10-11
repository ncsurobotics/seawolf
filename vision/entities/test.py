import entities
import math
import cv
import libvision

class TestEntity(entities.VisionEntity):

    def init(self):
        cv.NamedWindow("Frame")
        cv.NamedWindow("Edges")
        cv.NamedWindow("Lines")
        cv.NamedWindow("Thresh")
 
    def process_frame(self, frame, debug=True):
        ''' process this frame, then place output in self.output'''

        if debug:
            #display frame
            cv.ShowImage("Frame", frame)

            #create a new image, the size of frame
            gray = cv.CreateImage(cv.GetSize(frame), 8, 1)
            edge = cv.CreateImage(cv.GetSize(frame), 8, 1)
            lines = cv.CloneImage(frame)

            #copy BW frame into binary
            cv.CvtColor(frame, gray, cv.CV_BGR2GRAY)

            # Get Edges
            cv.Canny(gray, edge, 60, 80)

            # Create a Binary Image
            binary = cv.CreateImage(cv.GetSize(frame), 8, 1)

            # Run Adaptive Threshold
            cv.AdaptiveThreshold(gray, binary,
                255,
                cv.CV_ADAPTIVE_THRESH_MEAN_C,
                cv.CV_THRESH_BINARY_INV,
                19,
                4,
            )

            #display adaptive threshold
            cv.ShowImage("Thresh", binary)

            # Hough Transform
            line_storage = cv.CreateMemStorage()
            raw_lines = cv.HoughLines2(edge, line_storage, cv.CV_HOUGH_STANDARD,
                rho=1,
                theta=math.pi/180,
                threshold=50,
                param1=0,
                param2=0
            )

            #process line data
            found_lines = []
            for line in raw_lines[:10]:
                found_lines.append((abs(line[0]),line[1]))
            print found_lines

            #display our transformed image
            cv.ShowImage("Edges", edge)

            #draw found lines
            libvision.misc.draw_lines(lines, found_lines)

            #display image with lines
            cv.ShowImage("Lines", lines)

            cv.WaitKey(10)

        self.output = "test data"

