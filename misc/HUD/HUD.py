from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import seawolf as sw
import sys
import math
import random

ESCAPE = '\033'

# Number of the glut window.
window = 0
PI=3.14159

PORT=0.0
STAR = 0.0
BOW = 0.0
STERN = 0.0
STRAFE = 0.0
DEPTH = 0.0
DEPTH_HEADING = 0.0
CUR_PITCH = 0.0
CUR_ROLL = 0.0

# A general OpenGL initialization function.  Sets all of the initial parameters
def InitGL(Width, Height):              # We call this right after our OpenGL window is created.
    glClearColor(0.0, 0.0, 0.0, 0.0)    # This Will Clear The Background Color To Black
    glClearDepth(1.0)                   # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)                # The Type Of Depth Test To Do
    glDisable(GL_DEPTH_TEST)                # Enables Depth Testing
    glShadeModel(GL_SMOOTH)             # Enables Smooth Color Shading

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()                    # Reset The Projection Matrix
                                        # Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)

# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
    if Height == 0:                     # Prevent A Divide By Zero If The Window Is Too Small
        Height = 1

    glViewport(0, 0, Width, Height)     # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def Update(d):
    glutTimerFunc(2000,Update,0)
    glutPostRedisplay()

def SetVariables(number):
    global PORT
    global STAR
    global BOW
    global STERN
    global STRAFE
    global DEPTH
    global DEPTH_HEADING
    global CUR_PITCH
    global CUR_ROLL

    if number==0:
        PORT = random.randint(-100,100)*0.001
        STAR = random.randint(-100,100)*0.001
        BOW = random.randint(-100,100)*0.001
        STERN = random.randint(-100,100)*0.001
        STRAFE = random.randint(-100,100)*0.001
        DEPTH = random.randint(0,12)
        DEPTH_HEADING = random.randint(0,12)
        CUR_PITCH = random.randint(-10,10)
        CUR_ROLL = random.randint(-10,10)
    else:
        PORT = sw.var.get("PORT")
        STAR = sw.var.get("Star")
        BOW = sw.var.get("Bow")
        STERN = sw.var.get("Stern")
        STRAFE = sw.var.get("Strafe")
        DEPTH = sw.var.get("Depth")
        DEPTH_HEADING = sw.var.get("DEPTHPID.Heading")
        CUR_PITCH = sw.var.get("SEA.Pitch")
        CUR_ROLL = sw.var.get("SEA.Roll")


# The main drawing function.
def DrawGLScene():
    # Clear The Screen And The Depth Buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()                    # Reset The View

    SetVariables(1)

    # Move Right 3.0 units.
    glTranslatef(-4, 0.0, -10.0)
    drawDepthGauge()

    glTranslatef(3,0,0)

    drawThrusterGauge()

    glTranslatef(6,0,0)

    drawLevelGauge()

    #  since this is double buffered, swap the buffers to display what just got drawn.
    glutSwapBuffers()

#  The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)  [0.0,1.0,0.0,1.0]
def keyPressed(*args):
    # If escape is pressed, kill everything.
    if args[0] == ESCAPE:
        glutDestroyWindow(window)
        sys.exit()

def drawText(x, y, font, text):
    text_color=[0.0,1.0,0.0,1.0]
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, text_color)
    glColor4f(1,1,1,1);
    glRasterPos2f(x,y)
    for i in text:
        glutBitmapCharacter(font, ord(i))

