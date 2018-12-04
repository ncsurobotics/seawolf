

#using: https://www.youtube.com/watch?v=g4E9iq0BixA
import pygame, sys, math
from srv.nettools import MailBox
from environment import ENGINE_ADDR

pygame.init()
w,h = 60, 60; cx,cy = w//2, h//2
screen = pygame.display.set_mode((w,h))
clock = pygame.time.Clock()

pygame.event.get(); pygame.mouse.get_rel()
pygame.mouse.set_visible(0); pygame.event.set_grab(0)

mouseMode = 0
def switchMouseMode():
    global mouseMode
    mouseMode = (mouseMode + 1) % 2
    pygame.event.set_grab(mouseMode)

mailBox = MailBox()

while True:
    dt = clock.tick()/1000.0
    events = dict()
    events['mouse'] = []
    events['keydown'] = []
    events['keyup'] = []
    for event in pygame.event.get():
        #key = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            events['keydown'].append(event.key)
            if event.unicode == 'm':
                switchMouseMode()
        elif event.type == pygame.MOUSEMOTION:
            events['mouse'].append(event.rel)
        elif event.type == pygame.KEYUP:
            events['keyup'].append(event.key)
        elif event.type == pygame.QUIT: pygame.quit(); sys.exit()
    if len(events['keydown']) or len(events['keyup']) or len(events['mouse']):
        print events
        mailBox.send(events, ENGINE_ADDR)
    

    key = pygame.key.get_pressed()

    if key[pygame.K_k]:
        pygame.quit(); sys.exit()
    #print [int(i) for i in cam.pos]