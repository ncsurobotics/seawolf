"""
Group of functions for converting slide and degree values.
Also has functions for checking if a point is on a shape.
"""

import math

"""
Maps the value given on an input range to a scaled value on an output range. For instance, given the point 1 on the input scale 0 to 5,
you would want to set this to 2 on the output scale 0 to 10. This function takes parameters for the input point, input scale start, input
scale end, output scale start, and output scale end, and returns the matching point to the input point, but on the output scale.

p1 - point on input scale to be mapped
a - start of the input range
b - end of the input range
c - start of the output range
d - end of the output range
return input point scaled to output range
"""
def mapValTo(p1,a,b,c,d):
        return (p1-a)*(d-c)/(b-a)+c

"""
Determines if a point (xr, yr) is on the rectangle starting at (ox, oy) with a witdh of w and length of l.

xr - x coordinate of point potentially on the rectangle
yr - y coordinate of point potentially on the rectangle
ox - x coordinate of the origin of the rectangle
oy - y coordinate of the origin of the rectangle
w - width of the rectangle
l - length (or height) of the rectangle
return true if (xr, yr) is on the rectangle, false if not
"""
#is xr and yr on rect from ox,oy with width w and length l
def isOnSlider(xr,yr,ox,oy,w,l):
        if(ox <= xr and xr <= ox+w and oy <= yr and yr <= oy+l):
            return True
        return False

"""
Calculates the distance between (x1, y1) and (x2, y2) with the pythagorean theorem.

x1 - x coordinate of point 1
y1 - y coordinate of point 1
x2 - x coordinate of point 2
y2 - y coordinate of point 2
return distance between the 2 points
"""
def dist(x1,y1,x2,y2):
    return math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))

"""
Converts from the radians used to display on the dial to real radians.
"""
def displayToRealRadians(r):
        if(r < math.pi/2):
                return math.degrees(r + math.pi/2)
        if(r > math.pi/2):
                return math.degrees(r - 3*math.pi/2)
        return math.degrees(math.pi)
"""
Takes in a normal radian (0 through 2*PI ) and returns a radian that can be used to display a bearing.
"""
def realToDisplayRadians(r):
        if(r < 0):
                return r + 3*math.pi/2
        if(r > 0):
                return r - math.pi/2
        return -math.pi/2
"""
Converts a degree to real degrees.
"""
def toRealDegrees(d):
    d -= 90
    if d < 0:
        return d + 180
    if d >= 0:
        return d-180
    return 0
"""
Gets the heading between two points. Like atan2, but better.
"""
def heading(ox,oy,x,y):
    if(ox<x and oy<y):
        return math.pi-math.pi/2-math.atan2(x-ox,y-oy)
    if(x<ox and oy<y):
        return math.pi-math.pi/2-math.atan2(x-ox,y-oy)

    if(ox<x and y<oy):
        return math.pi-math.pi/2-math.atan2(x-ox,y-oy)
    if(x<ox and y<oy):
        return math.pi-math.pi/2-math.atan2(x-ox,y-oy)

    if(x==ox and y < oy):
        return math.pi+math.pi/2
    if(x==ox and y > oy):
        return math.pi/2
    if(x<ox and y == oy):
        return math.pi
    if(x>ox and y == oy):
        return 0
        
    return -math.pi