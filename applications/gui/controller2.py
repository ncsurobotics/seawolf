"""
Like the GUI except used to control the robot with keyboard presses.

W and S move robot forward and backwards

Space and shift move robot up and down

If you are not holding left-control, A and D turn the robot (yaw)

If you are holding left-control, A and D strafe the robot sideways

Pygame used for reading key events
"""
import pygame, sys, math
import seawolf as sw

sys.path.append('../../mission_control')
import sw3


connected = True
if connected:
    sw.loadConfig("../../conf/seawolf.conf")
    sw.init("Controller") 

pygame.init()
w,h = 100, 100
cx,cy = w//2, h//2
screen = pygame.display.set_mode((w,h))
clock = pygame.time.Clock()

pygame.event.get()
pygame.mouse.get_rel()
pygame.mouse.set_visible(0)
pygame.event.set_grab(0)

def handleKey(states):
  for letter in events['keydown']:
    states[letter] = True
  for letter in events['keyup']:
    states[letter] = False
  
def doMoves(states):
  rot = .4
  speed = 1
  rise_speed = .5
  #Move forwards and backwards
  if states['w']:
    sw3.Forward(speed).start()
  elif states['s']:
    sw3.Forward(-speed).start()
  else:
    sw3.Forward(0).start()
  
  if states['a']:
      sw3.RelativeYaw( rot + math.pi ).start()
  elif states['d']:
      sw3.RelativeYaw( -rot ).start()
  else:
      #reset yaw and strafe, both states of l-ctrl are covered
      sw3.RelativeYaw( 0 ).start()
  
def char(ascii):
    try:
        return chr(ascii).lower()
    except:
        if ascii == 304:
            return 'shift'
        elif ascii == 306:
            return 'l-ctrl'
        elif ascii == 305:
            return 'r-ctrl'
        return str(ascii)  

mouseMode = 0
def switchMouseMode():
    global mouseMode
    mouseMode = (mouseMode + 1) % 2
    pygame.event.set_grab(mouseMode)

states = {'w':False, 'a':False, 's':False, 'd':False, 'shift':False, 'l-ctrl':False, ' ':False }

while True:
    dt = clock.tick()/1000.0
    events = dict()
    events['mouse'] = []
    events['keydown'] = []
    events['keyup'] = []
    for event in pygame.event.get():
        #key = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            events['keydown'].append(char(event.key))
            if event.unicode == 'm':
                switchMouseMode()
        elif event.type == pygame.MOUSEMOTION:
            events['mouse'].append(event.rel)
        elif event.type == pygame.KEYUP:
            events['keyup'].append(char(event.key))
        elif event.type == pygame.QUIT: pygame.quit(); sys.exit()
    if len(events['keydown']) or len(events['keyup']) or len(events['mouse']):
        #print events
        handleKey(states)
        #print states
        #mailBox.send(events, ENGINE_ADDR)
    if connected:
        doMoves(states)
    

    key = pygame.key.get_pressed()

    if key[pygame.K_k]:
        pygame.quit()
        if connected:
            sw.close()
            sys.exit()
    #print [int(i) for i in cam.pos]