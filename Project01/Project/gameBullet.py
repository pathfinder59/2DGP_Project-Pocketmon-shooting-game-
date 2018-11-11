import random
import json
import os

from pico2d import *
import math
#import pause_state
import game_framework
from bullet import Bullet
PI=3.1452

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 15# Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

SHOT_SPEED_KMPH = 40 # Km / Hour
SHOT_SPEED_MPM = (SHOT_SPEED_KMPH * 1000.0 / 60.0)
SHOT_SPEED_MPS = (SHOT_SPEED_MPM / 60.0)
SHOT_SPEED_PPS = (SHOT_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_BULLET = 8

ROT_SPEED_TPS = 250

fileLink='C:\\Users\\jack\Documents\\GitHub\\2DGP_Project\\Project01\\Project\\'
class Player_bullet(Bullet):
    def __init__(self,x,y):
        super().__init__(x,y)
        Player_bullet.image=load_image(fileLink+'Bullet\\Bullet.png')
    def update(self):
        self.y=self.y+SHOT_SPEED_PPS*game_framework.frame_time
        if self.y > 875:
            return True
        return False
    def draw(self,player):
        Player_bullet.image.clip_draw((2 - player.Type) * 10, 0, 10, 10, self.x, self.y)

##bullet_image=load_image('Bullet.png')

class Enemy_bullet(Bullet):
    def __init__(self,x,y,angle,angle_rate,speed,speed_rate):
        super().__init__(x, y)
        self.angle=angle
        self.angle_rate=angle_rate
        self.speed=speed
        self.speed_rate=speed_rate
        self.frame=0
        Enemy_bullet.image = load_image(fileLink+'Bullet\\Poketball.png') #frame&7 조절 하나당 크기10x10
    def update(self):
        global PI
        self.frame = (self.frame + FRAMES_PER_BULLET*ACTION_PER_TIME*game_framework.frame_time) % 8
        self.x=self.x+(self.speed*math.cos(self.angle*PI*2))*game_framework.frame_time*RUN_SPEED_PPS
        self.y=self.y-(self.speed*math.sin(self.angle*PI*2))*game_framework.frame_time*RUN_SPEED_PPS
        self.angle+=self.angle_rate*ROT_SPEED_TPS*game_framework.frame_time
        self.speed+=self.speed_rate

        if self.y > 875 or self.y<0 or self.x>595 or self.x<0:
            return True
        return False

    def draw(self,player):
        self.image.clip_draw(int(self.frame)* 30, 0, 30, 30, self.x, self.y)

#Enemy.y = Enemy.y-3*math.sin(0.125*3.1415*2)
 #       Enemy.x = Enemy.x + 3 *math.cos(0.125 * 3.1415*2)