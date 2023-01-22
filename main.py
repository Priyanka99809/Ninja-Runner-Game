import pygame
from sys import exit
from random import randint
import pygame.time

def display_score():
    current_time=int(pygame.time.get_ticks()/100)-start_time
    score_surface = text_font.render(f'Score: {current_time}', False, 'white') #curr is in f{} because it is number and we want string
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)
    #pygame.draw.rect(screen, 'black', score_rect)  # drawing a rect to score_surface and adding white color
    return current_time
def obstackle_movement(obstackle_list): #shifting all obstackles rect to left by 3 and then printing them on screen
    if obstackle_list:
        for obstackle_rect in obstackle_list:
            obstackle_rect.x-=4.5
            if obstackle_rect.bottom==580: #if obstackle is at ground i.e snail then blit snail
                 screen.blit(snail_surface,obstackle_rect)
            else:
                screen.blit(fly_surface, obstackle_rect)
        #copy only those items in obs list if they are on screen otherwise kill them when they leave so as to
        #avoid reducing performance of game system
        obstackle_list= [obs for obs in obstackle_list if obs.x>-60]
        return obstackle_list
    else:
        return []

def collisions(player,obstackles):
    if obstackles: #if obs list is non empty
        for obs in obstackles:
            if obs.colliderect(player): #if any obs collide with player
                return False
    return True

def player_animation():
    global player_surface,player_index
    if player_rect.bottom<580:
        #jump image of player
        player_surface=player_jump
    else:
        player_index+=0.05 #slowly move to next image in player walk instead of just switching fast
        if player_index>=len(player_walk):
            player_index=0
        player_surface=player_walk[int(player_index)]

#iniatializing pygame
pygame.init()
pygame.display.set_caption("Runner")


#display a window
screen=pygame.display.set_mode((800,700))

# define a clock object to control frame rate at maximum 60frame/sec
clock=pygame.time.Clock()

#creating font
text_font=pygame.font.Font('fonts/ARCADE.TTF',50)
text_font2=pygame.font.Font(None,50)
text_font3=pygame.font.Font('fonts/Minecraft Evenings.otf',40)


#creating obstackles
# creating sky surface to put on display surface screen
snail_surface=pygame.image.load('graphics/snail/snail4.png').convert_alpha() #convert imported image to something pygame can understand easily
 #create a rect around snail and take midbottom of rect and put it at 100,580
obstackle_rect_list=[] #list of enemies


#player
player_walk1=pygame.image.load('graphics/player/player45_walk1.png').convert_alpha()
player_walk2=pygame.image.load('graphics/player/player45_walk2.png').convert_alpha()
player_jump=pygame.image.load('graphics/player/player_jump.png').convert_alpha()
player_walk=[player_walk1,player_walk2]
player_index=0
player_surface=player_walk[player_index]
player_rect=player_surface.get_rect(midbottom=(80,580)) #create a rect around player and take midbottom of rect and put it at 100,580

#fly
fly_walk1=pygame.image.load('graphics/fly/fly3.png').convert_alpha()
fly_walk2=pygame.image.load('graphics/fly/fly4.png').convert_alpha()
fly_walk=[fly_walk1,fly_walk2]
fly_index=0
fly_surface=fly_walk[fly_index]
 #create a rect around player and take midbottom of rect and put it at 100,580

#intro screen player
player_stand=pygame.image.load('graphics/player/player_intro.png').convert_alpha()
player_stand=pygame.transform.scale(player_stand,(300,300))
player_stand_rect=player_stand.get_rect(center=(400,350))

#sky
sky=pygame.image.load('graphics/haunted2.webp').convert()
sky_surface = pygame.transform.scale(sky, (800, 700)) #update image to fit screen size

#road
road_surface=pygame.image.load('graphics/road.webp').convert()
road_surface = pygame.transform.scale(road_surface, (800,120)) #update image to fit screen size

#sound
# jump_sound=pygame.mixer.Sound('audio/jump.mp3')
pygame.mixer.music.load('audio/jump.mp3')
pygame.mixer.music.play()

pygame.mixer.music.set_volume(1)
bg_sound=pygame.mixer.music.load('audio/music.wav')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play()

#font on start screen of game
name_surface = text_font3.render('Ninja Runner', False,'white')  # curr is in f{} because it is number and we want string
name_surface=pygame.transform.scale2x(name_surface)
name_rect = name_surface.get_rect(center=(400, 150)) #for press space to start
name2_surface = text_font2.render('Click on Screen or Press Space to Start', False,'white')  # curr is in f{} because it is number and we want string
name2_rect = name_surface.get_rect(center=(350, 580))

