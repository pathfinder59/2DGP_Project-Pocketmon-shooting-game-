import random
import json
import os

from pico2d import *
import math
#import pause_state
import game_framework
import start_state
import over_state
from player import Player
from p_bullet import P_bullet
from character import Character
from score import Score
from life import Life
from enemy import Enemy

GAME_HEIGHT = 875
GAME_WIDTH = 590
lFrame=0


P_bullet_list=None #플레이어 탄알 리스트
Enemy_list=[]  #적 탄알 리스트

name = "PlayState"


screen=None
score=None
player=None
life=None
E_time=0


def pause():
    pass

def enter():
    global screen,score,player,life,P_bullet_list
    screen=load_image('GAMEPrint.png')
    player=Player(590/2,100,3,start_state.character)
    P_bullet_list = [P_bullet(player.x,player.y)]
    score=Score()
    life=Life()



def exit():
    global screen,bullet_image,score,player,life,P_bullet_list
    del(bullet_image)
    del(screen)
    del(player)
    del(life)
    del(score)
    for i in range(len(P_bullet_list)):
        del(P_bullet_list[0])
    for i in range(len(Enemy_list)):
        del(Enemy_list[0])



def pause():
    pass



def resume():
    pass


def handle_events():

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.push_state(over_state)
        elif event.type==SDL_KEYDOWN and event.key==SDLK_SPACE:
            player.skill()


def update():
    global P_bullet_list,E_time,player
    score.update()
    life.update()
    player.update(P_bullet_list)
    i=0
    while i<len(P_bullet_list):
        if P_bullet_list[i].update():
            del P_bullet_list[i]
        else:
            i=i+1

    i=0
    while i < len(Enemy_list):
        if Enemy_list[i].update(P_bullet_list,player) :
            del Enemy_list[i]
        else:
            i=i+1

    E_time=(E_time+1)%100

    if E_time%100==0:
        Enemy_list.append(Enemy(player.x,GAME_HEIGHT+15,10))


def draw():
    global  screen,P_bullet_list
    clear_canvas()
    screen.draw(GAME_WIDTH / 2, GAME_HEIGHT / 2)
    life.draw(player)
    score.draw()
    for i in range(len(P_bullet_list)):
        P_bullet_list[i].draw(player)
    for i in range(len(Enemy_list)):
        Enemy_list[i].draw()

    player.draw()

    update_canvas()
    delay(0.02)




