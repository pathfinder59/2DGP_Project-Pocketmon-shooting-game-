import random
import json
import os

from pico2d import *
import math
#import pause_state
from character import Character
import game_framework
from gameBullet import Enemy_bullet
MOVE,IDLE,SHOOT=range(3)


PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 13 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ENEMY = 3

class PinWheelShooter(Character):
    def __init__(self, x, y):
        super().__init__(x, y,5)

        self.type=1
        self.pattern=random.randint(1,2)
        self.frame=random.randint(0,4)
        self.arriveY=random.randint(600,820)
        self.lifetime=pico2d.get_time()
        self.moveBit=-1
        self.shoot_time=0
        self.shoot_angle=0
        self.angle_rate=0.02
        self.event_que = []
        self.cur_state = MoveState
        self.cur_state.enter(self)
        self.score=20
    def update(self,P_bullet_list,player,E_bullet_list):

        self.frame = (self.frame + FRAMES_PER_ENEMY * ACTION_PER_TIME * game_framework.frame_time) % 3

        i=0
        while i < len(P_bullet_list):
            if math.sqrt((P_bullet_list[i].x-self.x)**2+(P_bullet_list[i].y-self.y)**2)<20:
                self.hp=self.hp-P_bullet_list[i].attack
                del P_bullet_list[i]
            else:
                i=i+1
        if self.hp<0 or (self.moveBit==1 and self.y>890):
            if self.hp<0:
                self.hitSound.play()
            return True
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.change_state(event)

        self.cur_state.update(self,E_bullet_list,player)


    def draw(self):
        self.cur_state.draw(self)
        self.locateImage.draw(self.x, 60)


    def change_state(self,  state):
        self.cur_state.exit(self)
        self.cur_state = state
        self.cur_state.enter(self)



    def add_event(self, event):
        self.event_que.insert(0,event)



class MoveState:
    def enter(Enemy):
        pass
    def exit(Enemy):
        pass

    @staticmethod

    def update(Enemy,E_bullet_list,player):
        Enemy.y = Enemy.y +Enemy.moveBit*RUN_SPEED_PPS*game_framework.frame_time

        if Enemy.y <= Enemy.arriveY:
            Enemy.add_event(IdleState)

    @staticmethod
    def draw(Enemy):
        Enemy.image.clip_draw(int(Enemy.frame)  * 70, Enemy.type * 80, 70, 80, Enemy.x, Enemy.y)

    pass


class IdleState:
    def enter(Enemy):
        Enemy.shoot_time = pico2d.get_time()

    def exit(Enemy):
        pass

    @staticmethod
    def update(Enemy,E_bullet_list,player):
        if pico2d.get_time()-Enemy.shoot_time>=0.2 :
            Enemy.add_event(ShootState)

        if pico2d.get_time()-Enemy.lifetime>=18:
            Enemy.moveBit=1
            Enemy.add_event(MoveState)
    def draw(Enemy):
        Enemy.image.clip_draw(int(Enemy.frame)  * 70, Enemy.type * 80, 70, 80, Enemy.x, Enemy.y)


class ShootState:
    def enter(Enemy):
        pass
    def exit(Enemy):
        pass

    @staticmethod
    def update(Enemy,E_bullet_list,player):
      #타입 1 총알생성
        if Enemy.pattern==1:
            E_bullet_list.append(Enemy_bullet(Enemy.x, Enemy.y, Enemy.shoot_angle, 0, 2, 0))
        elif Enemy.pattern==2:
            E_bullet_list.append(Enemy_bullet(Enemy.x, Enemy.y, Enemy.shoot_angle, 0, 2, 0))
            E_bullet_list.append(Enemy_bullet(Enemy.x, Enemy.y, Enemy.shoot_angle+0.5, 0, 2, 0))
            E_bullet_list.append(Enemy_bullet(Enemy.x, Enemy.y, Enemy.shoot_angle+0.25, 0, 2, 0))
            E_bullet_list.append(Enemy_bullet(Enemy.x, Enemy.y, Enemy.shoot_angle+0.75, 0, 2, 0))

        Enemy.shoot_angle = (Enemy.shoot_angle + Enemy.angle_rate) % 360
        Enemy.add_event(IdleState)

    @staticmethod
    def draw(Enemy):
        Enemy.image.clip_draw(int(Enemy.frame)  * 70, Enemy.type * 80, 70, 80, Enemy.x, Enemy.y)