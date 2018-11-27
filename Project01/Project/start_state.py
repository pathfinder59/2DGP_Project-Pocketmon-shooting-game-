import game_framework


from pico2d import *
import play_state
from score import Score
import pickle

GAME_HEIGHT= 875
GAME_WIDTH= 590

name = "StartState"

turtleImage = None
grassImage = None
lizardImage = None
bestScore=None

character = None
background = None
pointer=None

fileLink='C:\\Users\\jack\Documents\\GitHub\\2DGP_Project\\Project01\\Project\\'


class BackGround:
    def __init__(self):
        BackGround.Image = load_image(fileLink + 'Screen\\gamestart.png')
        BackGround.bgm=load_music(fileLink+'Screen\\startMusic.mp3')
        BackGround.bgm.set_volume(40)
        BackGround.bgm.repeat_play()
    def update(self):
        pass
    def draw(self):
        BackGround.Image.draw(GAME_WIDTH / 2, GAME_HEIGHT / 2)
        pass
    def exit(self):
        BackGround.bgm.stop()
class Pointer:
    def __init__(self):
        self.x=GAME_WIDTH/2
        self.y=50
        pass
def enter():
    global pointer,turtleImage,grassImage,lizardImage,background
    global bestScore
    pointer=Pointer()
    background=BackGround()
    turtleImage = load_image(fileLink+'SelectImage\\CHAR1.png')
    grassImage = load_image(fileLink+'SelectImage\\CHAR2.png')
    lizardImage = load_image(fileLink+'SelectImage\\CHAR3.png')
    bestScore = Score()
    load()
    pass
def turn_on_music():
    background.bgm.repeat_play()
    pass

def exit():
    global turtleImage,grassImage,lizardImage,background,pointer
    background.exit()
    del (turtleImage)
    del (grassImage)
    del (lizardImage)
    del(background)
    del(pointer)

def save():
    with open('score.sav', 'wb') as f:
        pickle.dump(bestScore, f)
def load():
    global bestScore
    with open('score.sav', 'rb') as f:
        bestScore = pickle.load(f)
def pause():

    background.exit()
    pass
def handle_events():
    global character,pointer

    events=get_events()
    for event in events:
        if event.type==SDL_MOUSEBUTTONDOWN and event.button==SDL_BUTTON_LEFT:
            if turtleButton:
                character=0
                game_framework.push_state(play_state)
            elif grassButton:
                character=2
                game_framework.push_state(play_state)
            elif lizardButton:
                character=1
                game_framework.push_state(play_state)

        elif event.type==SDL_MOUSEMOTION:
            pointer.y=875-event.y
            pointer.x=event.x
        elif event.type == SDL_KEYDOWN and event.key==SDLK_ESCAPE:
            save()
            game_framework.quit()

def update():
    global character
    global turtleButton,grassButton,lizardButton
    turtleButton = False
    grassButton = False
    lizardButton = False
    if pointer.x >= 65 and pointer.x <= 65 + 75 + 75 and pointer.y >= 357 - 75 - 75 and pointer.y <= 357:
        turtleButton = True
    elif pointer.x >= 160 + 65 and pointer.x <= 160 + 65 + 75 + 75 and pointer.y >= 357 - 75 - 75 and pointer.y <= 357:
        grassButton = True
    elif pointer.x >= 320 + 65 and pointer.x <= 320 + 65 + 75 + 75 and pointer.y >= 357 - 75 - 75 and pointer.y <= 357:
        lizardButton = True
    pass


def draw():
#595 889
    clear_canvas()
    background.draw()
    turtleImage.draw(65 + 75, 357 - 75, 150 + (turtleButton * 40), 150 + (turtleButton * 40))
    grassImage.draw(65 + 75 + 75*2 + 10, 357 - 75, 150 + (grassButton * 40), 150 + (grassButton * 40))
    lizardImage.draw(65 + 75 + 75*4 + 20, 357 - 75, 150 + (lizardButton * 40), 150 + (lizardButton * 40))
    update_canvas()
    pass
