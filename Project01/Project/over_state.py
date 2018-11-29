import game_framework
from pico2d import *
import start_state
import play_state
from score import Score

name = "OverState"
background = None
bestScoreImage=None
currentScoreImage=None
fileLink='C:\\Users\\jack\Documents\\GitHub\\2DGP_Project\\Project01\\Project\\'
GAME_HEIGHT = 875
GAME_WIDTH = 590

class BackGround:
    def __init__(self):
        BackGround.Image = load_image(fileLink + 'Screen\\GAMEOVER.png')
        BackGround.bgm=load_music(fileLink+'Screen\\overMusic.mp3')
        BackGround.bgm.set_volume(20)
        BackGround.bgm.repeat_play()
        BackGround.bestBgm=load_wav(fileLink + 'Screen\\bestScore.wav')

        BackGround.bestBgm.set_volume(60)
        if play_state.score_renew:
            play_state.score_renew=False
            BackGround.bestBgm.play()
    def update(self):
        pass
    def draw(self):
        BackGround.Image.draw(GAME_WIDTH / 2, GAME_HEIGHT / 2)

    def exit(self):
        BackGround.bgm.stop()
        BackGround.bestBgm.set_volume(0)

def enter():
    global background,currentScoreImage,bestScoreImage
    background=BackGround()
    bestScoreImage = load_image(fileLink + 'Screen\\bestscore.png')
    currentScoreImage = load_image(fileLink + 'Screen\\currentscore.png')


def pause():
    pass
def turn_on_music():
    background.bgm.repeat_play()

def exit():
    global background,currentScoreImage,bestScoreImage
    background.exit()
    del(background)
    del (currentScoreImage)
    del (bestScoreImage)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type==SDL_KEYDOWN and event.key==SDLK_ESCAPE:
            game_framework.returnState(start_state)
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            game_framework.returnState(start_state)


def update():
    pass

def draw():
    clear_canvas()
    background.draw()
    bestScoreImage.draw(100, 140)
    currentScoreImage.draw(100, 40)
    start_state.bestScore.draw(450,130)
    play_state.score.draw(450,30)
    update_canvas()

