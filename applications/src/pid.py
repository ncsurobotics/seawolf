import libseawolf

"""Instantiates new PID contoller object with parameters
setPoint=initial set point, prop=initial proportional 
coefficient,integ=initial integral coefficient, d=initial 
differential coefficient
Info on PID theory here: http://en.wikipedia.org/wiki/PID_controller
"""

class pid:
    
    """Pass in setPoint and p, i, and d constants
    and initialize other constants"""
    
    def __init__(self, setPoint, prop, integ, deriv):
        #set point
        self.sp = setPoint
        #P value coefficient constant
        self.kp = prop
        #I value coefficient constant
        self.ki = integ
        #D value coefficient constant
        self.kd = deriv
        #creates new Timer object
        libseawolf.Timer = Timer()
        #sum of all past error values
        self.derivator = 0.0
        #time that has passed
        self.integrator = 0.0
        #P value of equation
        self.P_Value = 0.0
        #I value of equation
        self.I_Value = 0.0
        #D value of equation
        self.D_Value = 0.0
        #last error value
        self.lastError = 0.0
        #paused boolean
        self.paused = True
        return self
    
    #pause the pid
    def pause(self):
        self.paused = True
    
    #updates time step    
    def update(self, pv):
        delta = Timer.getDelta(self.Timer)
        error = self.sp - pv
        self.P_Value = self.kp * error
        if self.paused == False:
            self.integrator += delta * error
            self.derivator = error - self.lastError
            self.I_Value = self.ki * self.integrator
            self.D_Value = self.kd * (self.derivator / delta)
        self.paused = False
        self.lastError = error
        mv = self.P_Value + self.I_Value + self.D_Value
        return mv
    #reset integrator
    def resetIntegrator(self):
        self.integrator = 0
    
    #set the set point
    def setSP(self, setPoint):
        self.sp = setPoint
        self.paused = True
    
    #set p coefficient
    def setKP(self, p):
        self.kp = p
    
    #set i coefficient    
    def setKI(self, i):
        self.ki = i
    
    #set d coefficient
    def setKD(self, d):
        self.kd = d
        