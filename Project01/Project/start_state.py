import game_framework
from pico2d import *
import play_state
#import drill06
GAME_HEIGHT= 875
GAME_WIDTH= 590

name = "StartState"

Character1 = None
Character2 = None
Character3 = None
character = None
cursurX=GAME_WIDTH/2
cursurY=50
fileLink='C:\\Users\\jack\Documents\\GitHub\\2DGP_Project\\Project01\\Project\\'

def enter():
    global back_groundImage,Character1,Character2,Character3
    back_groundImage = load_image(fileLink+'Screen\\gamestart.png')
    Character1 = load_image(fileLink+'SelectImage\\CHAR1.png')
    Character2 = load_image(fileLink+'SelectImage\\CHAR2.png')
    Character3 = load_image(fileLink+'SelectImage\\CHAR3.png')
    pass


def exit():
    global back_groundImage,Character1,Character2,Character3
    del (Character1)
    del (Character2)
    del (Character3)
    del (back_groundImage)
    pass

def pause():
    pass
def handle_events():
    global cursurY,cursurX,character

    events=get_events()
    for event in events:
        if event.type==SDL_MOUSEBUTTONDOWN and event.button==SDL_BUTTON_LEFT:
            if c1!= 0:
                character=0
                game_framework.push_state(play_state)
            elif c2!=0:
                character=2
                game_framework.push_state(play_state)
            elif c3!=0:
                character=1
                game_framework.push_state(play_state)

        elif event.type==SDL_MOUSEMOTION:
            cursurY=875-event.y
            cursurX=event.x
        elif event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type ==SDLK_ESCAPE:
            game_framework.quit()

def update():
    global character
    global cursurY, cursurX, image,c1,c2,c3
    c1 = 0
    c2 = 0
    c3 = 0
    if cursurX >= 65 and cursurX <= 65 + 75 + 75 and cursurY >= 357 - 75 - 75 and cursurY <= 357:
        c1 = 2
    elif cursurX >= 160 + 65 and cursurX <= 160 + 65 + 75 + 75 and cursurY >= 357 - 75 - 75 and cursurY <= 357:
        c2 = 2
    elif cursurX >= 320 + 65 and cursurX <= 320 + 65 + 75 + 75 and cursurY >= 357 - 75 - 75 and cursurY <= 357:
        c3 = 2
    pass


def draw():
    global Character1, Character2, Character3,back_groundImage,c1,c2,c3
#595 889
    clear_canvas()
    back_groundImage.draw(GAME_WIDTH / 2, GAME_HEIGHT / 2)
    Character1.draw(65 + 75, 357 - 75, 150 + (c1 * 20), 150 + (c1 * 20))
    Character2.draw(65 + 75 + 150 + 10, 357 - 75, 150 + (c2 * 20), 150 + (c2 * 20))
    Character3.draw(65 + 75 + 300 + 20, 357 - 75, 150 + (c3 * 20), 150 + (c3 * 20))
    update_canvas()
    pass
