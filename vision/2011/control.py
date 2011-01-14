
'''A set of intuitive functions and constants to control Seawolf's movements.

These functions work by setting libseawolf variables.  They must be used
after calling seawolf.loadConfig().

'''

import seawolf

# These constants correspond to constants in software/include/seawolf3.h
DEPTH_RELATIVE = 0
DEPTH_ABSOLUTE = 1
ROT_MODE_ANGULAR = 1
ROT_MODE_RATE = 2
ROT_MODE_RELATIVE = 3

def zero_movement():
    '''
    Zeros all headings and surfaces.
    '''
    set_depth(0, DEPTH_ABSOLUTE)
    set_yaw(0, ROT_MODE_RELATIVE)
    set_rho(0)

### Depth
def get_depth():
    '''
    Gets the current depth of the robot.
    '''
    return seawolf.var.get("Depth")

def set_depth(depth, depth_control):
    '''
    Sets depth relatively or absolutely
    accordingly.
    '''

    if depth_control is DEPTH_ABSOLUTE:
        set_depth_absolute(depth)
    elif depth_control is DEPTH_RELATIVE:
        set_depth_relative(depth)
    else:
        #TODO: Convert to seawolf.logging.log call
        print 'ERROR: depth_control incorrectly set to %f!!!' % depth_control

def set_depth_relative(depth):
    '''
    Sets the depth relative to the current depth.
    '''
    current_depth = seawolf.var.get("Depth")
    seawolf.var.set("DepthHeading", current_depth + depth)

def set_depth_absolute(depth):
    '''
    Sets the depth absolutely, independant to the current depth.
    '''
    seawolf.var.set("DepthHeading", depth)

### Yaw
def get_yaw():
    '''Gets the current yaw of th robot.'''
    return seawolf.var.get("SEA.Yaw")

def set_yaw(yaw, yaw_control):
    '''
    Sets Rot.Mode to yaw_control and updates yaw relatively or absolutely
    accordingly.
    '''

    if yaw_control is not yaw_control_cache:
        if yaw_control is ROT_MODE_RELATIVE:
            seawolf.var.set("Rot.Mode", ROT_MODE_ANGULAR)
        else:
            seawolf.var.set("Rot.Mode", yaw_control)
        yaw_control_cache = yaw_control
    if yaw_control is ROT_MODE_ANGULAR:
        set_yaw_absolute(yaw)
    elif yaw_control is ROT_MODE_RELATIVE:
        set_yaw_relative(yaw)
    elif yaw_control is ROT_MODE_RATE:
        set_yaw_rate(yaw)
    else:
        #TODO: Convert to seawolf.logging.log call
        print "ERROR: yaw_control incorrectly set to %f!!!" % yaw_control

def set_yaw_relative(yaw):
    '''
    Sets the yaw to the current yaw.
    '''
    current_yaw = seawolf.var.get("SEA.Yaw")
    seawolf.var.set("Rot.Angular.Target", current_yaw + yaw)

def set_yaw_absolute(yaw):
    '''
    Sets the yaw absolutely, independant to the current yaw.
    '''
    seawolf.var.set("Rot.Angular.Target", yaw)

def set_yaw_rate(yaw):
    '''
    '''
    seawolf.var.set("Rot.Rate.Target", yaw)

### Forward
def set_rho(rho):
    '''
    Sets the forward/backward speed.
    '''
    rho = seawolf.util.inRange(-THRUSTER_MAX, rho, THRUSTER_MAX)
    seawolf.notify.send("THRUSTER_REQUEST", "Forward %d %d" % (rho, rho))

### Reference Angle
def set_reference_angle(theta):
    '''Sets the reference angle.'''
    pass #TODO

def get_reference_angle():
    '''Gets the reference angle.'''
    pass #TODO
