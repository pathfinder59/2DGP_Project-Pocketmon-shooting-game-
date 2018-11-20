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
class IdleState:
    def enter(player,event):
        player.timer=1000

    def exit(player,event):
        pass
    def update(player):
        #player.frame=(player.frame+1)%8
        pass

    def draw(player):
        if player.hitSwitch:
            player.image.opacify(random.random())
            if pico2d.get_time()-player.hitcount>=3:
                player.image.opacify(1)
                player.hitSwitch=False
        player.image.clip_draw(int(player.frame) * 40, 40 * player.Type, 40, 40, player.x, player.y)
        if player.skillSwitch:
            Player.skill_image.clip_draw(int(player.skillframe)*50,50*player.Type,50,50,player.x,player.y)
            pass
# fill here
class RunState:
    def enter(player,event):
        if event == RIGHT_DOWN:
            player.velocityX += player.speed
        elif event == RIGHT_UP:
            player.velocityX -= player.speed
        if event == LEFT_DOWN:
            player.velocityX -= player.speed
        elif event == LEFT_UP:
            player.velocityX += player.speed
        if event == TOP_DOWN:
            player.velocityY += player.speed
        elif event == TOP_UP:
            player.velocityY -= player.speed
        if event == UNDER_DOWN:
            player.velocityY -= player.speed
        elif event == UNDER_UP:
            player.velocityY += player.speed

        if event == SHIFT_DOWN:
            if player.velocityX > 0:
                player.velocityX -= SLOW_SPEED_PPS
            elif player.velocityX < 0:
                player.velocityX += SLOW_SPEED_PPS
            if player.velocityY > 0:
                player.velocityY -= SLOW_SPEED_PPS
            elif player.velocityY < 0:
                player.velocityY += SLOW_SPEED_PPS
            player.speed = RUN_SPEED_PPS-SLOW_SPEED_PPS
            pass
        elif event == SHIFT_UP:
            if player.velocityX > 0:
                player.velocityX += SLOW_SPEED_PPS
            elif player.velocityX < 0:
                player.velocityX -= SLOW_SPEED_PPS
            if player.velocityY > 0:
                player.velocityY += SLOW_SPEED_PPS
            elif player.velocityY < 0:
                player.velocityY -= SLOW_SPEED_PPS
                player.speed = RUN_SPEED_PPS
            pass

        player.dir=player.velocityX

    def exit(player,event):
        pass
    def update(player):
        player.x+=player.velocityX*game_framework.frame_time
        player.x=clamp(25,player.x,590-25)
        player.y += player.velocityY*game_framework.frame_time
        player.y = clamp(25, player.y, 875 - 25)

    def draw(player):
        if player.hitSwitch:
            player.image.opacify(random.random())
            if pico2d.get_time()-player.hitcount>=3:
                player.image.opacify(1)
                player.hitSwitch=False

        player.image.clip_draw(int(player.frame) * 40, 40 * player.Type, 40, 40, player.x, player.y)
        if player.skillSwitch:
            Player.skill_image.clip_draw(int(player.skillframe)*50,50*player.Type,50,50,player.x,player.y)
            pass


next_state_table = {
    RunState:{RIGHT_UP:RunState,LEFT_UP:RunState,LEFT_DOWN:RunState,RIGHT_DOWN:RunState,
              TOP_UP: RunState, UNDER_UP: RunState, TOP_DOWN: RunState, UNDER_DOWN: RunState,
              SHIFT_DOWN: RunState, SHIFT_UP: RunState}
# fill here
}




class Player(Character):
    def __init__(self,x,y,Hp,type):
        super().__init__(x,y,Hp)
        self.Type=type
        self.attack=1
        self.count=pico2d.get_time()
        self.frame=0

        self.skilltime=None
        self.skillframe=0
        self.skillCooltime=pico2d.get_time()-25
        self.speed=RUN_SPEED_PPS
        self.skillSwitch=False
        self.hitSwitch=False
        self.hitcount=0
        Player.image = load_image(fileLink+'Character\\player1.png')
        Player.skill_image=load_image(fileLink+'Skill\\skill.png')
        self.dir = 1
        self.velocityX = 0
        self.velocityY = 0
        # fill here
        self.event_que = []
        self.cur_state = RunState
        self.cur_state.enter(self,None)

        self.sCount=0

    def update(self,P_bullet_list,E_bullet_list):
        self.frame = (self.frame + FRAMES_PER_PLAYER*ACTION_PER_TIME*game_framework.frame_time) % 9

        if self.skillSwitch:

            self.skillframe=(self.skillframe+ FRAMES_PER_SKILL*ACTION_PER_TIME*game_framework.frame_time)%10
            if pico2d.get_time()-self.skilltime>=5:
                self.skillSwitch = False
                self.attack = 1

        for i in E_bullet_list:
            if math.sqrt((i.x - self.x) ** 2 + (i.y - self.y) ** 2) < 9:
                if self.Type==0:
                    if self.skillSwitch:
                        pass
                    else:
                        if self.hitSwitch==False:
                            self.hp=self.hp-1
                            self.hitcount=pico2d.get_time()
                            self.hitSwitch=True
                            E_bullet_list.remove(i)
                            del i
                else:
                    if self.hitSwitch == False:
                        self.hp = self.hp - 1
                        self.hitcount = pico2d.get_time()
                        self.hitSwitch = True
                        E_bullet_list.remove(i)
                        del i
                if self.hp==0:   #게임오버 실행
                    return False
                    pass
        if pico2d.get_time()-self.count>=0.15 :  #일종의 타이머로 총알 생성
            P_bullet_list.append(Player_bullet(self.x, self.y))
            self.count=get_time()
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
        if pico2d.get_time()-self.skillCooltime>=25:
            self.skillSwitch=True
            self.skilltime=pico2d.get_time()

            self.skillCooltime=pico2d.get_time()
            self.sCount=-1
            if self.Type== 2 : ##이상해씨
                self.hp=self.hp+1
                pass
            elif self.Type==1: ##파이리
                self.attack=4
                pass
            elif self.Type==0: ##꼬부기
                pass

    #def change_state(self,  state):
     #   self.cur_state.exit(self,key_event)
        #if state==IdleState:
            #if len(move_list) > 0:
             #   del move_list[0]
            #if len(move_list)>0:
            #    pass
            #else:
#                self.cur_state=state

 #       if state == RunState:
  #          move_list.append(state)
      #  self.cur_state = state
       # self.cur_state.enter(self,event)
        pass


    def add_event(self, event):
        self.event_que.insert(0,event)
        pass

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
        pass