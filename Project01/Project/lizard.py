import random
import json
import os
import game_framework
from pico2d import *
import math
#import pause_state


from gameBullet import Player_bullet
from character import Character
import play_state

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
    def enter(Lizard,event):
        if event == RIGHT_DOWN:
            Lizard.velocityX += Lizard.speed
        elif event == RIGHT_UP:
            Lizard.velocityX -= Lizard.speed
        if event == LEFT_DOWN:
            Lizard.velocityX -= Lizard.speed
        elif event == LEFT_UP:
            Lizard.velocityX += Lizard.speed
        if event == TOP_DOWN:
            Lizard.velocityY += Lizard.speed
        elif event == TOP_UP:
            Lizard.velocityY -= Lizard.speed
        if event == UNDER_DOWN:
            Lizard.velocityY -= Lizard.speed
        elif event == UNDER_UP:
            Lizard.velocityY += Lizard.speed

        if event == SHIFT_DOWN:
            if Lizard.velocityX > 0:
                Lizard.velocityX -= SLOW_SPEED_PPS
            elif Lizard.velocityX < 0:
                Lizard.velocityX += SLOW_SPEED_PPS
            if Lizard.velocityY > 0:
                Lizard.velocityY -= SLOW_SPEED_PPS
            elif Lizard.velocityY < 0:
                Lizard.velocityY += SLOW_SPEED_PPS
            Lizard.speed = RUN_SPEED_PPS-SLOW_SPEED_PPS

        elif event == SHIFT_UP:
            if Lizard.velocityX > 0:
                Lizard.velocityX += SLOW_SPEED_PPS
            elif Lizard.velocityX < 0:
                Lizard.velocityX -= SLOW_SPEED_PPS
            if Lizard.velocityY > 0:
                Lizard.velocityY += SLOW_SPEED_PPS
            elif Lizard.velocityY < 0:
                Lizard.velocityY -= SLOW_SPEED_PPS
            Lizard.speed = RUN_SPEED_PPS


        Lizard.dir=Lizard.velocityX

    def exit(Lizard,event):
        pass

    def update(Lizard):
        P_bullet_list=play_state.get_pBulletList()

        Lizard.x += Lizard.velocityX * game_framework.frame_time
        Lizard.x = clamp(25, Lizard.x, 590 - 25)
        Lizard.y += Lizard.velocityY * game_framework.frame_time
        Lizard.y = clamp(25, Lizard.y, 875 - 25)

        if Lizard.skillSwitch:

            Lizard.skillframe=(Lizard.skillframe+ FRAMES_PER_SKILL*ACTION_PER_TIME*game_framework.frame_time)%10
            if pico2d.get_time()-Lizard.skilltime>=5:
                Lizard.skillSwitch = False
                Lizard.attack = 1

        Lizard.check_collision()

        if pico2d.get_time()-Lizard.shoottime>=0.15 :  #일종의 타이머로 총알 생성
            P_bullet_list.append(Player_bullet(Lizard.x, Lizard.y,Lizard.attack))
            Lizard.shoottime=get_time()


    def draw(Lizard):
        if Lizard.hitSwitch:
            Lizard.image.opacify(random.random())
            if pico2d.get_time()-Lizard.hitcount>=3:
                Lizard.image.opacify(1)
                Lizard.hitSwitch=False
        if pico2d.get_time() - Lizard.skillCooltime >=18 :
            Lizard.skill_icon.draw(20, 150)
        Lizard.image.clip_draw(int(Lizard.frame) * 40, 40 * 1, 40, 40, Lizard.x, Lizard.y)
        if Lizard.skillSwitch:
            Lizard.skill_image.clip_draw(int(Lizard.skillframe)*50,50*1,50,50,Lizard.x,Lizard.y)



next_state_table = {
    RunState:{RIGHT_UP:RunState,LEFT_UP:RunState,LEFT_DOWN:RunState,RIGHT_DOWN:RunState,
              TOP_UP: RunState, UNDER_UP: RunState, TOP_DOWN: RunState, UNDER_DOWN: RunState,
              SHIFT_DOWN: RunState, SHIFT_UP: RunState}
# fill here
}




class Lizard(Character):
    def __init__(self,x,y,Hp):
        super().__init__(x,y,Hp)
        self.Type=1
        self.attack=1
        self.shoottime=pico2d.get_time()
        self.frame=0

        self.skilltime=None
        self.skillframe=0
        self.skillCooltime=pico2d.get_time()-25
        self.speed=RUN_SPEED_PPS
        self.skillSwitch=False
        self.hitSwitch=False
        self.hitcount=0
        Lizard.image = load_image('./Character/player1.png')
        Lizard.skill_image=load_image('./Skill/skill.png')
        Lizard.skill_icon=load_image('./Skill/attackSkill.png')

        Lizard.bgm = load_wav('./Skill/attack.wav')
        Lizard.bgm.set_volume(70)


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
                if self.hitSwitch == False:
                    self.hitSound.play()
                    self.hp = self.hp - 1
                    self.hitcount = pico2d.get_time()
                    self.hitSwitch = True
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


        ##적총알 플레이어 타격시 타입이 거북이&스킬중이면 피격x
    def skill(self):
        if pico2d.get_time()-self.skillCooltime>=18:
            self.skillSwitch=True
            Lizard.bgm.play()
            self.skilltime=pico2d.get_time()
            self.skillCooltime=pico2d.get_time()

            self.attack=4






    def add_event(self, event):
        self.event_que.insert(0,event)


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
