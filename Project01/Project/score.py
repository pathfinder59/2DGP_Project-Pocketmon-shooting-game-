import random
import json
import os

from pico2d import *
import math
#import pause_state
import game_framework


class Score:
    def __init__(self):
        self.current_score=0
        self.count=pico2d.get_time()
        Score.image=load_image('./Score/Number.png')
    def update(self):
        if pico2d.get_time()-self.count>0.1:
            self.count=pico2d.get_time()
            self.current_score=self.current_score+1
    def draw(self,x,y):
        Game_score = self.current_score
        i = 0

        while Game_score != 0:
            j = Game_score % 10
            Score.image.clip_draw(j * 32, 0, 32, 60, x - (32 * i), y)
            i = i + 1
            Game_score = Game_score // 10
