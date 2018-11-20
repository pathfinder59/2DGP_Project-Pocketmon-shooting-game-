import random
import math
import game_framework
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
from pico2d import *
import play_state

# zombie Run Speed

animation_names = ['Attack', 'Dead', 'Idle', 'Walk']


class Administrator:
    images = None

    def __init__(self):


    def wander(self):
        self.speed = RUN_SPEED_PPS
        self.timer -= game_framework.frame_time
        if self.timer < 0:
            self.timer += 1.0
        self.dir = random.random() * 2 * math.pi
        return BehaviorTree.SUCCESS

    def find_player(self):
        boy = main_state.get_boy()
        distance = (boy.x - self.x) ** 2 + (boy.y - self.y) ** 2
        if distance < (PIXEL_PER_METER * 10) ** 2:
            self.dir = math.atan2(boy.y - self.y, boy.x - self.x)
            return BehaviorTree.SUCCESS
        else:
            self.speed = 0
            return BehaviorTree.FAIL

    def move_to_player(self):
        self.speed = RUN_SPEED_PPS
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        find_player_node = LeafNode("Find Player", self.find_player)
        move_to_player_node = LeafNode("Move to Player", self.move_to_player)
        chase_node = SequenceNode("Chase")
        chase_node.add_children(find_player_node, move_to_player_node)
        self.bt = BehaviorTree(chase_node)


    def update(self):
        self.bt.run()
        pass
