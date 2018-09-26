import os
import pygame
from sprites import *
from engine import *

background_colour = (255,255,255)
(width, height) = (1280, 720)

window = pygame.display.set_mode((width, height))
pygame.display.set_caption('yaaa')
window.fill(background_colour)
pygame.init()

groundimg = pygame.image.load('backtest.png').convert_alpha()
ground1img = pygame.image.load('back1.png').convert_alpha()
playerimg = pygame.image.load('playerimg.png').convert_alpha()

worldrect = Rect(0,0,10800,1080)

layer1 = 1
layer2 = 0.8
layer3 = 0.6

things = []
debugger = Debug()
main_layer = Layer((0,0),groundimg, layer1,window,"main", things, debug=debugger)
back_0 = Layer((0,0),ground1img,layer2,window,"back",things,debug=debugger)
player = Player((0,800), playerimg, layer1, window, "player", things, mass=0.1, debug=debugger)
game_cam = Game_camera((0,0),(width,height),worldrect, debug=debugger)
things.append(back_0)
things.append(main_layer)
things.append(player)

pygame.display.flip()

clock = pygame.time.Clock()

running = True
while running:
    dt = clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
    
    up=left=down=right=space=False
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        running = False
    if keys[K_w]:
        up = True
    if keys[K_s]:
        down = True
    if keys[K_a]:
        left = True
    if keys[K_d]:
        right = True
    if keys[K_SPACE]:
        space = True
    window.fill((190,215,170))
    if not space:
        game_cam.update(player,window)
    else:
        game_cam.update(back_0,window)
    mousex,mousey = mouse.get_pos()
    debugger.additem(str((mousex-game_cam.x, mousey+game_cam.y)))
    for item in things:
        window.blit(item.img,(item.x-game_cam.x,item.y-game_cam.y))
        if 'update' in dir(item):
            item.update(up,left,down,right,space,dt)
    debugger.display(window,game_cam)
    pygame.display.update()
   