def drawDepthGauge():
    #white top border
    glColor3f(.9,.9,.9)
    glBegin(GL_QUADS)
    glVertex3f(-2,2,0)
    glVertex3f(-2,2.25,0)
    glVertex3f(2,2.25,0)
    glVertex3f(2,2,0)
    glEnd()

    #black bottom border
    glColor3f(.1,.1,.1)
    glBegin(GL_QUADS)
    glVertex3f(-2,-3,0)
    glVertex3f(-2,-2,0)
    glVertex3f(2,-2,0)
    glVertex3f(2,-3,0)
    glEnd()

    #blue water
    glColor3f(0,0,.05)
    glBegin(GL_QUADS)
    glVertex3f(-2,-2,0)
    glVertex3f(2,-2,0)
    glColor3f(0,0,1)
    glVertex3f(2,2,0)
    glVertex3f(-2,2,0)
    glEnd()

    #scale
    glColor(.4,.4,.4)
    glBegin(GL_QUADS)
    glVertex3f(-1.6,-2,0)
    glVertex3f(-.8,-2,0)
    glColor(.9,.9,.9)
    glVertex3f(-.8,2,0)
    glVertex3f(-1.6,2,0)
    glEnd()

    #scale lines
    i=-20
    j=16
    while i<=20:
        drawText(-1.9,i*0.1-0.05,GLUT_BITMAP_HELVETICA_12,'%d' % j)
        glColor3f(1,1,1)
        glBegin(GL_LINES)
        glVertex2f(-1.6,i*.1)
        glVertex2f(-.8,i*.1)
        glEnd()
        i=i+5
        j=j-2

    glColor3f(1,1,1)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex3f(0,2-DEPTH*0.25,0)
    glVertex3f(1.5,2-DEPTH*0.25,0)

    glColor3f(1,0,0)
    glVertex3f(.5,2.25-DEPTH_HEADING*0.25,0)
    glVertex3f(1,1.75-DEPTH_HEADING*0.25,0)

    glVertex3f(1,2.25-DEPTH_HEADING*0.25,0)
    glVertex3f(.5,1.75-DEPTH_HEADING*0.25,0)
    glEnd()

    drawText(-1.5,-2.3,GLUT_BITMAP_HELVETICA_12,"ACTUAL")
    drawText(-1.5,-2.9,GLUT_BITMAP_HELVETICA_18,'%.3f' % DEPTH)

    drawText(.5,-2.3,GLUT_BITMAP_HELVETICA_12,"HEADING")
    drawText(.5,-2.9,GLUT_BITMAP_HELVETICA_18,'%.3f' % DEPTH_HEADING)

    drawText(-1,3,GLUT_BITMAP_HELVETICA_18,"DEPTH GAUGE")

def drawThrusterGauge():
    drawText(0,3,GLUT_BITMAP_HELVETICA_18,"THRUSTER GAUGE")

    glColor3f(1,1,1)
    glBegin(GL_LINE_LOOP)
    glVertex3f(0,-2,0)
    glVertex3f(0,2,0)
    glVertex3f(3,2,0)
    glVertex3f(3,-2,0)
    glEnd()

    glBegin(GL_LINES)
    glVertex3f(1.2,-2,0)
    glVertex3f(1.2,2,0)

    glVertex3f(0,1.2,0)
    glVertex3f(3,1.2,0)

    glVertex3f(0,.4,0)
    glVertex3f(3,.4,0)

    glVertex3f(0,-.4,0)
    glVertex3f(3,-.4,0)

    glVertex3f(0,-1.2,0)
    glVertex3f(3,-1.2,0)
    glEnd()

    drawText(.1,1.3,GLUT_BITMAP_HELVETICA_18,"Port X")
    drawText(1.3,1.3,GLUT_BITMAP_HELVETICA_18,'%.3f' %PORT)
    drawText(.1,.5,GLUT_BITMAP_HELVETICA_18,"Star X")
    drawText(1.3,.5,GLUT_BITMAP_HELVETICA_18,'%.3f' %STAR)
    drawText(.1,-.3,GLUT_BITMAP_HELVETICA_18,"Bow Y")
    drawText(1.3,-.3,GLUT_BITMAP_HELVETICA_18,'%.3f' %BOW)
    drawText(.1,-1.1,GLUT_BITMAP_HELVETICA_18,"Stern Y")
    drawText(1.3,-1.1,GLUT_BITMAP_HELVETICA_18,'%.3f' %STERN)
    drawText(.1,-1.9,GLUT_BITMAP_HELVETICA_18,"Strafe")
    drawText(1.3,-1.9,GLUT_BITMAP_HELVETICA_18,'%.3f' %STRAFE)

