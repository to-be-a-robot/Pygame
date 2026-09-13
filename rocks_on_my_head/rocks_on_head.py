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
        for (r, g, b, a) in pixels
    ]
    img.putdata(new_pixels)
    return pygame.image.fromstring(img.tobytes(), img.size, 'RGBA').convert_alpha()


# creating a window

WIDTH, HEIGHT= 1000, 600 # the dimensions of the window in pixels
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # creating the window

#caption for the window - this will be the name at the top of the window
pygame.display.set_caption(" Rocks on My Head")

#setting a background image
BG= pygame.transform.scale(pygame.image.load(os.path.join(IMAGES_DIR,'space_blue.jpg')), (WIDTH, HEIGHT))

#Player attributes
PLAYER_WIDTH, PLAYER_HEIGHT= 150, 150
PLAYER_VELOCITY= 30
spacecraft = load_image_no_bg(os.path.join(IMAGES_DIR,'spacecraft.jpg'), (PLAYER_WIDTH, PLAYER_HEIGHT))
spacecraft_mask = pygame.mask.from_surface(spacecraft)

#Projectile attributes
PROJECTILE_WIDTH=  50 
PROJECTILE_HEIGHT= 50 
PROJECTILE_VELOCITY= 5 
asteroid = load_image_no_bg(os.path.join(IMAGES_DIR,'asteroid.jpg'), (PROJECTILE_WIDTH, PROJECTILE_HEIGHT))
asteroid_mask = pygame.mask.from_surface(asteroid) 


#setting a font for the timer
FONT= pygame.font.SysFont("comicsans", 30) # setting the font 

def draw(player, elapsed_time, projectiles): 

    WIN.blit(BG, (0,0)) # background

    timer_text= FONT.render(f"Time: {round(elapsed_time)}s", 1, "white") #timer
    WIN.blit(timer_text, (850,10))  # position of timer

    WIN.blit(spacecraft, (player.x, player.y)) #spacecraft image at the player's position

    for projectile in projectiles:  #this will draw each projectile on the window
        WIN.blit(asteroid, (projectile.x, projectile.y))  #this will draw the asteroid image at the projectile's position

    pygame.display.update()  #this updates the display to show the new frame


def main():
    run = True 

    player =pygame.Rect(WIDTH//2 - PLAYER_WIDTH//2, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT) #spacecraft at the bottom middle 

    clock= pygame.time.Clock() 

    start_time = time.time()  #current time in seconds
    elapsed_time = 0  

    #adding projectiles
    proj_add_increment = 2000 # first projectile @ 2000 'milliseconds'
    proj_count = 0 #this will keep track of when to add a new projectile to the game
    
    projectiles=[] #this will be a list to hold the projectiles that are currently on the screen

    hit= False 
    

    while run:

        proj_count += clock.tick(20)  # limit the frame rate to 60 frames per second
        elapsed_time = time.time() - start_time  # elapsed time since the start of the game

        if proj_count >= proj_add_increment:  #if the proj_count is greater than  the proj_add_increment, we will add a new projectile to the game

            for _ in range(3):  
                projectile_x= random.randint(0, WIDTH - PROJECTILE_WIDTH)  #random position for the new projectile
                projectile= pygame.Rect(projectile_x, -PROJECTILE_HEIGHT, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)  #new projectile 
                projectiles.append(projectile)  

            proj_add_increment = max(200, proj_add_increment - 50) #make the game more challenging over time
            proj_count = 0  

        for event in pygame.event.get():  
            #if the user clicks the close button, we set run to False to exit the loop and quit the game.
            if event.type == pygame.QUIT:
                run = False  
                break 


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
                    hit= True
                    break

        if hit:  #if the player is hit by a projectile, we end the game
            lost_text= FONT.render(f"You lost! Time survived: {round(elapsed_time)}s", 1, "maroon")  # player loses
            WIN.blit(lost_text, (WIDTH//2 - lost_text.get_width()//2, HEIGHT//2 - lost_text.get_height()//2))  
            pygame.display.update()  
            pygame.time.delay(4000)  
            run = False  #this will exit the main game loop


        draw(player,elapsed_time,projectiles)  #this will call the draw function to update the display with the background image

    pygame.quit()  #this will close the window and quit the game



if __name__ == "__main__":
    main()
