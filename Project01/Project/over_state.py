import game_framework
from pico2d import *
import start_state
import play_state
from score import Score

name = "OverState"
back_groundImage = None
fileLink='C:\\Users\\jack\Documents\\GitHub\\2DGP_Project\\Project01\\Project\\'
GAME_HEIGHT = 875
GAME_WIDTH = 590


def enter():
    global back_groundImage
    back_groundImage = load_image(fileLink+'Screen\\GAMEOVER.png')
    pass

def pause():
    pass

def exit():
    global back_groundImage
    del (back_groundImage)
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            game_framework.returnState(start_state)
        elif event.type == SDL_KEYDOWN:
            game_framework.returnState(start_state)


def update():
    pass

def draw():
    global back_groundImage
    clear_canvas()
    back_groundImage.draw(590/2, 875/2)
    start_state.bestScore.draw(400,130)
    play_state.score.draw(400,30)
    update_canvas()
    pass
