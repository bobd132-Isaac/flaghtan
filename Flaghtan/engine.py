import math
import time
import pygame
from pygame import *
pygame.init()
myfont = pygame.font.SysFont("monospace", 15)

class Game_camera():
    def __init__(self, (x,y), (screenwidth, screenheight), worldrect, target=None, debug=None):
        self.x = x
        self.y = y
        self.velx = 0
        self.vely = 0
        self.target = target
        self.swidth = screenwidth
        self.sheight = screenheight
        self.rect = Rect(self.x,self.y,screenwidth,screenheight)
        self.centerect =  Rect(self.rect.centerx,self.rect.centery,1,1)
        self.worldrect = worldrect
        self.debug = debug
    def update(self, target, scr):
        self.rect = Rect(self.x,self.y,self.swidth,self.sheight)#camera rect in world ordinates
        self.centerect =  Rect(self.rect.centerx,self.rect.centery,1,1)
        self.velx = self.vely = 0.0
        centered = False
        if target == None:
            print("no target")
        else:
            correx = target.x-self.x
            correy = target.y-self.y
            rectx,recty,w,h = target.rect
            pygame.draw.rect(scr,(0,0,0),(self.swidth//2,self.sheight//2,1,1),2)
            pygame.draw.rect(scr,(80,0,80),(correx,correy,10,10))
            templst = [] #draw mask outline
            for pair in target.mask.outline():
                newx = (pair[0]+target.x)-self.x
                newy = (pair[1]+target.y)-self.y
                templst.append((newx,newy))
            #pygame.draw.polygon(scr,(200,10,50),templst,2) #draw mask outline\
            if not self.centerect.contains(target.rect):
                centered = False
                ##calculate distance/path to target over time
                self.velx = round(float(((target.rect.centerx-(self.swidth/2))-self.x)/3),3)
                self.vely = round(float(((target.rect.centery-(self.sheight/2))-self.y)/3),3)
                x,y,w,h = self.rect
                #predict where rect will be after adding velocity
                temprect = Rect(x+self.velx,y+self.vely,w,h)
                if self.worldrect.contains(temprect):
                    self.x += self.velx #= target.x-(self.swidth//2)
                    self.y += self.vely #= target.y-(self.sheight//2)
                if (temprect.x >= 0 and temprect.x+temprect.width <= self.worldrect.width) and not((temprect.y >= 0 and temprect.y+temprect.height <= self.worldrect.height)):#if out y bounds and in y bounds
                    self.x += self.velx #= target.x-(self.swidth//2)
                if (not(temprect.x >= 0 and (temprect.x+temprect.width) <= self.worldrect.width)) and (temprect.y >= 0 and (temprect.y+temprect.height) <= self.worldrect.height):# if out x bounds and in y bounds
                    self.y += self.vely #= target.y-(self.sheight//2)

            else:
                centered = True
            if self.debug != None:
                self.debug.additem('target pos: '+str((rectx//1,recty//1)))
                self.debug.additem('camera pos: '+str((self.x//1,self.y//1)))
                self.debug.additem('corrected: '+str((correx//1,correy//1)))
                self.debug.additem('velocity: '+str((self.velx,self.vely)))
                self.debug.additem('centered: '+str(centered))


def Collide(thing, otherthings, debug):
    sidetouch=False
    bottomtouch = False
    for object in otherthings:
        if object != thing and object.layer == thing.layer:#not itself, and in same layer
            calc_velx = int(thing.velx)
            calc_vely = int(thing.vely)
            if thing.vely > 0: #if y-velocity is positive (down)
                new_vely = CastRay(thing,object,0,1,debug)[1]
                thing.vely = new_vely
                debug.additem("vely: {0}".format(str(new_vely)))
            if thing.vely < 0: #if y-velocity is negative (up)
                new_vely = CastRay(thing,object,0,-1,debug)[1]
                thing.vely = new_vely
                debug.additem("vely: {0}".format(str(new_vely)))
                pass
            if thing.velx > 0: #if x-velocity is positive (right)
                new_velx = CastRay(thing,object,1,0,debug)[0]
                thing.velx = new_velx
                debug.additem("vely: {0}".format(str(new_velx)))
            if thing.velx < 0: #if x-velocity is negative (left)
                new_velx = CastRay(thing,object,-1,0,debug)[0]
                thing.velx = new_velx
                debug.additem("vely: {0}".format(str(new_velx)))

            overlap_on_obj = object.mask.overlap(thing.mask, (int((thing.x-object.x)+thing.velx), int((thing.y-object.y)+thing.vely)))
            if overlap_on_obj:
                overlap_on_thing = (int(overlap_on_obj[0]-thing.x),int(overlap_on_obj[1]-thing.y))
                debug.additem("overlap on environment (thing), {0}: {1}".format(thing.name,str(overlap_on_obj)))
                debug.additem("overlap on object, {0}: {1}".format(object.name,str(overlap_on_thing)))
                debug.addpixel(overlap_on_obj)
                debug.addpixel(overlap_on_thing)
    thing.grounded = bottomtouch

def CastRay(thing, target, xstep, ystep, debug):
    xdist = 0
    ydist = 0
    while not target.mask.overlap(thing.mask, (int((thing.x-target.x)+xdist+xstep), int((thing.y-target.y)+ydist+ystep))):#not touching anything
        debug.additem(str(target.mask.overlap(thing.mask, (int((thing.x-target.x)+xdist+xstep), int((thing.y-target.y)+ydist+ystep)))))
        if abs(xdist)>abs(thing.velx) or abs(ydist)>abs(thing.vely):
            return thing.velx ,thing.vely
        xdist += xstep
        ydist += ystep
    return xdist, ydist


def ApplyForce(mass, forcex, forcey):
    if math.fabs(float(mass)) >= 0.05:
        return ((forcex/mass),(forcey/mass))
    else:
        return 0, 0

def Accelerate(deltat, (oldvelx, oldvely), (accelx, accely), debug):
    newvelx = oldvelx + (accelx/1000)*deltat
    newvely = oldvely + (accely/1000)*deltat
    return(newvelx,newvely)

def Friction(thing, debug, drag):
    thing.velx *= drag
    thing.vely *= drag

class Debug():
    def __init__(self):
        self.debuglst = []
        self.pixellst = []
    def additem(self,item):
        self.debuglst.append(item)
    def addpixel(self,(x,y)):
        self.pixellst.append((x,y))
    def display(self,screen,cam):
        for ypos,item in enumerate(self.debuglst):
            label = myfont.render(item,1,(100,100,100))
            screen.blit(label,(0,ypos*15))
        for item in self.pixellst:
            draw.rect(screen,(130,50,200),Rect(item[0]-cam.x,item[1]-cam.y,5,5))
        self.pixellst = []
        self.debuglst = []
