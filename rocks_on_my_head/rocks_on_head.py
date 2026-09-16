import pygame
import random
import time
import os
from PIL import Image
pygame.font.init()

IMAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')


def load_image_no_bg(path, size, tolerance=30):  #loads a jpg and makes its background transparent, since jpg can't store transparency itself
    img = Image.open(path).convert('RGBA')
    bg_r, bg_g, bg_b, _ = img.getpixel((0, 0))  #sample the actual background color from the corner instead of assuming it's white
    img = img.resize(size)
    pixels = img.getdata() #return PIL object -ImagingCore  
    new_pixels = [
        (r, g, b, 0) if abs(r - bg_r) <= tolerance and abs(g - bg_g) <= tolerance and abs(b - bg_b) <= tolerance else (r, g, b, a)
        for (r, g, b, a) in pixels]
    img.putdata(new_pixels)
    return pygame.image.fromstring(img.tobytes(), img.size, 'RGBA').convert_alpha()


#---------- WINDOW & BACKGROUND -----------
# creating a window
WIDTH, HEIGHT= 1000, 600 # the dimensions of the window in pixels
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE) # creating the window, RESIZABLE lets the player drag the corners to expand it

#caption for the window - this will be the name at the top of the window
pygame.display.set_caption(" Rocks on My Head")

#setting a background image
BG_ORIGINAL = pygame.image.load(os.path.join(IMAGES_DIR,'space_blue.jpg')).convert()  #keep the unscaled image so it can be rescaled cleanly for any window size
BG= pygame.transform.scale(BG_ORIGINAL, (WIDTH, HEIGHT))

FULLSCREEN = False
WINDOWED_SIZE = (WIDTH, HEIGHT)  #remembers the windowed size so toggling fullscreen off can restore it

#---------- PLAYER ----------- 
#Player attributes
PLAYER_WIDTH, PLAYER_HEIGHT= 150, 150
PLAYER_VELOCITY= 30
spacecraft = load_image_no_bg(os.path.join(IMAGES_DIR,'spacecraft.jpg'), (PLAYER_WIDTH, PLAYER_HEIGHT))
spacecraft_mask = pygame.mask.from_surface(spacecraft)


 #---------- PROJECTILES ----------- 
#Projectile attributes
PROJECTILE_WIDTH=  50 
PROJECTILE_HEIGHT= 50 
PROJECTILE_VELOCITY= 5 
asteroid = load_image_no_bg(os.path.join(IMAGES_DIR,'asteroid.jpg'), (PROJECTILE_WIDTH, PROJECTILE_HEIGHT))
asteroid_mask = pygame.mask.from_surface(asteroid) 


#setting a font for the timer
FONT= pygame.font.SysFont("comicsans", 30) # setting the font

#restart button attributes
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 60
BUTTON_RECT = pygame.Rect(WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 + 40, BUTTON_WIDTH, BUTTON_HEIGHT)


