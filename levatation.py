import pygame
import os
import math
import Utilities
import abc
import random
import time
from pygame.locals import *
from eeg import MindStream

# constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 1000
GRAVITY = 3
MAX_VEL = 7 * 0.1

def initializeGraphics():
    # initialize pygame
    pass
#Roll this mess into the initializeGraphics() function
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
background = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
screen.fill(Utilities.white)
background.fill(Utilities.white)
screen.blit(background, (0,0))
pygame.display.update()
gameScene = pygame.sprite.RenderUpdates()
playerBrain = MindStream()
pygame.font.init()
font = pygame.font.Font(None,25)
goalSize = (64,100,200)


class ScreenObject(pygame.sprite.Sprite):

    __metaclass__ = abc.ABCMeta    
    def __init__(self,x = 0,y = 0,surface_width = 64,surface_height = 64):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pygame.Surface((surface_width,surface_height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x,self.y)
        gameScene.add(self)

    def draw(self,blit_surface = screen):
        screen.blit(self.image,(self.x,self.y))
        
    @abc.abstractmethod
    def update(self):
        return


class Ground(ScreenObject):

    def __init__(self):
        ScreenObject.__init__(self,surface_width = 500, y = 936)
        self.rect = self.image.get_rect()
        self.image.fill(Utilities.green)

    def __str__(self):
        return "Ground"
    
    def update(self):
        self.rect.topleft = (self.x,self.y)


class Levitation_Object(ScreenObject):

    def __init__(self):
        ScreenObject.__init__(self,x = screen.get_width()/2, y = 572)
        self.image.fill(Utilities.white)        
        pygame.draw.circle(self.image, Utilities.blue,
                           (self.image.get_width()/2,
                            self.image.get_width()/2),
                           30,3)        
        self.current_vel = 0
        
    def collides_with_ground(self,s_group = gameScene):
        collides_with = pygame.sprite.spritecollideany(self,s_group)        
        return str(collides_with) == "Ground"
                        
    def update(self):        
        brain_data = playerBrain.getData()
        print 'attention:', brain_data
        attention = None
        if brain_data != None:
            attention = brain_data.pop()['attention']
        else:
            attention = 0
        print 'attention:',attention
        self.current_vel = GRAVITY - int(attention * MAX_VEL)
        print 'vel:', self.current_vel
        #Update collision rect
        self.rect.topleft = (self.x,self.y)
        
        # Keeps object from falling through the ground
        if (self.collides_with_ground() and self.current_vel > 0) or (self.y < 0 and self.current_vel < 0): pass
        else: self.y += self.current_vel
            
    def __str__(self):        
        return 'Levitation object:\n\tx: %d\ty: %d' % (self.x, self.y)

    
class Goal(ScreenObject):

    def __init__(self,size = 0):        
        ScreenObject.__init__(x = screen.get_width()/2,y = 0)
        self.image.fill(Utilities.yellow)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x,self.y)
        
    def update(self):
        print self.x,self.y
                
        ScreenObject.__init__()
ScreenObject.register(Ground)
ScreenObject.register(Levitation_Object)

def draw_sprites(gameScene):
    for sprite in gameScene:        
        sprite.draw()

initializeGraphics()        
ground = Ground()
levitator = Levitation_Object()
CONNECTION_WAIT_TIME = 2 # seconds
running = True

while running:
    if not playerBrain.isConnected():
        print 'Player brain not yet connected'
        time.sleep(CONNECTION_WAIT_TIME)
        continue        
    gameScene.clear(screen,background)
    gameScene.update()
    dirty = gameScene.draw(screen)
    
    vel_text = font.render('Vel: \t' + str(levitator.current_vel),True,Utilities.black)
    screen.blit(vel_text,(0,vel_text.get_height()))
    
    pygame.display.update(dirty)    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()


    
        
                                         
                                         
                                    
        
        
        



    




    