#start background
garden=pygame.image.load('graphics/haunted.jpg').convert()
garden_surface = pygame.transform.scale(garden, (800, 700)) #update image to fit screen size

#variables
game_active=False
start_time=0 #to subtract from current time so as to display time from 0 everytime new game is started
score=0
# display window until close button is pressed
#player gravity
player_gravity=0

#timer
obstackle_event=pygame.USEREVENT+1 # creating a custom event and adding +1 to avoid collisions with pygame events
pygame.time.set_timer(obstackle_event,1500) #set onstacle every 800 ms

#fly timer
fly_animation_timer=pygame.USEREVENT+2;
pygame.time.set_timer(fly_animation_timer,200) #set onstacle every 800 ms


while True:
    for events in pygame.event.get(): #checking all user inputs
        if events.type==pygame.QUIT:
            pygame.quit()
            exit() #to completely end the loop after quit is called
        if game_active==True:
            if events.type==pygame.MOUSEBUTTONDOWN and player_rect.bottom==580:
                 player_gravity= -28 #MOVE PLAYER UPWARDS IF PRESSED BUTTON OF MOUSE
                 pygame.mixer.music.play()

            if events.type==pygame.KEYDOWN:
                 if events.key==pygame.K_SPACE and player_rect.bottom==580:
                     player_gravity= -28

                     bg_sound = pygame.mixer.music.load('audio/music.wav')
                     pygame.mixer.music.set_volume(0.5)
                     pygame.mixer.music.play()

        else:
            if (events.type == pygame.KEYDOWN and events.key == pygame.K_SPACE) or (events.type==pygame.MOUSEBUTTONDOWN):
                game_active = True
                start_time=int(pygame.time.get_ticks()/100)
        if game_active:
            if events.type==obstackle_event:
                if randint(0,2):
                    obstackle_rect_list.append(snail_surface.get_rect(midbottom=(randint(900,1100),580) ))
                else:
                     obstackle_rect_list.append(fly_surface.get_rect(midbottom=(randint(900, 1100), 380)))

            #spawning enemy snail to the right of screen by generating a random no for value of x
            if events.type==fly_animation_timer:
                if fly_index==0: fly_index=1
                elif fly_index==1: fly_index=0
                fly_surface = fly_walk[fly_index]

    if game_active:
         #if game active variable is false pause screen and stop drawing more images
         #block image transfer to put test surface on screen on top left otherwise not visible
         screen.blit(sky_surface,(0,0))
         screen.blit(road_surface,(0,580))


         #fall of the player downwards
         player_gravity +=1
         player_rect.y+=player_gravity #move player downwards exponentially as gravity is global var
         if player_rect.bottom>580: player_rect.bottom=580 #stop the fall at ground level that is if player goes down below grouund level he is back at ground

         #call animation of player
         player_animation()
         screen.blit(player_surface,player_rect)

         #obstackle movement function to spawn enemies by updating obs rect list using function(changing their x dimension)
         obstackle_rect_list=obstackle_movement(obstackle_rect_list)
         score=display_score()

         #COLLISIONS
         game_active=collisions(player_rect,obstackle_rect_list) #call collision function


    else:
        #fill screen with black color
        screen.fill('Black')
        #printing score on screen
        score_msg_surface = text_font2.render(f'SCORE :{score} ', False,'white')  # curr is in f{} because it is number and we want string
        score_msg2_surface = text_font2.render('Press space to Restart', False,'white')  # curr is in f{} because it is number and we want string
        score_msg_rect = score_msg_surface.get_rect(center=(350, 560))
        score_msg2_rect = score_msg2_surface.get_rect(center=(350, 660))
        screen.blit(name_surface,name_rect)
        obstackle_rect_list.clear() #to clear rect list so that game can restart easily otherwise would crash
        screen.blit(player_stand,player_stand_rect)
        if score==0: screen.blit(name2_surface, name2_rect)
        else:
            screen.blit(score_msg_surface, score_msg_rect)
            screen.blit(score_msg2_surface, score_msg2_rect)

    # keys=pygame.key.get_pressed() #get all keys from keyboard as an object and check if key 1 is pressed print 1 pressed
    #update everything
    pygame.display.update()
    clock.tick(60) #while loop will not faster more than 60 times per sec controls the frame rate