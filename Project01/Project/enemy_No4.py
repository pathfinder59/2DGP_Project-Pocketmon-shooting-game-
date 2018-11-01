import random
import json
import os

from pico2d import *
import math
#import pause_state
from character import Character
import game_framework
from p_bullet import E_bullet
MOVE,IDLE,SHOOT=range(3)

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 13 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ENEMY = 3

class Enemy04(Character):
    def __init__(self, x, y):
        super().__init__(x, y,8)
        Enemy04.image=load_image('trainner.png')
        self.type=3
        self.pattern=random.randint(1,2)
        self.frame=random.randint(0,4)
        self.arriveY=random.randint(600,820)
        self.time=0
        self.shoot_time=0
        self.shoot_angle=0
        self.angle_rate=0
        self.event_que = []
        self.cur_state = MoveState
        self.cur_state.enter(self)

    def update(self,P_bullet_list,player,E_bullet_list):
        # self.time=(self.time+1)%10
        # if self.time%10==0:
        # self.frame=(self.frame+1)%3
        self.frame = (self.frame + FRAMES_PER_ENEMY * ACTION_PER_TIME * game_framework.frame_time) % 3
        i=0
        while i < len(P_bullet_list):
            if math.sqrt((P_bullet_list[i].x-self.x)**2+(P_bullet_list[i].y-self.y)**2)<20 :
                self.hp=self.hp-player.attack
                del P_bullet_list[i]
            else:
                i=i+1
        if self.hp<0:
            return True
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.change_state(event)

        self.cur_state.update(self,E_bullet_list,player)


    def draw(self):
        self.cur_state.draw(self)
        pass

    def change_state(self,  state):
        self.cur_state.exit(self)
        self.cur_state = state
        self.cur_state.enter(self)
        pass


    def add_event(self, event):
        self.event_que.insert(0,event)
        pass


class MoveState:
    def enter(Enemy):
        pass
    def exit(Enemy):
        pass

    @staticmethod

    def update(Enemy,E_bullet_list,player):
        Enemy.y = Enemy.y - RUN_SPEED_PPS*game_framework.frame_time
        if Enemy.y <= Enemy.arriveY:
            Enemy.add_event(IdleState)

    @staticmethod
    def draw(Enemy):
        Enemy.image.clip_draw(int(Enemy.frame) * 70, Enemy.type * 80, 70, 80, Enemy.x, Enemy.y)

    pass


class IdleState:
    def enter(Enemy):
        Enemy.shoot_time = pico2d.get_time()
        pass
    def exit(Enemy):
        pass

    @staticmethod
    def update(Enemy,E_bullet_list,player):
        if pico2d.get_time()-Enemy.shoot_time>=0.5 :
            Enemy.add_event(ShootState)
            pass
    @staticmethod
    def draw(Enemy):
        Enemy.image.clip_draw(int(Enemy.frame) * 70, Enemy.type * 80, 70, 80, Enemy.x, Enemy.y)


class ShootState:
    def enter(Enemy):
        pass
    def exit(Enemy):
        pass

    @staticmethod
    def update(Enemy,E_bullet_list,player):
   ##타입 0 총알생성
        Enemy.shoot_angle= -math.atan2(player.y-Enemy.y,player.x-Enemy.x)/3.1415/2

        if Enemy.pattern==1:
            E_bullet_list.append(E_bullet(Enemy.x,Enemy.y,Enemy.shoot_angle,0,2,0))
            pass
        elif Enemy.pattern==2:
            E_bullet_list.append(E_bullet(Enemy.x, Enemy.y, Enemy.shoot_angle, 0, 3, 0))
            pass
        Enemy.add_event(IdleState)

    @staticmethod
    def draw(Enemy):
        Enemy.image.clip_draw(int(Enemy.frame) * 70, Enemy.type * 80, 70, 80, Enemy.x, Enemy.y)