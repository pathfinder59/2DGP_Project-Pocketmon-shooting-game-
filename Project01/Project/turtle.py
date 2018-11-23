import random
import json
import os
import game_framework
from pico2d import *
import math
#import pause_state

fileLink='C:\\Users\\jack\Documents\\GitHub\\2DGP_Project\\Project01\\Project\\'
from gameBullet import Player_bullet
from character import Character
import play_state
move_list=[]
SKILL_COOLTIME={0:30,1:30,2:25}

RIGHT_DOWN,LEFT_DOWN,TOP_DOWN,UNDER_DOWN,RIGHT_UP,LEFT_UP,TOP_UP,UNDER_UP,SHIFT_DOWN,SHIFT_UP=range(10)
key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_UP): TOP_DOWN,
    (SDL_KEYDOWN, SDLK_DOWN): UNDER_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYUP, SDLK_UP): TOP_UP,
    (SDL_KEYUP, SDLK_DOWN): UNDER_UP,
    (SDL_KEYDOWN, SDLK_LSHIFT): SHIFT_DOWN,
    (SDL_KEYUP, SDLK_LSHIFT): SHIFT_UP
}
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 30 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

SLOW_SPEED_KMPH = 15 # Km / Hour
SLOW_SPEED_MPM = (SLOW_SPEED_KMPH * 1000.0 / 60.0)
SLOW_SPEED_MPS = (SLOW_SPEED_MPM / 60.0)
SLOW_SPEED_PPS = (SLOW_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_PLAYER = 9
FRAMES_PER_SKILL = 10
class RunState:
    def enter(Turtle,event):
        if event == RIGHT_DOWN:
            Turtle.velocityX += Turtle.speed
        elif event == RIGHT_UP:
            Turtle.velocityX -= Turtle.speed
        if event == LEFT_DOWN:
            Turtle.velocityX -= Turtle.speed
        elif event == LEFT_UP:
            Turtle.velocityX += Turtle.speed
        if event == TOP_DOWN:
            Turtle.velocityY += Turtle.speed
        elif event == TOP_UP:
            Turtle.velocityY -= Turtle.speed
        if event == UNDER_DOWN:
            Turtle.velocityY -= Turtle.speed
        elif event == UNDER_UP:
            Turtle.velocityY += Turtle.speed

        if event == SHIFT_DOWN:
            if Turtle.velocityX > 0:
                Turtle.velocityX -= SLOW_SPEED_PPS
            elif Turtle.velocityX < 0:
                Turtle.velocityX += SLOW_SPEED_PPS
            if Turtle.velocityY > 0:
                Turtle.velocityY -= SLOW_SPEED_PPS
            elif Turtle.velocityY < 0:
                Turtle.velocityY += SLOW_SPEED_PPS
            Turtle.speed = RUN_SPEED_PPS-SLOW_SPEED_PPS
            pass
        elif event == SHIFT_UP:
            if Turtle.velocityX > 0:
                Turtle.velocityX += SLOW_SPEED_PPS
            elif Turtle.velocityX < 0:
                Turtle.velocityX -= SLOW_SPEED_PPS
            if Turtle.velocityY > 0:
                Turtle.velocityY += SLOW_SPEED_PPS
            elif Turtle.velocityY < 0:
                Turtle.velocityY -= SLOW_SPEED_PPS
            Turtle.speed = RUN_SPEED_PPS
            pass

        Turtle.dir=Turtle.velocityX

    def exit(Turtle,event):
        pass

    def update(Turtle):
        P_bullet_list=play_state.get_pBulletList()

        Turtle.x += Turtle.velocityX * game_framework.frame_time
        Turtle.x = clamp(25, Turtle.x, 590 - 25)
        Turtle.y += Turtle.velocityY * game_framework.frame_time
        Turtle.y = clamp(25, Turtle.y, 875 - 25)

        if Turtle.skillSwitch:
            Turtle.skillframe=(Turtle.skillframe+ FRAMES_PER_SKILL*ACTION_PER_TIME*game_framework.frame_time)%10
            if pico2d.get_time()-Turtle.skilltime>=5:
                Turtle.skillSwitch = False
        Turtle.check_collision()

        if pico2d.get_time()-Turtle.count>=0.15 :  #일종의 타이머로 총알 생성
            P_bullet_list.append(Player_bullet(Turtle.x, Turtle.y))
            Turtle.count=get_time()


    def draw(Turtle):
        if Turtle.hitSwitch:
            Turtle.image.opacify(random.random())
            if pico2d.get_time()-Turtle.hitcount>=3:
                Turtle.image.opacify(1)
                Turtle.hitSwitch=False

        Turtle.image.clip_draw(int(Turtle.frame) * 40, 0, 40, 40, Turtle.x, Turtle.y)
        if Turtle.skillSwitch:
            Turtle.skill_image.clip_draw(int(Turtle.skillframe)*50,0,50,50,Turtle.x,Turtle.y)
            pass


next_state_table = {
    RunState:{RIGHT_UP:RunState,LEFT_UP:RunState,LEFT_DOWN:RunState,RIGHT_DOWN:RunState,
              TOP_UP: RunState, UNDER_UP: RunState, TOP_DOWN: RunState, UNDER_DOWN: RunState,
              SHIFT_DOWN: RunState, SHIFT_UP: RunState}
# fill here
}




class Turtle(Character):
    def __init__(self,x,y,Hp,type):
        super().__init__(x,y,Hp)
        self.Type=type
        self.attack=1
        self.count=pico2d.get_time()
        self.frame=0

        self.skilltime=None
        self.skillframe=0
        self.skillCooltime=pico2d.get_time()-30
        self.speed=RUN_SPEED_PPS
        self.skillSwitch=False
        self.hitSwitch=False
        self.hitcount=0
        Turtle.image = load_image(fileLink+'Character\\player1.png')
        Turtle.skill_image=load_image(fileLink+'Skill\\skill.png')
        self.dir = 1
        self.velocityX = 0
        self.velocityY = 0
        # fill here
        self.event_que = []
        self.cur_state = RunState
        self.cur_state.enter(self,None)

        self.sCount=0
    def check_collision(self):
        E_bullet_list = play_state.get_eBulletList()
        for i in E_bullet_list:
            if math.sqrt((i.x - self.x) ** 2 + (i.y - self.y) ** 2) < 9:
                if self.skillSwitch:
                     pass
                else:
                    if self.hitSwitch==False:
                        self.hp=self.hp-1
                        self.hitcount=pico2d.get_time()
                        self.hitSwitch=True
                        E_bullet_list.remove(i)
                        del i


    def update(self,P_bullet_list,E_bullet_list):
        if self.hp == 0:  # 게임오버 실행
            return False
        self.frame = (self.frame + FRAMES_PER_PLAYER*ACTION_PER_TIME*game_framework.frame_time) % 9
        self.cur_state.update(self)

        if len(self.event_que)>0:
            event=self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state=next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)
        return True


    def draw(self):
        self.cur_state.draw(self)
        pass

        ##적총알 플레이어 타격시 타입이 거북이&스킬중이면 피격x
    def skill(self):
        if pico2d.get_time()-self.skillCooltime>=30:
            self.skillSwitch=True
            self.skilltime=pico2d.get_time()
            self.skillCooltime=pico2d.get_time()
        pass


    def add_event(self, event):
        self.event_que.insert(0,event)
        pass

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
        pass