def drawLevelGauge():
    drawText(-1,3,GLUT_BITMAP_HELVETICA_18,"LEVEL GAUGE")

    glColor3f(.1,.1,.1)
    glBegin(GL_QUADS)
    glVertex3f(-2,-2,0)
    glVertex3f(2,-2,0)
    glVertex3f(2,-3,0)
    glVertex3f(-2,-3,0)

    glColor3f(0,0,.5)
    glVertex3f(-2,-0.02*CUR_ROLL-0.04*CUR_PITCH,0)
    glVertex3f(2,0.02*CUR_ROLL-0.04*CUR_PITCH,0)
    glVertex3f(2,-2,0)
    glVertex3f(-2,-2,0)
    glEnd()


    glColor3f(1,1,1)
    glLineWidth(2)
    #white circle outline
    i=0
    while i<360:
        glBegin(GL_LINES)
        glVertex3f(2*math.cos(i*PI/180),2*math.sin(i*PI/180),0)
        glVertex3f(2*math.cos((i+1)*PI/180),2*math.sin((i+1)*PI/180),0)
        i=i+1
        glEnd()

    glBegin(GL_LINES)
    glVertex3f(-2,0,0)
    glVertex3f(-.75,0,0)

    glVertex3f(-.75,0,0)
    glVertex3f(-.5,-.4,0)

    glVertex3f(.5,-.4,0)
    glVertex3f(.75,0,0)

    glVertex3f(.75,0,0)
    glVertex3f(2,0,0)

    i=-1.6
    while i<=1.6:
        glVertex3f(-.5,i,0)
        glVertex3f(.5,i,0)
        i=i+.4
    glEnd()

    glBegin(GL_LINE_LOOP)
    glVertex3f(-.5,-.4,0)
    glVertex3f(.5,-.4,0)
    glVertex3f(0,0,0)
    glEnd()

    i=-1.7
    number = 40
    while i<=1.7:
        drawText(-.72,i,GLUT_BITMAP_HELVETICA_12,'%d' % math.fabs(number))
        i=i+.4
        number=number-10

    drawText(-1.5,-2.3,GLUT_BITMAP_HELVETICA_12,"PITCH")
    drawText(-1.5,-2.9,GLUT_BITMAP_HELVETICA_18,'%.3f' % CUR_PITCH)
    drawText(.5,-2.3,GLUT_BITMAP_HELVETICA_12,"ROLL")
    drawText(.5,-2.9,GLUT_BITMAP_HELVETICA_18,'%.3f' % CUR_ROLL)

def main():
    #sw.loadConfig("../../conf/seawolf.conf")
    #sw.init("HUD")
    #sw.var.subscribe("Depth")
    #sw.var.subscribe("DepthPID.Heading")
    #sw.var.subscribe("Port")
    #sw.var.subscribe("Star")
    #sw.var.subscribe("Bow")
    #sw.var.subscribe("Stern")
    #sw.var.subscribe("Strafe")
    #sw.var.subscribe("SEA.Pitch")
    #sw.var.subscribe("SEA.Roll")

    global window
    # For now we just pass glutInit one empty argument. I wasn't sure what should or could be passed in (tuple, list, ...)
    # Once I find out the right stuff based on reading the PyOpenGL source, I'll address this.

    glutInit(())

    # Select type of Display mode
    #  Double buffer
    #  RGBA color
    # Alpha components supported
    # Depth buffer
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)

    # get a 640 x 480 window
    glutInitWindowSize(840, 480)

    # the window starts at the upper left corner of the screen
    glutInitWindowPosition(0, 0)

    # Okay, like the C version we retain the window id to use when closing, but for those of you new
    # to Python (like myself), remember this assignment would make the variable local and not global
    # if it weren't for the global declaration at the start of main.
    window = glutCreateWindow("Seawolf Software HUD")

    # Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
    # set the function pointer and invoke a function to actually register the callback, otherwise it
    # would be very much like the C version of the code.
    glutDisplayFunc (DrawGLScene)

    # Uncomment this line to get full screen.
    #glutFullScreen()

    # When we are doing nothing, redraw the scene.
   # glutTimerFunc(0,Update(),0)
    glutTimerFunc(0,Update,0)

    # Register the function called when our window is resized.
    glutReshapeFunc(ReSizeGLScene)

    # Register the function called when the keyboard is pressed.
    glutKeyboardFunc (keyPressed)

    # Initialize our window.
    InitGL(640, 480)

    # Start Event Processing Engine
    glutMainLoop()

# Print message to console, and kick off the main to get it rolling.
print "Hit ESC key to quit."
main()

