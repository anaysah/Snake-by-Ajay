#IMPORTING ALL DEPENDENCIES----------------------------------------------------------------
import pygame
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_UP
from random import randint
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


#INITTILIZING PYGAME-----------------------------------------------------------------------
pygame.init()
win = pygame.display.set_mode((800,500))
win.fill((225,225,225))
pygame.display.set_caption("Snake By Ajay")
icon_surface = resource_path(r"Assets\snake.png")
icon_surface = pygame.image.load(icon_surface)
pygame.display.set_icon(icon_surface)

#SNAKE BODY AND LIST-----------------------------------------------------------------------
snake_list =[[-200,250],[-150,250],[-100,250],[-50,250]]

#REQUIRED VARIABLES------------------------------------------------------------------------
def reset_all_var():
    global direction,moved,food_eated,firstrgb,secondrgb,thirdrgb,score,game_active
    direction = "RIGHT"
    moved = True
    food_eated = False
    firstrgb = 250
    secondrgb =0
    thirdrgb = 0
    score = 0
    game_active = True

reset_all_var()

#SNAKEFOOD---------------------
food_pos_x,food_pos_y  =400,250
food_pos=[food_pos_x-(food_pos_x%50),food_pos_y-(food_pos_y%50)]
food_img = resource_path(r"Assets\apple.png")
food_img = pygame.image.load(food_img)
food_rect = food_img.get_rect(topleft=(food_pos_x,food_pos_y))

#GAMEOVER TEXT-----------------------------------------------------------------------------
gameover_font = resource_path(r"Assets\Glory-Bold.ttf")
gameover_font=pygame.font.Font(gameover_font,100,bold=True)
gameover_text= gameover_font.render("GAME OVER","AA",(255,247,72))  #(0, 162, 255)
gameover_text_rect = gameover_text.get_rect(center=(400,250))

presssapce_font = resource_path(r"Assets\Glory-Bold.ttf")
presssapce_font=pygame.font.Font(presssapce_font,60,bold=True)
pressspace_text= presssapce_font.render("press space to replay","AA",(0, 247, 255))
pressspace_text_rect = pressspace_text.get_rect(center=(400,320))

gameover_score_font = resource_path(r"Assets\Glory-Bold.ttf")
gameover_score_font = pygame.font.Font(gameover_score_font,60,bold=True)

#SCORE BOARD ------------------------------
score_font = resource_path(r"Assets\Merkur-j147.otf")
score_font = pygame.font.Font(score_font,40)
score_text = score_font.render(f"Score {score}","AA",(0, 153, 204))
score_text_rect = score_text.get_rect(topleft=(10,10))


clock = pygame.time.Clock()
runing = True
while runing:
    clock.tick(7)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
        elif event.type == pygame.KEYDOWN :
            if event.key==K_SPACE and game_active==False:
                snake_list =[[-200,250],[-150,250],[-100,250],[-50,250]]
                reset_all_var()
            elif event.key==K_DOWN and direction in ["LEFT", "RIGHT"]:
                direction="DOWN";break
            elif event.key==K_UP and direction in ["LEFT", "RIGHT"]:
                direction="UP";break
            elif event.key==K_RIGHT and direction in ["UP", "DOWN"]:
                direction="RIGHT";break
            elif event.key==K_LEFT and direction in ["UP", "DOWN"]:
                direction="LEFT";break

    if game_active:        
    #REGULAR MOMENT IN PARTICULAR DIRECTION----------------------------------------------------
        if direction=="DOWN":
            snake_list[-1][1]+=50
        elif direction=="UP":
            snake_list[-1][1]-=50
        elif direction=="RIGHT":
            snake_list[-1][0]+=50
        elif direction=="LEFT":
            snake_list[-1][0]-=50

    #WINDOW BACKGROUND-------------------------------------------------------------------------
        win.fill((162,209,73))
        for i in range(10):
            for r in range(16):
                if (i%2==0 and r%2==0) or (i%2!=0 and r%2!=0):
                    background = pygame.draw.rect(win,(170,215,81),(r*50,i*50,50,50))


    #FOOD BODY PART----------------------------------------------------------------------------
        win.blit(food_img,food_rect)
        if food_eated:
            food_pos_x,food_pos_y  =randint(0,750),randint(0,450)
            food_rect.x,food_rect.y=[food_pos_x-(food_pos_x%50),food_pos_y-(food_pos_y%50)]
            food_eated=False

    #SNAKE HEAD--------------------------------------------------------------------------------
        snake_rect = pygame.draw.rect(win,"Blue",(snake_list[-1][0],snake_list[-1][1],50,50))
    #SNAKE BODY AND COLOR----------------------------------------------------------------------
        for r in snake_list[::-1]:    
            rand_color = (firstrgb,secondrgb,thirdrgb)
            snake_body = pygame.draw.rect(win,rand_color,(r[0],r[1],50,50))
            if secondrgb+20<250:
                secondrgb+=20
            elif firstrgb-20>0:
                firstrgb-=20
            elif thirdrgb+20<250:
                thirdrgb+=20
            elif secondrgb-20>0:
                secondrgb-=20

        firstrgb=250
        secondrgb=0
        thirdrgb=0

    #GAME OVER-----------------------------------------------------------------------
        snake_pos = snake_list[-1]
        for r in snake_list[0:-1]:
            if r==snake_pos:
                game_active=False
                break
        if snake_pos[0]>=800 or snake_pos[0]<0 or snake_pos[1]>=500 or snake_pos[1]<0 or not game_active:
            game_active=False
            continue


    #CHANGING SNKAE_LIST-----------------------------------------------------------------------
        last_body_part = snake_list.pop(0)
        snake_list.append([snake_rect.x,snake_rect.y])

    #COLLISION WITH FOOD-----------------------------------------------------------------------
        if snake_rect.colliderect(food_rect):
            food_eated=True
            snake_list.insert(0,last_body_part)
            score+=1
        score_text = score_font.render(f"Score {score}","AA",(0, 153, 204))
        win.blit(score_text,score_text_rect)

    else:
        win.fill((60,26,91))  #(162,209,73)
        win.blit(gameover_text,gameover_text_rect)
        win.blit(pressspace_text,pressspace_text_rect)
        # score = "SCORE:" + str(score)
        gameover_score_text = gameover_score_font.render(f"SCORE: {score}","AA",(0, 247, 255))
        gameover_score_rect = gameover_score_text.get_rect(center =(400,180))
        win.blit(gameover_score_text,gameover_score_rect)

    pygame.display.update()