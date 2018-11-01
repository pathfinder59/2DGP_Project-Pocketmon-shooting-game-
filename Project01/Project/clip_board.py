import random
import json
import os

from pico2d import *
import math
#import pause_state
from character import Character
import game_framework
#from bullet import Bullet

class Enemy(Character):
    def __init__(self, x, y,Hp):
        super().__init__(x, y,Hp)
        Enemy.image=load_image('trainner.png')
        self.type=random.randint(0,4)
        self.frame=random.randint(0,4)
        self.arriveY=random.randint(600,820)
        self.time=0
    def update(self,P_bullet_list,player):
        self.time=(self.time+1)%10
        if self.y > self.arriveY:
            self.y=self.y-2
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



    def draw(self):
        Enemy.image.clip_draw(self.frame*51,self.type*60,51,60,self.x,self.y)
        pass