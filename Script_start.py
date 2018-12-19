# -*- coding: utf-8 -*-   
from FGO import FGO_Scripts, Fgo_stratege, SKILL, M_SKILL, ORIENT, CHANGE
import argparse
import sys


    # 万华镜狂兰
skills1 = [[SKILL[0],ORIENT[1],SKILL[6],ORIENT[1]],
    [SKILL[2],ORIENT[1],SKILL[5],M_SKILL[0],M_SKILL[2],ORIENT[1]], 
    [SKILL[8],ORIENT[1],SKILL[1],SKILL[7]]
    ]

    # 小莫三回合冲浪
skills2 = [[SKILL[0],ORIENT[1],SKILL[3],SKILL[8],ORIENT[1]],
    [], 
    []
    ]

    # 帽子狂兰
skills3 = [[SKILL[0],ORIENT[1],SKILL[2],ORIENT[1],SKILL[6],ORIENT[1]],
    [SKILL[5],SKILL[8],ORIENT[1]],
    [SKILL[1],SKILL[7],M_SKILL[0],M_SKILL[2],ORIENT[1]]
    ]

    # 狗粮 
skills4 = [[SKILL[0],SKILL[2],SKILL[3]],
    [SKILL[1],SKILL[5]],
    [SKILL[4],SKILL[7],SKILL[8],ORIENT[1]]
    ]
    
    # 绿礼装狂兰(刷彩钢)
skills5 = [[SKILL[0],ORIENT[1],SKILL[6],ORIENT[1]],
    [SKILL[2],ORIENT[1],SKILL[5],M_SKILL[0],M_SKILL[3],ORIENT[1]], 
    [SKILL[8],ORIENT[1],SKILL[7],SKILL[1],M_SKILL[0],M_SKILL[1]]
    ]

    # 刷勋章。。。。
skills6 = [[SKILL[2],SKILL[3],ORIENT[2],SKILL[4],SKILL[5],M_SKILL[0],M_SKILL[3],ORIENT[0],ORIENT[2],ORIENT[3]],
    [SKILL[6],SKILL[7]],
    [SKILL[1],SKILL[3],ORIENT[0],SKILL[4],SKILL[5],ORIENT[0]]
]   

    # 万华镜阿脚
skills7 = [[SKILL[0],ORIENT[1],SKILL[6],ORIENT[1],SKILL[3]],
    [SKILL[2],ORIENT[1],SKILL[5]], 
    [SKILL[8],ORIENT[1],M_SKILL[0],M_SKILL[3],ORIENT[1]]
    ]
# (13,40) 起始坐标

def dog():
    #默认狗粮脚本 使用自爆弓孔明三回合
    script = FGO_Scripts()
    script.start()

def simple():
    cards = ["R", "R", "R"]
    skills = [[SKILL[7],],
              [SKILL[8], SKILL[6], ORIENT[0]], 
              [SKILL[4], SKILL[5], SKILL[3], M_SKILL[0], M_SKILL[1], ORIENT[1]]
             ]
    ultimate = [[], [], [0,1,2]]
    stratege = Fgo_stratege(cards=cards, skills=skills, ultimate=ultimate)
    script = FGO_Scripts(stratege=stratege, debug=True)
    script.start(epo=2)

def chie4():
    cards = ["R", "R", "R"]
    skills = skills7
    # ultimate = [[1], [1], [1]]
    ultimate = [[1],[1],[1]]
    stratege = Fgo_stratege(cards=cards, skills=skills, ultimate=ultimate)
    script = FGO_Scripts(stratege=stratege, debug=True)
    script.start(epo=1400)

def hard(num):
    cards = ["R", "G", "R"]
    skills = [[SKILL[2]],
              [SKILL[7], SKILL[8], SKILL[6], ORIENT[1], SKILL[0], SKILL[3], SKILL[5]], 
              [SKILL[2], M_SKILL[0], M_SKILL[1], ORIENT[0]]
             ]
    ultimate = [[0], [1], [2,0]]
    stratege = Fgo_stratege(cards=cards, skills=skills, ultimate=ultimate)
    script = FGO_Scripts(stratege=stratege)
    script.start(epo=num)

def lottery():
    Script = FGO_Scripts()
    Script.lottery()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--epoch", "-E", type=int, default=0,
                    help="loop number")
    parser.add_argument("--lottery", "-T", action="store_true",
                    help="if lottery")
    args = parser.parse_args()

    chie4()
    '''
    if args.epoch and args.lottery:
        raise RuntimeError("")
    if args.epoch:
        hard(args.epoch)
    if args.lottery:
        lottery()
    '''
    
    