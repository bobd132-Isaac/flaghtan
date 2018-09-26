import pygame
from pygame import *
from engine import *
pygame.init()
myfont = pygame.font.SysFont("monospace", 15)

class world():
    def __init__(self, (x,y)):
        self.x = x
        self.y = y

class thing():
    def __init__(self, (x,y), img, layer, screen, name, space, mass=0, debug=None):
        self.x = x
        self.y = y
        self.velx = 0
        self.vely = 0
        self.forcex = 0
        self.forcey = 0
        self.img = img
        self.rect = Rect(self.x,self.y,5,5)
        self.centerx = self.rect.centerx
        self.centery = self.rect.centery
        self.mass = mass
        self.mask = pygame.mask.from_surface(self.img)
        self.grounded = False
        self.maskoutline = self.mask.outline()
        self.name = name
        self.space = space
        self.layer = layer
        self.window = screen
        self.debug = debug
    def update(self, w,a,s,d,space, deltat):
        self.rect = Rect(self.x,self.y,5,5)
        x,y,wid,hei = self.img.get_rect()
        #self.mask = pygame.mask.from_surface(self.img)
        self.centerx = self.rect.centerx
        self.centery = self.rect.centery
        if self.debug != None:
            self.debug.additem(self.name+"{0},{1},{2},{3}".format(x,y,wid,hei))


class Player(thing):
    def update(self, w, a, s, d, space, deltat):
        self.rect = Rect(self.x,self.y,self.img.get_rect().width,self.img.get_rect().height)
        self.centerx = self.rect.centerx
        self.centery = self.rect.centery
        self.mask = pygame.mask.from_surface(self.img)
        oldvelx = self.velx
        oldvely = self.vely
        oldforcex = self.forcex
        oldforcey = self.forcey
        if w:# and self.grounded:
            self.forcey += -5
        if s:
            self.forcey += 1
        if a:
            self.forcex += -3
        if d:
            self.forcex += 3
        self.forcey += 2 #gravity
        self.forcex = self.forcex - self.velx*0.8#friction
        self.forcey = self.forcey - self.vely*0.8
        self.forcex = self.forcex - oldforcex
        self.forcey = self.forcey - oldforcey
        self.debug.additem("{0}: {1}xN {2}yN".format(self.name,self.forcex,self.forcey))
        self.velx, self.vely = Accelerate(deltat,(oldvelx,oldvely),(ApplyForce(self.mass,self.forcex,self.forcey)),self.debug)
        Collide(self, self.space, self.debug)
        self.debug.additem("{0}: {1}x {2}y".format(self.name,self.velx,self.vely))
        #Friction(self,self.debug,0.99)
        
        self.x += self.velx
        self.y += self.vely

class Layer(thing):
    pass


