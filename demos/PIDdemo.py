import seawolf
import curses
import sys

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

CELL_X = 12
CELL_Y = 1

class GUI:
    def __init__(self,pid,curses_obj):
        self.pid = pid
        self.display
        self.PID_choice = ['Depth','Pitch','Yaw']
        self.PID_param = ['p','i','d']
        self.PID_group = [('w','s','x'), ('e','d','c'), ('r','f','v')]
        self.matrix = self.populate_matrix()

    def populate_matrix(self):
        #aquire common stuff
        pids = self.PID_choice
        params = self.PID_param

        #setup for loop
        N = len(pids)
        M = len(params)
        matrix = np.empty((N,M),dtype='object')

        #populate the matrix
        for (n,m) in (range(N), range(M)):
            x = n*CELL_X
            y = m*CELL_Y
            value = self.pid.getPID(pids[n],param[m])

            matrix[n,m] = {'name':pids[n],
                            'param':param[m],
                            'value':value,
                            'x':x,
                            'y':x,
                            }

        return matrix
            

    def update(self, key, shift):
        PID_choice = self.PID_choice
        PID_param = self.PID_param
        PID_group = self.PID_group
        
        i = 0; PID_flg = False;

        for group in PID_group:
            if key in group:
                PID_idx = i
                PID_flg = True
                break
            else
                i += 1

        #match found, find which variable it is
        if PID_flg:
            param_idx = PID_group[PID_idx].index(key)
        else:
            return None

        name = PID_choice[PID_idx]
        param = PID_param[param_idx]
        prev_value = self.cell[PID_idx,param_idx]['value']
        
        if (shift == 0): #increment
            new_value =prev_value+0.1
        elif (shift == 1): #decrement
            new_value =prev_value-0.1
        else:
            print "error"

        self.pid.setPID(name,param,new_value)
            

class PID:
    def __init__(self):
        pass
        

    def setPID(self, PID, val, param):
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
        pidname = ["Depth", "Yaw", "Pitch"] 
        pidparam = ['p','i','d']
        for i in pidname:
            for j in pidparam:
                print("{}.{}={}".format(i,j,self.getPID(i,j)))

    def gui(self):
        curses.wrapper(self._guiMode)
    
    def _guiMode(self,curses_obj)
        gui = GUI(self,curses_obj)
        while 1:
            #print display
            gui.refresh()

            #query user
            key = gui.getKey()

            #update display
            if (key != None):
                gui.update(key)

            if (key == 'q'):
                sys.exit()
            

pid = PID()
pid.printAll()