def rescale(new_width, new_height):  #recomputes everything that depends on the window size so expanding the screen expands the whole game with it
    global WIDTH, HEIGHT, BG, BUTTON_RECT
    WIDTH, HEIGHT = new_width, new_height
    BG = pygame.transform.scale(BG_ORIGINAL, (WIDTH, HEIGHT))
    BUTTON_RECT = pygame.Rect(WIDTH//2 - BUTTON_WIDTH//2, HEIGHT//2 + 40, BUTTON_WIDTH, BUTTON_HEIGHT)


def toggle_fullscreen():
    global WIN, FULLSCREEN, WINDOWED_SIZE
    FULLSCREEN = not FULLSCREEN
    if FULLSCREEN:
        WINDOWED_SIZE = (WIDTH, HEIGHT)  #remember the windowed size so we can restore it later
        info = pygame.display.Info()
        WIN = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
        rescale(info.current_w, info.current_h)
    else:
        WIN = pygame.display.set_mode(WINDOWED_SIZE, pygame.RESIZABLE)
        rescale(*WINDOWED_SIZE)


def draw(player, elapsed_time, projectiles):

    WIN.blit(BG, (0,0)) # background

    timer_text= FONT.render(f"Time: {round(elapsed_time)}s", 1, "white") #timer
    WIN.blit(timer_text, (WIDTH - timer_text.get_width() - 20, 10))  # position of timer, relative to the current width

    WIN.blit(spacecraft, (player.x, player.y)) #spacecraft image at the player's position

    for projectile in projectiles:  #this will draw each projectile on the window
        WIN.blit(asteroid, (projectile.x, projectile.y))  #this will draw the asteroid image at the projectile's position

    pygame.display.update()  #this updates the display to show the new frame


GAME_OVER_DELAY = 2  # seconds to show "Game Over" before the reset button appears

def draw_game_over(elapsed_time, show_button):

    WIN.blit(BG, (0,0)) # background

    lost_text= FONT.render(f" Game Over! Time survived: {round(elapsed_time)}s", 1, "white")  # player loses
    WIN.blit(lost_text, (WIDTH//2 - lost_text.get_width()//2, HEIGHT//2 - lost_text.get_height()//2))

    if show_button:
        pygame.draw.rect(WIN, "orange", BUTTON_RECT, border_radius=8)
        button_text = FONT.render("Restart", 1, "white")
        WIN.blit(button_text, (BUTTON_RECT.centerx - button_text.get_width()//2, BUTTON_RECT.centery - button_text.get_height()//2))

    pygame.display.update()


def main():
    global WIN
    run = True

    player =pygame.Rect(WIDTH//2 - PLAYER_WIDTH//2, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT) #spacecraft at the bottom middle 

    clock= pygame.time.Clock() 

    start_time = time.time()  #current time in seconds
    elapsed_time = 0  

    #adding projectiles
    proj_add_increment = 2000 # first projectile @ 2000 'milliseconds'
    proj_count = 0 #this will keep track of when to add a new projectile to the game
    
    projectiles=[] #this will be a list to hold the projectiles that are currently on the screen

    game_state= "playing"
    game_over_time = None  # timestamp when the game ended, used to gate the reset button


    while run:


        if game_state == "playing":
            proj_count += clock.tick(20)  # limit the frame rate to 60 frames per second
            elapsed_time = time.time() - start_time  # elapsed time since the start of the game

            if proj_count >= proj_add_increment:  #if the proj_count is greater than  the proj_add_increment, we will add a new projectile to the game

                for _ in range(3):  
                    projectile_x= random.randint(0, WIDTH - PROJECTILE_WIDTH)  #random position for the new projectile
                    projectile= pygame.Rect(projectile_x, -PROJECTILE_HEIGHT, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)  #new projectile 
                    projectiles.append(projectile)  

                proj_add_increment = max(400, proj_add_increment - 50) #make the game more challenging over time
                proj_count = 0  

            #key presses
            keys = pygame.key.get_pressed()  #this returns a list of all the keys that are currently being pressed
                    
            if keys[pygame.K_LEFT] and player.x - PLAYER_VELOCITY >= 0: 
                player.x -= PLAYER_VELOCITY  
            if keys[pygame.K_RIGHT]:
                player.x = min(player.x + PLAYER_VELOCITY, WIDTH - player.width) 

            #update the position of the projectiles  
            for projectile in projectiles[:] :  
                projectile.y += PROJECTILE_VELOCITY  #move the projectile down the screen

                if projectile.y > HEIGHT:  #projectile goes off the bottom of the screen gets removed 
                    projectiles.remove(projectile)  

                elif projectile.colliderect(player):  # if the boxes overlap at all
                    offset = (projectile.x - player.x, projectile.y - player.y)
                    if spacecraft_mask.overlap(asteroid_mask, offset):  #only counts as a hit if the visible pixels of both images actually overlap
                        projectiles.remove(projectile)
                        game_state = "game_over"
                        game_over_time = time.time()
                        break

        show_button = False
        if game_state == "playing":
            draw(player, elapsed_time, projectiles)  #this will call the draw function to update the display with the background image
        elif game_state == "game_over":  #if the player is hit by a projectile, we end the game
            show_button = (time.time() - game_over_time) >= GAME_OVER_DELAY
            draw_game_over(elapsed_time, show_button)

        for event in pygame.event.get():
            #if the user clicks the close button, we set run to False to exit the loop and quit the game.
            if event.type == pygame.QUIT:
                run = False
                break

            #F11 (or F, in case F11 is captured by the OS) toggles between windowed and fullscreen, expanding the whole game to fit
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_F11, pygame.K_f):
                toggle_fullscreen()
                player.x = min(player.x, WIDTH - player.width)
                player.y = HEIGHT - PLAYER_HEIGHT

            #dragging the window's corners resizes it while windowed; rescale everything to match
            if event.type == pygame.VIDEORESIZE and not FULLSCREEN:
                WIN = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                rescale(event.w, event.h)
                player.x = min(player.x, WIDTH - player.width)
                player.y = HEIGHT - PLAYER_HEIGHT

            #while game over, the reset button (once it appears) is the only way to start a new game
            if game_state == "game_over" and show_button:
                if event.type == pygame.MOUSEBUTTONDOWN and BUTTON_RECT.collidepoint(event.pos):
                    # reset everything
                    player.x = WIDTH // 2 - player.width // 2   # or your original start position
                    player.y = HEIGHT - PLAYER_HEIGHT
                    projectiles = []
                    proj_count = 0
                    proj_add_increment = 2000  # whatever your original starting value was
                    start_time = time.time()
                    game_state = "playing"
                    game_over_time = None

    pygame.quit()  #this will close the window and quit the game



if __name__ == "__main__":
    main()
