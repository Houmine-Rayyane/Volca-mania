'''blabla'''
import pygame 
from pygame import mixer
from random import randint

pygame.init()

#Drawing the Window
WIDTH, HEIGHT = 1000 , 750
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Dragonhunt')
game_icon = pygame.image.load('images/icon.jpg')
pygame.display.set_icon(game_icon)
FPS=60
clk = pygame.time.Clock()
txt_font = pygame.font.Font('fonts/gamefont.ttf',30)
background_surf =pygame.image.load('images/Background.png').convert()
txt_surf = txt_font.render('Volca-Mania', False, 'Black').convert()
game_name = txt_font.render('Volca-Mania',False, 'Black')
game_name_rect = game_name.get_rect(center = (500,100))

#Game audio 
mixer.music.load('audio/music.mp3')
mixer.music.play(-1)



#Player
villain_surf = pygame.image.load('images/villain.png')
villain_rect = villain_surf.get_rect(midbottom=(100,560))
villain2_surf = pygame.transform.scale2x(villain_surf)
villain2_rect = villain_surf.get_rect(midbottom = (370,330))
villain_grav = 0

#Enemies
fireball_surf = pygame.image.load('images/fireball.png').convert_alpha()
fireball_rect = fireball_surf.get_rect(bottomright =(800,540))
dragon_surf = pygame.image.load('images/dragons/dragon.png').convert_alpha()
dragon_rect = dragon_surf.get_rect(bottomright =(800,540))

#Game message
game_mess = txt_font.render('Press space to run',False, 'Black')
game_mess_rect = game_name.get_rect(center = (400,600))


game_play = True
start_time = 0
score = 0

#New event
enemies_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemies_timer,1000)
enemies_list = [ ]

def enemies_move(liste):
    if liste:
        for enemy in liste:
            enemy.x -= 8
            if enemy.bottom == 540:
                WIN.blit(fireball_surf, enemy) 
            else:
                WIN.blit(dragon_surf, enemy) 
        liste = [enemy for enemy in liste if enemy.x > -100 ]       
        return liste
    else:
        return []

def collisions(player, enemies):
    player_mask = pygame.mask.from_surface(villain_surf)
    for enemy in enemies:
        enemy_mask = pygame.mask.from_surface(fireball_surf)
        pos = (enemy.x - player.x, enemy.y - player.y)
        if player_mask.overlap(enemy_mask, pos):
            return False
    return True
def display_score():
    curr_time = (pygame.time.get_ticks() // 1000) - start_time
    score_surf = txt_font.render(f'Score :{curr_time}', False,'Black')
    score_rect = score_surf.get_rect(center = (200,130))
    WIN.blit(score_surf, score_rect)   
    return curr_time


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            #Adding the exit button X
            exit()
        #keyboard controll
        if game_play:
            if event.type == pygame.KEYDOWN:
                if event.key ==  pygame.K_SPACE and villain_rect.bottom >= 570:
                    villain_grav = -20
        else:
            if event.type == pygame.KEYDOWN and event.key ==  pygame.K_SPACE:
                game_play = True
                fireball_rect.left = 1000
                start_time = (pygame.time.get_ticks() // 1000)
                mixer.music.play(-1)
                
        
        if event.type == enemies_timer and game_play: 
            if randint(0,2):
                enemies_list.append(fireball_surf.get_rect(bottomright =(1000,540)))          
            else :
                enemies_list.append(dragon_surf.get_rect(bottomright =(1000,350)))       
                
            
    if game_play:
        #printing the background for the game       
        WIN.blit(background_surf,(0,0))
        #printing the text surface
        WIN.blit(txt_surf,(330,50))
        #printing the player
        villain_grav +=1
        villain_rect.y += villain_grav
        if villain_rect.bottom >= 570:villain_rect.bottom = 570
        WIN.blit(villain_surf,villain_rect)
        
        enemies_list = enemies_move(enemies_list)
        game_play = collisions(villain_rect,enemies_list)
        score= display_score()
        
    else:
        mixer.music.stop()
        WIN.fill((255,178,102))
        WIN.blit(villain2_surf,villain2_rect)
        enemies_list.clear()
        score_mess = txt_font.render(f'Your score:{score}', False, 'Black')
        score_mess_rect = score_mess.get_rect(center=(500, 600))
        WIN.blit(game_name, game_name_rect)
        if score == 0:
            WIN.blit(game_mess,game_mess_rect)
        else:
            WIN.blit(score_mess,score_mess_rect)
        
            
                    
    #updating the window 
    pygame.display.update()
    #Setting the frequency
    clk.tick(FPS)

 