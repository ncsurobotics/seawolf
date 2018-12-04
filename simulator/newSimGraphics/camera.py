#uses code from as the core: https://www.youtube.com/watch?v=g4E9iq0BixA
#adapted for opencv
import cv2
import numpy as np
import pygame, sys, math
from cube import Cube
from triangle import Triangle
from mesh import Mesh




class Cam:
    def __init__(self, pos=(0,0,0),rot=(0,0)):
        self.pos = list(pos)
        self.rot = list(rot)
        self.states = dict()
        for c in "wasd .lp;'f":
            self.states[c] = False

    def update(self, events):
        #print self.states['w']
        if len(events['keyup']) > 0:
            self.states[chr(events['keyup'].pop(0))] = False
        if len(events['keydown']) > 0:
            self.states[chr(events['keydown'].pop(0))] = True
        s = .1
        if self.states[' ']:
            self.pos[1]+=s
        if self.states['.']:
            self.pos[1]-=s

        x,y = s * math.sin(self.rot[1]), s*math.cos(self.rot[1])

        if self.states['w']:
            #print "W"
            self.pos[0] += x; self.pos[2] += y
        if self.states['s']:
            self.pos[0] -= x; self.pos[2] -= y
        if self.states['a']:
            self.pos[0] -= y; self.pos[2] += x
        if self.states['d']:
            self.pos[0] += y; self.pos[2] -= x
        
        s = 5
        x = 0
        y = 0
        if self.states['l']:
            x = -1
        if self.states["'"]:
            x = 1
        if self.states['p']:
            y = -1
        if self.states[';']:
            y = 1
        
        x /= 200.0
        y /= 200.0

        self.rot[0] += y * s
        self.rot[1] += x * s

        if self.states['f']:
            return 1
        return 0

        
        """
        if len(events['mouse']) > 0:
            x,y = events['mouse'].pop(0)
            #switch to w/2, h/2
            s = 2
            x/= 200.0
            y/= 200.0
            self.rot[0] += y * s
            self.rot[1] += x * s
        """

