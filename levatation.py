import pygame,sys,os,math,Utilities, abc, userbrain
from pygame.locals import *
from userbrain import Brain
pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 1000
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
screen.fill(Utilities.white)

sprite_group = pygame.sprite.Group()

gravity = 3

max_vel = 7

player_brain = Brain()

pygame.font.init()
font = pygame.font.Font(None,25)
class Vector(object):
    
    def __init__(self, x=0.0, y=0.0):
        
        self.x = x
        self.y = y

class Screen_Object(pygame.sprite.Sprite):

    __metaclass__ = abc.ABCMeta
    
    def __init__(self,x = 0,y = 0,surface_width = 64,surface_height = 64):

        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.surface = pygame.Surface((surface_width,surface_height))
        self.rect = self.surface.get_rect()
        self.rect.topleft = (self.x,self.y)
        sprite_group.add(self)

    def draw(self,blit_surface = screen):

        screen.blit(self.surface,(self.x,self.y))
        
    @abc.abstractmethod
    def update(self):

        return


class Ground(Screen_Object):

    def __init__(self):

        Screen_Object.__init__(self,surface_width = 500, y = 936)

        self.surface.fill(Utilities.green)

    def __str__(self):

        return "Ground"
    
    def update(self):

        pass


class Levitation_Object(Screen_Object):

    def __init__(self):

        Screen_Object.__init__(self,x = screen.get_width()/2, y = 572)

        self.surface.fill(Utilities.white)
        
        pygame.draw.circle(self.surface, Utilities.blue,
                           (self.surface.get_width()/2,
                            self.surface.get_width()/2),
                           30,3)
        
        self.current_vel = 0
        
    def collides_with_ground(self,s_group = sprite_group):

        collides_with = pygame.sprite.spritecollideany(self,s_group)
        
        return str(collides_with) == "Ground"
                        
    def update(self):

        
        attention = player_brain.getProperty('attention')/100.0 
        print attention
        self.current_vel = gravity - int(attention * max_vel)
        #Update collision rect
        self.rect.topleft = (self.x,self.y)
        
        # Keeps object from falling through the ground
        if (self.collides_with_ground() and self.current_vel > 0) or self.y < 0:
            
            pass

        else:

            self.y += self.current_vel
            
    def __str__(self):
        
        return 'Levitation object:\n\tx: %d\ty: %d' % (self.x, self.y)
    

Screen_Object.register(Ground)
Screen_Object.register(Levitation_Object)

def draw_sprites(sprite_group):

    for sprite in sprite_group:
        
        sprite.draw()

        
ground = Ground()
levitator = Levitation_Object()
import time
CONNECTION_WAIT_TIME = 2 # seconds

running = True
while running:

    if not player_brain.isConnected():
        print 'Player brain not yet connected'
        time.sleep(CONNECTION_WAIT_TIME)
        continue
        
    screen.fill(Utilities.white)
    draw_sprites(sprite_group)
    sprite_group.update()
    #attn_text = font.render('Attention: \t' + str(attention),True,Utilities.black)
    vel_text = font.render('Vel: \t' + str(levitator.current_vel),True,Utilities.black)
    screen.blit(vel_text,(0,vel_text.get_height()))
    #screen.blit(attn_text,(0,0))
    pygame.display.flip()
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False
            pygame.quit()

##        elif event.type == pygame.KEYDOWN:
##
##            if event.key == pygame.K_UP:
##
##                attention += 0.1
##                if attention > 1:
##
##                    attention = 1
##
##            elif event.key == pygame.K_DOWN:
##
##                attention -= 0.1
##                if attention < 0:
##
##                    attention = 0
                    

    
        
                                         
                                         
                                    
        
        
        



    




    
