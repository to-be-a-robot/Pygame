import pygame
import random
import os 
import time

from PIL import Image
pygame.font.init()

IMAGES_DIR= os.path.join(os.path.dirname(os.path.abspath(__file__)),'images')

def load_image_no_bg(path, size, tolerance = 30):
    img= Image.open(path).convert('RGBA')
    bg_r,bg_g,bg_b,_= img.getpixel((0,0))
    img= img.resize(size)
    pixels= img.getdata()
    new_pixels=[(r,g,b,0) if abs(r - bg_r)<= tolerance and  abs(g - bg_g)<= tolerance and abs(b - bg_b)<= tolerance else (r, g, b, a)
                for (r,g,b,a) in pixels]

    img.putdata(new_pixels)
    return pygame.image.fromstring(img.tobytes(), img.size,'RGBA').convert_alpha()





class AsteroidGame:
    def __init__(self):

        #---------- WINDOW & BACKGROUND ----------- 
        #Creating the Window 
        WIN_HEIGHT, WIN_WIDTH = 600,1000
        self.WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

        #captions for the Window 
        pygame.display.set_caption("Rocks on My Head : Agent")

        #setting the background image 
        self.BG= pygame.transform.scale(pygame.image.load(os.path.join(IMAGES_DIR,'space_blue.jpg')),(WIN_WIDTH,WIN_HEIGHT))


        #---------- PLAYER ----------- 
        #Player attributes 
        PLAYER_WIDTH, PLAYER_HEIGHT = 150, 150 
        PLAYER_VELOCITY= 30 
        self.spacecraft = load_image_no_bg(os.path.join(IMAGES_DIR,'spacecraft.jpg'),(PLAYER_WIDTH,PLAYER_HEIGHT))
        self.spacecraft_mask = pygame.mask.from_surface(self.spacecraft)


        #---------- PROJECTILES -----------
        PROJECTILE_WIDTH, PROJECTILE_HEIGHT = 50,50
        PROJECTILE_VELOCITY = 5 
        self.asteroid = load_image_no_bg(os.path.join(IMAGES_DIR,'asteroid.jpg'),(PROJECTILE_WIDTH,PROJECTILE_HEIGHT)) 
        self.asteroid_mask= pygame.mask.from_surface(self.asteroid)

        #setting font
        self.FONT= pygame.font.SysFont("comicsans",30)


    
    def reset(self):
        # reset ship position, clear asteroids, reset score/timer
        # return initial state
        ...
    
    def step(self, action):
        # apply action (move ship left/right/stay)
        # advance one frame: move asteroids, spawn new ones, check collision
        # compute reward
        # return (state, reward, done, info)
        ...
    
    def draw(self, screen):
        # render current state to screen (only needed when watching, not during fast training)
        ...
    
    def get_state(self):
        # helper: package ship position + asteroid positions into a state array
        ...






