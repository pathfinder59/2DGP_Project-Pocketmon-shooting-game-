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

class Enemy(Character):
    def __init__(self, x, y,Hp):
        super().__init__(x, y,Hp)
        Enemy.image=load_image('trainner.png')
        self.type=random.randint(0,1)
        self.pattern=random.randint(1,2)
        self.frame=random.randint(0,4)
        self.arriveY=random.randint(600,820)
        self.time=0
        self.shoot_time=0
        self.shoot_angle=0
        if self.type==1:
            self.angle_rate=0.02
        else :
            self.angle_rate=0
        if self.type==0:
            self.clock=30
        elif self.type==1:
            self.clock=10
        self.event_que = []
        self.cur_state = MoveState
        self.cur_state.enter(self)

    def update(self,P_bullet_list,player,E_bullet_list):
        self.time=(self.time+1)%10
        if self.time%10==0:
            self.frame=(self.frame+1)%3
        i=0
        while i < len(P_bullet_list):
            if math.sqrt((P_bullet_list[i].x-self.x)**2+(P_bullet_list[i].y-self.y)**2)<15 :
                self.hp=self.hp-player.attack
                del P_bullet_list[i]
            else:
                i=i+1
        if self.hp<0:
            return True
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.change_state(event)

        self.cur_state.update(self,E_bullet_list)


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

    def update(Enemy,E_bullet_list):
        Enemy.y = Enemy.y - 2

        if Enemy.y <= Enemy.arriveY:
            Enemy.add_event(IdleState)

    @staticmethod
    def draw(Enemy):
        Enemy.image.clip_draw(Enemy.frame * 100, Enemy.type * 116, 100, 116, Enemy.x, Enemy.y)

    pass


class IdleState:
    def enter(Enemy):
        pass
    def exit(Enemy):
        pass

    @staticmethod
    def update(Enemy,E_bullet_list):
        Enemy.shoot_time=(Enemy.shoot_time+1)%30
        if Enemy.shoot_time%Enemy.clock==0 :
            Enemy.add_event(ShootState)
            pass
    @staticmethod
    def draw(Enemy):
        Enemy.image.clip_draw(Enemy.frame * 100, Enemy.type * 116, 100, 116, Enemy.x, Enemy.y)


class ShootState:
    def enter(Enemy):
        pass
    def exit(Enemy):
        pass

    @staticmethod
    def update(Enemy,E_bullet_list):
      #총알 생성
      if Enemy.type==0:      ##타입 0 총알생성
          if Enemy.pattern==1:
              E_bullet_list.append(E_bullet(Enemy.x,Enemy.y,0.25,0,2,0))
              pass
          elif Enemy.pattern==2:
              E_bullet_list.append(E_bullet(Enemy.x, Enemy.y, 0.25, 0, 2, 0))
              E_bullet_list.append(E_bullet(Enemy.x, Enemy.y, 0.125, 0, 2, 0))
              E_bullet_list.append(E_bullet(Enemy.x, Enemy.y, 0.375, 0, 2, 0))
              pass
          pass

      elif Enemy.type==1:    ##타입 1 총알생성
          if Enemy.pattern==1:
              E_bullet_list.append(E_bullet(Enemy.x, Enemy.y, Enemy.shoot_angle, 0, 2, 0))
              pass
          elif Enemy.pattern==2:
              E_bullet_list.append(E_bullet(Enemy.x, Enemy.y, Enemy.shoot_angle, 0, 2, 0))
              E_bullet_list.append(E_bullet(Enemy.x, Enemy.y, Enemy.shoot_angle+0.5, 0, 2, 0))
              E_bullet_list.append(E_bullet(Enemy.x, Enemy.y, Enemy.shoot_angle+0.25, 0, 2, 0))
              E_bullet_list.append(E_bullet(Enemy.x, Enemy.y, Enemy.shoot_angle+0.75, 0, 2, 0))
              pass
          Enemy.shoot_angle = (Enemy.shoot_angle + Enemy.angle_rate)%360
          pass

      elif Enemy.type==2:    ##타입 2 총알생성
          if Enemy.pattern==1:
              pass
          elif Enemy.pattern==2:
              pass
          pass

      elif Enemy.type==3:    ##타입 3 총알생성
          if Enemy.pattern==1:
              pass
          elif Enemy.pattern==2:
              pass
          pass

      elif Enemy.type==4:    ##타입 4 총알생성
          if Enemy.pattern==1:
              pass
          elif Enemy.pattern==2:
              pass
          pass
      Enemy.add_event(IdleState)

    @staticmethod
    def draw(Enemy):
        Enemy.image.clip_draw(Enemy.frame * 100, Enemy.type * 116, 100, 116, Enemy.x, Enemy.y)