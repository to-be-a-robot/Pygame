import pygame
import random 
import time 
pygame.font.init()  # Initialize the font module


# creating a window
# thisis the place to draw different objects and have your game running

WIDTH, HEIGHT= 1000, 600 # the dimensions of the window in pixels
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # creating the window

#caption for the window - this will be the name at the top of the window
pygame.display.set_caption(" Rocks on My Head ") # setting the caption for the window

#setting a background image
BG= pygame.transform.scale(pygame.image.load("images/green_background.jpg"), (WIDTH, HEIGHT)) # transforming scale of background to fit the window size

#Player attributes
PLAYER_WIDTH, PLAYER_HEIGHT= 50, 50 # dimensions of the player in pixels
PLAYER_VELOCITY= 30# speed of the player in pixels per frame

#Projectile attributes
PROJECTILE_WIDTH= 10 # width of each projectile in pixels
PROJECTILE_HEIGHT= 20 # height of each projectile in pixels
PROJECTILE_VELOCITY= 5 # speed of the projectiles in pixels per frame

#setting a font for the timer
FONT= pygame.font.SysFont("comicsans", 30) # setting the font for the timer display

def draw(player, elapsed_time, projectiles):  #this function will draw the background image and the player on the window

    WIN.blit(BG, (0,0))  #blit is a method that draws one image onto another || (0,0) is the top left corner of the window where the image will be drawn

    timer_text= FONT.render(f"Time: {round(elapsed_time)}s", 1, "maroon") #this will render the elapsed time in seconds on the window
    WIN.blit(timer_text, (850,10))  #this will draw the timer text on the window at position (10,10)

    pygame.draw.rect(WIN, "red", player) #this will draw a red rectangle on the window to represent the player

    for projectile in projectiles:  #this will draw each projectile on the window
        pygame.draw.rect(WIN, "yellow", projectile)  #this will draw a yellow rectangle on the window to represent the projectile

    pygame.display.update()  #this updates the display to show the new frame


#main game loop : in pygame, the main game loop is where the game runs continuously until the user quits. 
#It handles events, updates game state, and renders graphics.

def main():
    run = True 

    player =pygame.Rect(0, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT) #positon of the player on the screen

    clock= pygame.time.Clock() #this will help us control the frame rate of the game

    start_time = time.time()  #this will get the current time in seconds since the epoch (January 1, 1970)
    elapsed_time = 0  #this will keep track of the elapsed time since the start of the game

    #adding projectiles
    proj_add_increment = 2000 # first projectile will be at 2000 'milliseconds'
    proj_count = 0 #this will keep track of when to add a new projectile to the game
    
    projectiles=[] #this will be a list to hold the projectiles that are currently on the screen

    hit= False 
    

    while run:
        proj_count += clock.tick(20)  #this will limit the frame rate to 60 frames per second
        elapsed_time = time.time() - start_time  #this will calculate the elapsed time since the start of the game

        if proj_count >= proj_add_increment:  #if the proj_count is greater than  the proj_add_increment, we will add a new projectile to the game

            for _ in range(3):  #this will add 3 projectiles to the game at once
                projectile_x= random.randint(0, WIDTH - PROJECTILE_WIDTH)  #this will generate a random x position for the new projectile
                projectile= pygame.Rect(projectile_x, -PROJECTILE_HEIGHT, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)  #this will create a new projectile at the random x position and y position of 0 (top of the screen)
                projectiles.append(projectile)  #this will add the new projectile to the list of projectiles

            proj_add_increment = max(200, proj_add_increment - 50) #this will decrease the proj_add_increment by 50 milliseconds, but not below 200 milliseconds, to make the game more challenging over time
            proj_count = 0  #this will reset the proj_count to 0 so that we can add a new projectile after the next proj_add_increment


        for event in pygame.event.get():  #pygame.event.get() returns a list of all the events that have occurred since the last time it was called.

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
        # if keys[pygame.K_UP]: 
        #     player.y = max(player.y - PLAYER_VELOCITY, 0)  
        # if keys[pygame.K_DOWN]:  
        #     player.y = min(player.y + PLAYER_VELOCITY, HEIGHT - player.height)

        #update the position of the projectiles  
        for projectile in projectiles[:] :  
            projectile.y += PROJECTILE_VELOCITY  #this will move the projectile down the screen by the PROJECTILE_VELOCITY

            if projectile.y > HEIGHT:  #if the projectile goes off the bottom of the screen, we remove it from the list of projectiles
                projectiles.remove(projectile)  #this will remove the projectile from the list of projectiles

            elif projectile.y + projectile.height >= player.y and projectile.colliderect(player):  #if the projectile collides with the player, we end the game
                projectiles.remove(projectile) 
                hit= True
                break

        if hit:  #if the player is hit by a projectile, we end the game
            lost_text= FONT.render(f"You lost! Time survived: {round(elapsed_time)}s", 1, "maroon")  #this will render the text to display when the player loses
            WIN.blit(lost_text, (WIDTH//2 - lost_text.get_width()//2, HEIGHT//2 - lost_text.get_height()//2))  #this will draw the lost text on the window at the center of the screen
            pygame.display.update()  
            pygame.time.delay(4000)  #this will pause the game for 3 seconds to allow the player to read the lost text
            run = False  #this will exit the main game loop


        draw(player,elapsed_time,projectiles)  #this will call the draw function to update the display with the background image

    pygame.quit()  #this will close the window and quit the game



if __name__ == "__main__":
    main()
