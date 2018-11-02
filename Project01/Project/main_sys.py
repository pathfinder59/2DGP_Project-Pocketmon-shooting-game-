import game_framework
import pico2d
import start_state
GAME_HEIGHT = 875
GAME_WIDTH = 590
pico2d.open_canvas(GAME_WIDTH,GAME_HEIGHT)
game_framework.run(start_state)
pico2d.close_canvas()