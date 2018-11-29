import random
import math
import game_framework
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
from pico2d import *

import play_state



class Administrator:
    images = None

    def __init__(self):
        self.build_behavior_tree()

    def adjust_EnemyShootAngle(self):
        enemyList = play_state.get_EnemyList()
        player = play_state.get_Player()
        for i in enemyList:
            if i.type==0 or i.type==2:
                i.shoot_angle=-math.atan2(player.y - i.y, player.x - i.x) / 3.1415 / 2
        return BehaviorTree.SUCCESS

    def count_nEnemy(self):
        enemyList = play_state.get_EnemyList()
        if len(enemyList)<=(4*play_state.count):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL


    def generate_Enemy(self):
        pBulletList = play_state.get_pBulletList()
        enemyList = play_state.get_EnemyList()
        nLeftBullet=0
        nRightBullet=0
        for i in pBulletList:
            if i.x<=get_canvas_width()//2:
                nLeftBullet+=1
            else:
                nRightBullet+=1
        for i in range(play_state.count):
            if nLeftBullet<nRightBullet:
                enemyList.append(play_state.Enemy_table[random.randint(0, 3)](random.randint(20,get_canvas_width()//2 ),
                                                                          get_canvas_height() + 15))
            else:
                enemyList.append(play_state.Enemy_table[random.randint(0, 3)](random.randint(get_canvas_width() // 2,get_canvas_width()-20),
                                                                          get_canvas_height() + 15))
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        generateEnemy_node= LeafNode("Generate",self.generate_Enemy)
        countEnemy_node=LeafNode("Count",self.count_nEnemy)
        adjustEnemy_node=LeafNode("Adjust",self.adjust_EnemyShootAngle)
        makeEnemy_node=SequenceNode("Make")
        makeEnemy_node.add_children(countEnemy_node,generateEnemy_node)
        make_adjust_node=SelectorNode("MakeAdjust")
        make_adjust_node.add_children(makeEnemy_node,adjustEnemy_node)
        self.bt=BehaviorTree(make_adjust_node)




    def update(self):
        self.bt.run()

