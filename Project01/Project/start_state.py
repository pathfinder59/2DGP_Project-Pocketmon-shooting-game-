import game_framework


from pico2d import *
import play_state
from score import Score

GAME_HEIGHT= 875
GAME_WIDTH= 590

name = "StartState"

Character1 = None
Character2 = None
Character3 = None
character = None
background = None
pointer=None
cursurX=GAME_WIDTH/2
cursurY=50
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
        self.x=0
        self.y=0
        pass
def enter():
    global pointer,Character1,Character2,Character3,background
    global bestScore
    pointer=Pointer()
    background=BackGround()
    Character1 = load_image(fileLink+'SelectImage\\CHAR1.png')
    Character2 = load_image(fileLink+'SelectImage\\CHAR2.png')
    Character3 = load_image(fileLink+'SelectImage\\CHAR3.png')
    bestScore = Score()
    pass
def turn_on_music():
    background.bgm.repeat_play()
    pass

def exit():
    global Character1,Character2,Character3,background
    background.exit()
    del (Character1)
    del (Character2)
    del (Character3)
    del(background)


def pause():
    background.exit()
    pass
def handle_events():
    global cursurY,cursurX,character,pointer

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
        elif event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type ==SDLK_ESCAPE:
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
    global Character1, Character2, Character3,back_groundImage,turtleButton,grassButton,lizardButton
#595 889
    clear_canvas()
    background.draw()
    Character1.draw(65 + 75, 357 - 75, 150 + (turtleButton * 40), 150 + (turtleButton * 40))
    Character2.draw(65 + 75 + 75*2 + 10, 357 - 75, 150 + (grassButton * 40), 150 + (grassButton * 40))
    Character3.draw(65 + 75 + 75*4 + 20, 357 - 75, 150 + (lizardButton * 40), 150 + (lizardButton * 40))
    update_canvas()
    pass
