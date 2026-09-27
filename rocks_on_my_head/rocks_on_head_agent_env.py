import pygame
import random
import os
import time
import numpy as np

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

    # discrete action space for the agent
    ACTION_NONE = 0
    ACTION_LEFT = 1
    ACTION_RIGHT = 2

    def __init__(self, n_tracked=3, render_mode=None):

        # headless by default so training doesn't need a physical display / visible window;
        # pass render_mode="human" to actually see the game
        self.render_mode = render_mode
        if render_mode != "human":
            os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

        self.N_TRACKED = n_tracked

        #---------- WINDOW & BACKGROUND -----------
        #Creating the Window
        self.WIN_WIDTH, self.WIN_HEIGHT = 1000, 600
        self.WIN = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))

        #captions for the Window
        pygame.display.set_caption("Rocks on My Head : Agent")

        #setting the background image
        self.BG= pygame.transform.scale(pygame.image.load(os.path.join(IMAGES_DIR,'space_blue.jpg')),(self.WIN_WIDTH,self.WIN_HEIGHT))


        #---------- PLAYER -----------
        #Player attributes
        self.PLAYER_WIDTH, self.PLAYER_HEIGHT = 150, 150
        self.PLAYER_VELOCITY= 30
        self.spacecraft = load_image_no_bg(os.path.join(IMAGES_DIR,'spacecraft.jpg'),(self.PLAYER_WIDTH,self.PLAYER_HEIGHT))
        self.spacecraft_mask = pygame.mask.from_surface(self.spacecraft)


        #---------- PROJECTILES -----------
        self.PROJECTILE_WIDTH, self.PROJECTILE_HEIGHT = 50,50
        self.PROJECTILE_VELOCITY = 5
        self.asteroid = load_image_no_bg(os.path.join(IMAGES_DIR,'asteroid.jpg'),(self.PROJECTILE_WIDTH,self.PROJECTILE_HEIGHT))
        self.asteroid_mask= pygame.mask.from_surface(self.asteroid)

        #setting font
        self.FONT= pygame.font.SysFont("comicsans",30)

        # ms represented by a single step() call; matches the 20-tick clock used in the
        # playable version, and is only used to render a human-readable survival time
        self.TICK_DURATION_MS = 50

        self.done = True  # nothing has been reset() yet


    def reset(self):
        # reset ship position, clear asteroids, reset score/timer
        # return initial state

        self.player = pygame.Rect(self.WIN_WIDTH//2 - self.PLAYER_WIDTH//2,
                                  self.WIN_HEIGHT - self.PLAYER_HEIGHT,
                                  self.PLAYER_WIDTH,
                                  self.PLAYER_HEIGHT)

        self.projectiles = []
        self.proj_add_increment = 700
        self.proj_count = 0
        self.frame_count = 0
        self.survival_frames = 0
        self.done = False

        return self.get_state()

    def step(self, action):

        if self.done:
            raise RuntimeError("step() called after episode ended - call reset() first")

        # Apply Action
        if action == self.ACTION_LEFT and self.player.x - self.PLAYER_VELOCITY >= 0:
            self.player.x -= self.PLAYER_VELOCITY
        elif action == self.ACTION_RIGHT:
            self.player.x = min(self.player.x + self.PLAYER_VELOCITY, self.WIN_WIDTH - self.player.width)

        # Advance frame counters
        self.frame_count += 1
        self.proj_count += 50

        # new asteroids on schedule
        if self.proj_count >= self.proj_add_increment:

            for _ in range(2):
                projectile_x = random.randint(0, self.WIN_WIDTH - self.PROJECTILE_WIDTH)
                projectile = pygame.Rect(projectile_x, -self.PROJECTILE_HEIGHT, self.PROJECTILE_WIDTH, self.PROJECTILE_HEIGHT)
                self.projectiles.append(projectile)

            self.proj_add_increment = max(400, self.proj_add_increment - 50)
            self.proj_count = 0

        # moving asteroids and checking collison

        collided = False
        for projectile in self.projectiles[:]:
            projectile.y += self.PROJECTILE_VELOCITY

            if projectile.y > self.WIN_HEIGHT:
                self.projectiles.remove(projectile)

            elif projectile.colliderect(self.player):
                offset = (projectile.x - self.player.x, projectile.y - self.player.y)
                if self.spacecraft_mask.overlap(self.asteroid_mask, offset):
                    collided = True
                    break

        if collided:
            reward = -100
            self.done = True
        else:
            reward = 1
            self.survival_frames += 1

        state = self.get_state()
        info= {"survived_frames": self.survival_frames}
        return state, reward, self.done, info



    def get_state(self):
        # package ship position + N nearest asteroid positions into a  fixed numpy state array
        ship_x_norm = self.player.x / self.WIN_WIDTH  # easier to train the neural network

        #sorting steroid by y descending
        # higher y -> closer to the ship
        sorted_asteroids = sorted(self.projectiles,key = lambda r : -r.y)

        features = [ship_x_norm]
        for i in range(self.N_TRACKED):

            if i < len(sorted_asteroids):
                a = sorted_asteroids[i]
                dx = (a.x - self.player.x)/self.WIN_WIDTH
                dy = a.y/self.WIN_HEIGHT
                features.extend([dx,dy])
            else:
                features.extend([0.0,-1.0])

        return np.array(features, dtype= np.float32)




    def draw(self):
        #Renders curret state to the window
        #will not be called during training phase

        self.WIN.blit(self.BG,(0,0))
        self.WIN.blit(self.spacecraft, (self.player.x,self.player.y))

        for projectile in self.projectiles :
            self.WIN.blit(self.asteroid,(projectile.x, projectile.y))

        survived_seconds = self.survival_frames * (self.TICK_DURATION_MS /1000)
        survived_text = self.FONT.render(f"Survived: {survived_seconds:.1f}s",1,"white")

        self.WIN.blit(survived_text,(10,10))

        pygame.display.update()
