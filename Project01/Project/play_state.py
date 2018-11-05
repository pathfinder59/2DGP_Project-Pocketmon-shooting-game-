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
from score import Score
from life import Life
from enemy_No1 import Enemy01
from enemy_No2 import Enemy02
from enemy_No3 import Enemy03
from enemy_No4 import Enemy04
from enemy_No5 import Enemy05

Enemy_table={
    0:Enemy01,1:Enemy02,2:Enemy03,3:Enemy04,4:Enemy05
}
GAME_HEIGHT = 875
GAME_WIDTH = 590
E_bullet_list=[]
P_bullet_list=[] #플레이어 탄알 리스트
Enemy_list=[]  #적 탄알 리스트
count=1
name = "PlayState"

screen=None
score=None
player=None
life=None
E_time=None


def pause():
    pass

def enter():
    global screen,score,player,life,P_bullet_list,E_time,B_time,count
    screen=load_image('GAMEPrint.png')
    player=Player(590/2,100,3,start_state.character)
    P_bullet_list = [P_bullet(player.x,player.y)]
    score=Score()
    count = 1
    life=Life()
    E_time=pico2d.get_time()
    B_time = pico2d.get_time()



def exit():
    global screen,score,player,life,P_bullet_list,E_bullet_list
    del(screen)
    del(player)
    del(life)
    del(score)
    for i in range(len(P_bullet_list)):
        del(P_bullet_list[0])
    for i in range(len(E_bullet_list)):
        del(E_bullet_list[0])
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
            if player.skillSwitch==False:
                player.skill()
        else:
            player.handle_event(event)


def update():
    global P_bullet_list,E_time,player,E_bullet_list,count,B_time
    score.update()
    life.update()
    if player.update(P_bullet_list,E_bullet_list):
        pass
    else :
        game_framework.push_state(over_state)
        pass   #게임오버 구현 미완성
    i=0

    while i<len(P_bullet_list):
        if P_bullet_list[i].update():
            del P_bullet_list[i]
        else:
            i=i+1

    i = 0

    while i < len(E_bullet_list):
        if E_bullet_list[i].update():
            del E_bullet_list[i]
        else:
            i = i + 1

    i=0

    while i < len(Enemy_list):
        if Enemy_list[i].update(P_bullet_list,player,E_bullet_list) :
            del Enemy_list[i]
        else:
            i=i+1


    #E_time=(E_time+1)%2000
    if int(pico2d.get_time()-B_time)>=20:
        B_time=pico2d.get_time()
        if count<3:
            count+=1
        Enemy_list.append(Enemy_table[4](random.randint(200,250), GAME_HEIGHT + 15))

    elif int(pico2d.get_time()-E_time)>=3:
        E_time=pico2d.get_time()
        for i in range(count):
            Enemy_list.append(Enemy_table[random.randint(0,3)](random.randint(20,550),GAME_HEIGHT+15))



def draw():
    global  screen,P_bullet_list
    clear_canvas()
    screen.draw(GAME_WIDTH / 2, GAME_HEIGHT / 2)
    life.draw(player)
    score.draw(224,30)
    for i in range(len(P_bullet_list)):
        P_bullet_list[i].draw(player)

    for i in range(len(Enemy_list)):
        Enemy_list[i].draw()
    for i in range(len(E_bullet_list)):
        E_bullet_list[i].draw(player)


    player.draw()

    update_canvas()
    #delay(0.02)




