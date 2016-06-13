# How to use this script:
# This script is meant to run while the user
# has joystick_controller.py running, whereby
# the user can issue navigation commands and
# new PID target/heading values remotely.

# Explanation of controls
# Imagine the following keys as a 3x3 grid,
# which they are on typical key board:
#     (1) (2) (3)
# (1)  w   e   r
# (2)  s   d   f
# (3)  x   c   v
#
# column1 controls depth, 2 controls pitch, and 3 Yaw.
# row1 controls p, 2 controls i, and 3 d.
# pressing one of the keys will increment the corresponding
# PID parameter. To decrement the parameter, hold shift while
# pressing the key. 
#
# The "i" key will toggle the increment value between fine
# and coarse.
#
# The "q" key will quit the program
#
# Note: make sure there is some other program running that will
# frequently update one of the IMU-related variables, such as serialapp
# (with IMU connected), else the program will hang indefinately,
# because all seawolf.var.sync() commands are blocking functions.



import seawolf
import curses
import sys
import numpy as np

seawolf.loadConfig("../conf/seawolf.conf")
seawolf.init("PID")

#YAW
seawolf.var.subscribe("YawPID.p")
seawolf.var.subscribe("YawPID.i")
seawolf.var.subscribe("YawPID.d")
seawolf.var.subscribe("YawPID.Heading")
seawolf.var.subscribe("YawPID.Paused")
seawolf.var.subscribe("SEA.Yaw")

#DEPTH
seawolf.var.subscribe("DepthPID.p")
seawolf.var.subscribe("DepthPID.i")
seawolf.var.subscribe("DepthPID.d")
seawolf.var.subscribe("DepthPID.Heading")
seawolf.var.subscribe("DepthPID.Paused")
seawolf.var.subscribe("Depth")

#subscribe to PITCH PID
seawolf.var.subscribe("PitchPID.p")
seawolf.var.subscribe("PitchPID.i")
seawolf.var.subscribe("PitchPID.d")
seawolf.var.subscribe("PitchPID.Heading")
seawolf.var.subscribe("PitchPID.Paused")
seawolf.var.subscribe("SEA.Pitch")

#Roll
seawolf.var.subscribe("RollPID.p")
seawolf.var.subscribe("RollPID.i")
seawolf.var.subscribe("RollPID.d")
seawolf.var.subscribe("RollPID.Heading")
seawolf.var.subscribe("RollPID.Paused")
seawolf.var.subscribe("SEA.Roll")

CELL_X = 12
CELL_Y = 1
FIRST_LINE = 1
INFO_LINE = 6

class GUI:
    def __init__(self,pid, stdscr):
        self.pid = pid
        self.stdscr = stdscr
        self.PID_choice = ['Depth','Roll','Pitch','Yaw']
        self.PID_param = ['p','i','d']
        self.PID_group = [('w','s','x'), ('e','d','c'), ('r','f','v'),('t','g','b')]
        self.matrix = self.populate_matrix()

        self.incr = [0.1, 0.01]
        self.incr_idx = 0

    def populate_matrix(self):
        #aquire common stuff
        pids = self.PID_choice
        params = self.PID_param

        #setup for loop
        N = len(pids)
        M = len(params)
        matrix = np.empty((N,M),dtype='object')

        #populate the matrix
        for n in range(N):
            for m in range(M):
                x = n*CELL_X
                y = m*CELL_Y
                value = self.pid.getPID(pids[n],params[m])

                matrix[n,m] = {'name':pids[n],
                                'param':params[m],
                                'value':value,
                                'x':x,
                                'y':y,
                                }

        return matrix

    def refresh(self):
        N = len(self.PID_choice)
        M = len(self.PID_param)

        #clear the screen
        self.stdscr.clear()

        for n in range(N):
            name = self.matrix[n,0]['name']
            x = self.matrix[n,0]['x']

            #print the header
            self.stdscr.addstr(0,x, name)

            #print the 3x3 array of values            
            for m in range(M):
                y = self.matrix[n,m]['y']
                param = self.matrix[n,m]['param']
                val = self.matrix[n,m]['value']

                self.stdscr.addstr(y+FIRST_LINE,x,"%s:%.2f" % (param,val))

        #print increment text
        incr_txt = "(i)ncrement value: {}".format(self.incr[self.incr_idx])
        self.stdscr.addstr(INFO_LINE,0,incr_txt)
        self.stdscr.addstr(INFO_LINE,0,incr_txt)

        #refresh stdscr
        self.stdscr.refresh()
            

    """updates the cell of the gui display depending on what
    key the user pushes
    --key: char representing the key that was pressed
    --shift: boolean representing whether shift was held or not
    """
    def update(self, key, shift):
        PID_choice = self.PID_choice
        PID_param = self.PID_param
        PID_group = self.PID_group
        incr = self.incr[self.incr_idx]

        N = len(PID_choice)
        M = len(PID_param)

        #set increment amount
        if key == 'i':
            self.incr_idx = (self.incr_idx + 1) % len(self.incr)
        
        PID_flg = False;
        for n in range(N):
            if key in PID_group[n]:
                PID_idx = n #idx representing which PID 
                PID_flg = True
                break

        #match found, find which variable it is
        if PID_flg:
            param_idx = PID_group[PID_idx].index(key)
        else:
            return None

        name = PID_choice[PID_idx]
        param = PID_param[param_idx]

        #retrieve current value
        prev_value = self.matrix[PID_idx,param_idx]['value']
        
        if (shift == 0): #increment
            new_value =prev_value+incr
        elif (shift == 1): #decrement
            new_value =prev_value-incr
        else:
            print "error"

        #update value
        self.pid.setPID(name,param,new_value)

        #update value locally
        self.matrix[PID_idx,param_idx]['value'] = new_value
            
    def getKey(self):
        
        key = self.stdscr.getch()
        
        #if ascii
        if (65<=key) and (key<=122):
            if key < 97:
                shift = 1
                key += 32
            else:
                shift = 0

        key = chr(key) #convert decimal to ascii
        return (key,shift)

class PID:
    def __init__(self):
        pass
        

    def setPID(self, PID, param, val):
        cmd = "{}PID.{}".format(PID, param)
        seawolf.var.set(cmd, val)

    def printPID(self,PID, param):
        seawolf.var.sync()
        cmd = "{}PID.{}".format(PID, param)
        val = seawolf.var.get(cmd)
        print val

    def getPID(self,PID, param):
        seawolf.var.sync()
        cmd = "{}PID.{}".format(PID, param)
        val = seawolf.var.get(cmd)
        return val

    def printAll(self):
        pidname = ["Depth", "Roll", "Pitch", "Yaw"] 
        pidparam = ['p','i','d']
        for i in pidname:
            for j in pidparam:
                print("{}.{}={}".format(i,j,self.getPID(i,j)))

    def gui(self):
        curses.wrapper(self._guiMode)
    
    def _guiMode(self,curses_obj):
        gui = GUI(self,curses_obj)
        while 1:
            #print display
            gui.refresh()

            #query user
            (key,shift) = gui.getKey()

            #update display
            if (key != None):
                gui.update(key,shift)

            if (key == 'q'):
                sys.exit()
            
pid = PID()
pid.printAll()
pid.gui()
