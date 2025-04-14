import pygame 
import time
import random
pygame.font.init()

WIDTH,HEIGHT= 900,900
WIN = pygame.display.set_mode((HEIGHT,WIDTH))
pygame.display.set_caption("space Dodge")

BG = pygame.transform.scale(pygame.image.load("bg.jpeg"), (WIDTH,HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

PLAYER_VEL = 5
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 5

FONT = pygame.font.SysFont("comicsans",30)

def draw(player,elapsed_time,stars):
   WIN.blit(BG,(0,0))

   
   time_text =  FONT.render(f"Time: {round(elapsed_time)}s" ,1 , "white")#1 is for anti aliasing
   
   WIN.blit(time_text,(10,10))#to put time on screen
   
   pygame.draw.rect(WIN,(255,0,0),player)

   for star in stars:
      pygame.draw.rect(WIN, "white", star)


   pygame.display.update()#applys the drawing

def main():
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False


    while run:

        star_count += clock.tick(60)#delay the while loop (max 60 times in a minute)
        
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
           for _ in range(3):
              star_x =random.randint(0,WIDTH-STAR_WIDTH) 
              star = pygame.Rect(star_x, -STAR_HEIGHT,STAR_WIDTH,STAR_HEIGHT)#gonna get negative y
              stars.append(star)  # genrate 3 random start



           star_add_increment = max(200, star_add_increment-50)#50 milisecond faster every time
           star_count = 0


        for event in  pygame.event.get():
         if event.type == pygame.QUIT:
            run = False
            break
         

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
           player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL <= WIDTH:
           player.x += PLAYER_VEL



        for star in stars[:]: #making copy of star list , removing stars that hav ehit the bottom
            star.y += STAR_VEL
            if star.y > HEIGHT:
               stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
               stars.remove(star)  #to see if star is colliding
               hit = True
               break




      
        if hit :
           lost_text = FONT.render("you lost!",2 ,"white")
           WIN.blit(lost_text,(WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
           pygame.display.update()
           pygame.time.delay(4000)
           break
        
        draw(player, elapsed_time,stars)
         
    pygame.quit()

if __name__ == "__main__":
   main()