import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First game!")



WHITE = (255,255,255) #in pygame all colors are rgb! 
BLACK = (0,0,0)
RED = (255, 0,0)
YELLOW = (255, 255, 0)
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
BORDER = pygame.Rect(WIDTH//2, 0,10,HEIGHT) #not drawing recct from middle , drawing it from 0,0

BULLET_HIT_SOUND = pygame.mixer.Sound('assets/grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('assets/gun+silencer.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comiscsans' , 100)
FPS  = 60 # how fast i wnt my game to run

SPACESHIP_WIDTH, SPACSHIP_HEIGHT = 60,40

YELLOW_HIT = pygame.USEREVENT + 1 # this just represent the code or the number for a custom user event 
RED_HIT = pygame.USEREVENT + 2 # we just add 1 and 2 have a unique event id


YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACSHIP_HEIGHT,SPACESHIP_WIDTH)) ,90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACSHIP_HEIGHT,SPACESHIP_WIDTH)) ,270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')),(WIDTH,HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health): # take as an argument whatever I wanna draw
    WIN.blit(SPACE, (0,0))
   # WIN.fill(WHITE)  # we have to update the display for this to work
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10,10)) #bliting will be right at the edge #10 from the right wall, 10 from the top wall
    WIN.blit(yellow_health_text, (10,10))
    WIN.blit(YELLOW_SPACESHIP,(yellow.x, yellow.y)) # use blit when we want to draw a surface on the screen
    #IN PYTHON THE TOP LEFT IS (0,0)
    WIN.blit(RED_SPACESHIP, (red.x, red.y))  
    #rather than drwing yellow spaceship and red spaceship at predefined locations,
    # i am gonna draw it wherever position my red and yellow argument are at
    # this way i can modify red and yellow, and when passed to draw_window
    #it will change where we are drawing these rectangles
    
    

    for bullet in red_bullets:
          pygame.draw.rect(WIN , RED, bullet)


    for bullet in yellow_bullets:
          pygame.draw.rect(WIN , YELLOW, bullet)

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
     if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  #left
            yellow.x -= VEL
     if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  #right #it will make sure we are not over the border
            yellow.x += VEL
     if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  #up
            yellow.y -= VEL
     if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  #down
            yellow.y += VEL  #top left is 0,0  , so to go down we are adding

def red_handle_movement(keys_pressed, red):
     if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  #left
            red.x -= VEL
     if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  #right
            red.x += VEL
     if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  #up
            red.y -= VEL
     if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  #down
            red.y += VEL  #top left is 0,0  , so to go down we are adding

def handle_bullets(yellow_bullets, red_bullets, yellow, red): #move the bullets, handle the collision of  the bullets,handle removing bullets
    for bullet in yellow_bullets:
          bullet.x += BULLET_VEL #moving
          if red.colliderect(bullet):#rect representing yello has collided with rect representing bullet
                pygame.event.post(pygame.event.Event(RED_HIT))
                yellow_bullets.remove(bullet)
          elif bullet.x > WIDTH:
                yellow_bullets.remove(bullet)

          

    for bullet in red_bullets:
          bullet.x -= BULLET_VEL #moving
          if yellow.colliderect(bullet):#rect representing yello has collided with rect representing bullet
                pygame.event.post(pygame.event.Event(YELLOW_HIT))
                red_bullets.remove(bullet)

          elif bullet.x < 0 :
                red_bullets.remove(bullet)


def draw_winner(text):
     draw_text = WINNER_FONT.render(text,1,WHITE)
     WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2 ))
     pygame.display.update()
     pygame.time.delay(5000)



def main():
    red = pygame.Rect(700,300, SPACESHIP_WIDTH,SPACSHIP_HEIGHT)
    yellow = pygame.Rect(100,300, SPACESHIP_WIDTH,SPACSHIP_HEIGHT)
    
    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    
    run = True
    while run:   #this is game loop
        clock.tick(FPS) #control the speed of the while loop

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #if user quits
                run = False
                pygame.quit()



            if event.type == pygame.KEYDOWN:   # we dont want player to just spam bullets, have to press the key each time
                  if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 -2 ,10,5)  # we want bullets to com eout of the charachter
                        yellow_bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()
                        
                  if event.key == pygame.K_RSHIFT and len(red_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(red.x , red.y + red.height//2 -2 ,10,5)  # we want bullets to com eout of the charachter
                        red_bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()
                    # WE WANT TWO SLASHES FOR INTEGER DIVISION so we dont get any floating point issues
            if event.type == RED_HIT:
              red_health -= 1
              BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
              yellow_health -= 1
              BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
             winner_text = "Yellow Wins!"
        if yellow_health <= 0:
             winner_text = "RED Wins!"

        if winner_text != "":
               draw_winner(winner_text)
               break
        

        #print(red_bullets, yellow_bullets)
        keys_pressed = pygame.key.get_pressed() #what keys are currently being pressed 
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
       
        
        handle_bullets(yellow_bullets,red_bullets , yellow, red)

        #red.x += 1 #moving red spaceship 1 window
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health )
        
    main()



if __name__ == "__main__":  # we are only gonna run thids main function if we ran this file directly
    main()