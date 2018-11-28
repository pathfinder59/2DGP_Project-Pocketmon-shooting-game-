import random
import json
import os

from pico2d import *
import math

import game_framework
import start_state
import over_state
import pause_state

from turtle import Turtle
from lizard import Lizard
from grass import Grass
from gameBullet import Player_bullet
from administrator import Administrator

from score import Score
from life import Life

from lineShooter import LineShooter
from spinShooter import SpinShooter
from pinWheelShooter import PinWheelShooter
from flowerShooter import FlowerShooter
from aimShooter import AimShooter


Player_type_table={0:Turtle, 1:Lizard,2:Grass}
Enemy_table={
    0:LineShooter,1:PinWheelShooter,2:SpinShooter,3:AimShooter,4:FlowerShooter
}
GAME_HEIGHT = 875
GAME_WIDTH = 590
E_bullet_list=[]
P_bullet_list=[] #플레이어 탄알 리스트
Enemy_list=[]  #적 탄알 리스트
count=1
name = "PlayState"

back_groundImage=None
score=None
player=None
life=None
backGround=None
fileLink='C:\\Users\\jack\Documents\\GitHub\\2DGP_Project\\Project01\\Project\\'
E_time=None
score_renew=False

class BackGround:
    def __init__(self):
        BackGround.Image = load_image(fileLink + 'Screen\\GAMEPrint.png')
        BackGround.bgm=load_music(fileLink+'Screen\\playMusic.mp3')
        BackGround.bgm.set_volume(40)
        BackGround.bgm.repeat_play()
    def update(self):
        pass
    def draw(self):
        BackGround.Image.draw(GAME_WIDTH / 2, GAME_HEIGHT / 2)
        pass
    def exit(self):
        BackGround.bgm.stop()



def enter():
    global backGround,score,player,life,P_bullet_list,E_time,B_time,count,admin
    backGround=BackGround()
    player=Player_type_table[start_state.character](590/2,100,3)
    P_bullet_list = [Player_bullet(player.x,player.y)]
    score=Score()
    count = 1
    admin=Administrator()
    life=Life()
    E_time=pico2d.get_time()
    B_time = pico2d.get_time()
def pause():
    backGround.exit()
    pass


def exit():
    global backGround,score,player,life,P_bullet_list,E_bullet_list
    backGround.exit()
    del(backGround)
    del(player)
    del(life)
    del(score)
    for i in range(len(P_bullet_list)):
        del(P_bullet_list[0])
    for i in range(len(E_bullet_list)):
        del(E_bullet_list[0])
    for i in range(len(Enemy_list)):
        del(Enemy_list[0])

def get_Player():
    return player
def get_pBulletList():
    return P_bullet_list
def get_eBulletList():
    return E_bullet_list
def get_EnemyList():
    return Enemy_list
def pause():
    pass

def turn_on_music():
    backGround.bgm.repeat_play()
    pass


def resume():
    pass


def handle_events():

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            backGround.exit()
            game_framework.push_state(over_state)
        elif event.type==SDL_KEYDOWN and event.key==SDLK_p:
            game_framework.push_state(pause_state)
        elif event.type==SDL_KEYDOWN and event.key==SDLK_SPACE:
            if player.skillSwitch==False:
                player.skill()
        else:
            player.handle_event(event)


def update():
    global score_renew,P_bullet_list,E_time,player,E_bullet_list,count,B_time
    score.update()
    life.update()
    if player.update(P_bullet_list,E_bullet_list):
        pass
    else :
        if start_state.bestScore.current_score<score.current_score:
            start_state.bestScore.current_score=score.current_score
            score_renew=True
        game_framework.push_state(over_state)

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
            score.current_score+=Enemy_list[i].score
            del Enemy_list[i]
        else:
            i=i+1



    if int(pico2d.get_time()-B_time)>=60:
        B_time=pico2d.get_time()
        if count<3:
            count+=1
        Enemy_list.append(Enemy_table[4](random.randint(200,250), GAME_HEIGHT + 15))

    elif int(pico2d.get_time()-E_time)>=3:
        E_time=pico2d.get_time()
        admin.update()




def draw():
    global  back_groundImage,P_bullet_list
    clear_canvas()

    backGround.draw()
    life.draw(player)
    for i in range(len(P_bullet_list)):
        P_bullet_list[i].draw(player)
    for i in range(len(Enemy_list)):
        Enemy_list[i].draw()
    for i in range(len(E_bullet_list)):
        E_bullet_list[i].draw(player)
    score.draw(224, 30)

    player.draw()

    update_canvas()




