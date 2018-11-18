import random
import json
import os

from pico2d import *
import math
#import pause_state
import game_framework
import start_state





GAME_HEIGHT = 875
GAME_WIDTH = 590
pauseImage=None
name = "PauseState"

fileLink='C:\\Users\\jack\Documents\\GitHub\\2DGP_Project\\Project01\\Project\\'
def pause():
    pass

def enter():
    global pauseImage,pauseTime
    pauseImage=load_image(fileLink+'Screen\\pause.png')
    pauseTime = pico2d.get_time()
    pass


def exit():
    global pauseImage
    del(pauseImage)
    pass

def pause():
    pass



def resume():
    pass


def handle_events():

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type==SDL_KEYDOWN and event.key==SDLK_p:
            game_framework.pop_state()


def update():
    pass

def draw():
    pauseImage.draw(GAME_WIDTH/2,GAME_HEIGHT/2)
    update_canvas()






