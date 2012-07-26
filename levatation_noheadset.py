import pygame,sys,os,math,Utilities, abc
from pygame.locals import *
from mindcontrol.userbrain import Brain
pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 1000
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
screen.fill(Utilities.white)

background = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
background.fill(Utilities.white)
#^^^^^^^^
# To use pygame.sprite.RenderUpdates().clear(screen,bg), you must draw the background
#to the screen and call pygame.display.update()!!!!!!

screen.blit(background, (0,0))
pygame.display.update()

game_scene = pygame.sprite.RenderUpdates()

gravity = 3
attention = 0
max_vel = 7

pygame.font.init()
font = pygame.font.Font(None,25)

class Screen_Object(pygame.sprite.Sprite):

    __metaclass__ = abc.ABCMeta
    
    def __init__(self,x = 0,y = 0,surface_width = 64,surface_height = 64):

        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.image = pygame.Surface((surface_width,surface_height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x,self.y)
        game_scene.add(self)

    def draw(self,blit_surface = screen):

        screen.blit(self.image,(self.x,self.y))
        
    @abc.abstractmethod
    def update(self):

        return


class Ground(Screen_Object):

    def __init__(self):

        Screen_Object.__init__(self,surface_width = 500, y = 936)
        print self.rect.top_left
        self.image.fill(Utilities.green)

    def __str__(self):

        return "Ground"
    
    def update(self):

        pass


class Levitation_Object(Screen_Object):

    def __init__(self,color):

        Screen_Object.__init__(self,x = screen.get_width()/2, y = 572)
        self.color = color
        self.image.fill(Utilities.white)
        
        pygame.draw.circle(self.image, self.color,
                           (self.image.get_width()/2,
                            self.image.get_width()/2),
                           30,3)
        
        self.current_vel = 0
        
    def collides_with_ground(self,s_group = game_scene):
        
        collides_with = pygame.sprite.spritecollideany(self,s_group)
        print collides_with
        return str(collides_with) == "Ground"
                        
    def update(self):

        self.current_vel = gravity - int(attention * max_vel)
        
        #Update collision rect
        self.rect.topleft = (self.x,self.y)
        check = self.collides_with_ground()
        
        # Keeps object from falling through the ground or ceiling
        if (check and self.current_vel > 0) or (self.y < 0 and self.current_vel < 0):
            
            pass

        else:

            self.y += self.current_vel
            
    def __str__(self):
        'Levitation object:\n\tx: %d\ty: %d' % (self.x, self.y)
        return 'Levitation Object'
    

Screen_Object.register(Ground)
Screen_Object.register(Levitation_Object)
      
ground = Ground()
levitator = Levitation_Object(Utilities.blue)

running = True
while running:

    game_scene.clear(screen,background)
    game_scene.update()
    dirty = game_scene.draw(screen)
    vel_text = font.render('Vel: \t' + str(levitator.current_vel),True,Utilities.black)
    screen.blit(vel_text,(0,vel_text.get_height()))
    
    pygame.display.update(dirty)
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False
            pygame.quit()

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:

                attention += 0.1
                if attention > 1:

                    attention = 1

            elif event.key == pygame.K_DOWN:

                attention -= 0.1
                if attention < 0:

                    attention = 0
                    

    
        
                                         
                                         
                                    
        
        
        



    




    
