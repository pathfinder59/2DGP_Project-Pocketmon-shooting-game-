import random
import json
import os

from pico2d import *
import math
#import pause_state
import game_framework

TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_LIFE = 3
fileLink='C:\\Users\\jack\Documents\\GitHub\\2DGP_Project\\Project01\\Project\\'
class Life:
    def __init__(self):
        self.lFrame=0
        Life.image=load_image(fileLink+'Life\\Life.png')
    def update(self):
        self.lFrame=(self.lFrame + FRAMES_PER_LIFE*ACTION_PER_TIME*game_framework.frame_time) % 10
    def draw(self,player):

        for i in range(player.hp):
            Life.image.clip_draw(int(self.lFrame) * 35, 0, 35, 35, 15 + i * 35, 100)
    pass
