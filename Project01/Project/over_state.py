import game_framework
from pico2d import *
import start_state
import play_state
from score import Score

name = "OverState"
image = None

GAME_HEIGHT = 875
GAME_WIDTH = 590


def enter():
    global image
    image = load_image('GAMEOVER.png')
    pass

def pause():
    pass

def exit():
    global image
    del (image)
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            game_framework.reset(start_state)
        elif event.type == SDL_KEYDOWN:
            game_framework.reset(start_state)


def update():
    pass

def draw():
    global image
    clear_canvas()
    image.draw(590/2, 875/2)
    play_state.score.draw(400,30)
    update_canvas()
    pass
