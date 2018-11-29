import random
import json
import os

from pico2d import *
import math
#import pause_state
import game_framework
import start_state
import over_state


class Character:
    def __init__(self,x,y,Hp):
        self.x = x
        self.y = y
        self.hp=Hp
        Character.image=load_image('./Character/trainner.png')
        Character.hitSound=load_wav('./Character/hitSound.wav')
        Character.hitSound.set_volume(50)
        Character.locateImage=load_image('./Character/enemyLocate.png')