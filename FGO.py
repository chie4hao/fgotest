# -*- coding: utf-8 -*-    
import numpy as np
import win32gui
import win32api
import win32con
from ctypes import *
from PIL import Image
import time
from utils import *

COLOR = ["R", "G", "B"]
#https://baike.baidu.com/item/%E8%99%9A%E6%8B%9F%E9%94%AE%E7%A0%81/9884611
BOTTOM = {
    "CHECK_POINT": 48,  #0
    "APPLE":       49,  #1
    "DECISION":    50,  #2
    "SUPPORT":     51,  #3
    "STRAT":       52,  #4
    "ITEMS":       53,  #5

    "NEXT":        52,  #4
    "END":         52,  #4

    "PICK_CARD":   79,
    "CARDS":       [80, 81, 82, 83, 84],
    "ULTIMATE":    [85, 86, 87],
    }#90

SKILL = [56, 57, 65, 66, 67, 68, 69, 70, 71]   #9 skill
M_SKILL = [72, 73, 74, 75]                     #4 master skill bottom
ORIENT = [76, 77, 78, 187]                          #3 use orient
CHANGE = [88, 89, 90]                          # x, y, z

LONG_TIME = 3
MIAD_TIME = 2
SHORT_TIME = 1
#######################################################################
class Fgo_stratege():
    """SKILL = [56, 57, 65, 66, 67, 68, 69, 70, 71]
       M_SKILL = [72, 73, 74, 75]
       ORIENT = [76, 77, 78]
       CHANGE = []
    """
    def __init__(self, cards = ["R", "R", "R"],
                       skills = [[SKILL[7], SKILL[8], SKILL[2]],
                                 [SKILL[6], ORIENT[0]],
                                 [M_SKILL[0], M_SKILL[2], ORIENT[1]]],
                       ultimate = [[0], [0], [0,1,2]]):
        """
        """
        self.round = [True] * len(cards)
        self.cards = cards
        self.skills = skills
        self.ultimate = ultimate

    def card_policy(self, cards, rd):
        ultimate = cards[5:]
        first = [BOTTOM["ULTIMATE"][index] for index in self.ultimate[rd] if ultimate[index]]
        second = [BOTTOM["CARDS"][index] for index in range(5) if cards[index] == self.cards[rd]]
        third = [BOTTOM["CARDS"][index] for index in range(5) if cards[index] != self.cards[rd]]
        pick = first + second + third
        return pick[0:3]

    def skill_policy(self, rd):
        if self.round[rd]:
            self.round[rd] = False
            return self.skills[rd]
        return []
    
    def reset(self):
        self.round = [True] * len(self.cards)



class FGO_Scripts():


    def __init__(self, classname = "BS2CHINAUI", titlename = "BlueStacks App Player", stratege = Fgo_stratege(), debug = False):
        self.hwnd = win32gui.FindWindow(classname, titlename)
        print(self.hwnd)
        hwndChildList = []     
        win32gui.EnumChildWindows(self.hwnd, lambda hwnd, param: param.append(hwnd),  hwndChildList)

        # print(hwndChildList)
        for i in hwndChildList:
            if(win32gui.GetClassName(i)=="BlueStacksApp"):
                self.hwnd=i
                break
        # print(self.hwnd)
        '''
        for hwnd in hwndChildList:
            left, top, right, bot = win32gui.GetWindowRect(hwnd)
            if  right-left == 1280 and bot-top == 720:
                asf = win32gui.GetWindowText(hwnd)
                sd = win32gui.GetClassName(hwnd)
                print(asf)
                print(sd)
                self.hwnd = hwnd
                break
        '''
            # print(right-left , bot-top)
        self.current_state = None
        self.image = None
        self.stratege = stratege
        self.debug = True
        self.click_wait_time = 0.01
    ##########################################################
    def start(self, epo = 10000):
        """循环函数"""

        self.click_wait_time = 0.2
        # 抽卡池
        image = capture(self.hwnd)
        if is_pool(image):
            while True:
                image = capture(self.hwnd)
                if (if_pool_re(image)):
                    self.click(54)
                    time.sleep(2)
                    self.click(50)
                    while True:
                        self.click(54)
                        image = capture(self.hwnd)
                        if (is_pool(image)):
                            break
                        time.sleep(1)
                else: 
                    for i in range(10):
                        self.click(53)


        for i, _ in enumerate(range(epo)):
            print("Star epoch:",i + 1, "------------------------")
            start = time.time()
            #####################################
            while True_Type(self.current_state):
                self.current_state = self.get_state(None)
                time.sleep(SHORT_TIME)
            if self.current_state == "HOME":
                self.start_mission()
            elif self.current_state == "BATTLE":
                self.battle()
            else:
                self.end()
            ####################################
            speed = time.time() - start
            print("End epoch:",i + 1,"and used time ", speed)
            self.stratege.reset()

                
    def  lottery(self):
        "用来抽奖"
        while True:
            self.click(BOTTOM["CARDS"][1])
            time.sleep(0.25)
    
    #########################################################
    def start_mission(self):
        """
        """
        #click check point
        self.click_wait_time = LONG_TIME
        # self.click(BOTTOM["CHECK_POINT"])

        '''
        while True:
            if self.get_state(["APPLE"]) == "APPLE":
                #click apple and click decision
                self.click(BOTTOM["APPLE"])
                self.click(BOTTOM["DECISION"])
                time.sleep(1)
            else
                break
        '''

        # self.get_state()
        while True:
            self.get_state()
            if is_support(self.image):
                break
            time.sleep(1)

        # choose support
        while True:
            asdf = is_requiresupport(self.image)
            if asdf == 1:
                self.click(BOTTOM["SUPPORT"])
                break
            elif asdf == 2:
                self.click(BOTTOM["CARDS"][2])
                break
            else:
                # toggle
                # (211, 574) to (211, 374)
                print("toggle")
                '''
                client_pos = win32gui.ScreenToClient(self.hwnd, (111, 650))
                client_pos2 = win32gui.ScreenToClient(self.hwnd, (111, 250))
                tmp=win32api.MAKELONG(client_pos[0],client_pos[1])
                tmp1=win32api.MAKELONG(client_pos2[0],client_pos2[1])
                win32gui.SendMessage(self.hwnd, win32con.WM_ACTIVATE,win32con.WA_ACTIVE,0)
                win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN,win32con.MK_LBUTTON,tmp)
                time.sleep(0.01)
                #win32api.SendMessage(self.hwnd, win32con.WM_MOUSEMOVE,win32con.MK_LBUTTON,tmp1)
                # time.sleep(0.5)
                win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONUP,win32con.MK_LBUTTON,tmp)
                time.sleep(0.44)
                win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONUP,win32con.MK_LBUTTON,tmp)
                time.sleep(0.44)

                win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONUP,win32con.MK_LBUTTON,tmp)
                '''
                windll.user32.SetCursorPos(111, 634)    #鼠标移动到  
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)    #左键按下
                time.sleep(0.5)
                move = 50
                initial = 0
                for _ in range(0,200):
                    move -= 3
                    if move <= 1:
                        move = 1
                    initial += move
                    # print(move)
                    windll.user32.SetCursorPos(111, 634-initial)
                    time.sleep(0.05)
                    if(initial >= 400):
                        break
                time.sleep(0.4)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                # time.sleep(0.2)
            while True:
                self.image = capture(self.hwnd)
                if is_support(self.image):
                    break
                else:
                    self.click(88)
                    self.click(89)
                    while True:
                        self.image = capture(self.hwnd)
                        if is_support(self.image):
                            time.sleep(1)
                            break
                        else:
                            print("choose support ERROR")
                            time.sleep(1)
                            break

        #clik start mision
        self.click(BOTTOM["STRAT"])
        items = False
        if items:
            self.click(BOTTOM["ITEMS"])
        #loop waiting for load
        while self.current_state != "BATTLE":
            self.current_state = self.get_state(["BATTLE"])
            #wait gap time 
            time.sleep(MIAD_TIME)
        #battle
        self.battle()
        #end mission
    
    def battle(self):
        """
        """
        while self.current_state != "END":
            if self.current_state == "BATTLE":
                while True:
                    time.sleep(1)
                    #try:
                    self.get_state()
                    rd = get_round(self.image)
                    print("round:" + str(rd))
                    if rd == 0 or rd == 1 or rd == 2:
                        break
                    #except(SystemError, RuntimeError, IndexError):
                    #    continue
                
                #use skill by strategy and rd
                skills = self.stratege.skill_policy(rd)
                self.click_wait_time = LONG_TIME
                self.click(skills,until=None)
                #click battle to pick cards
                self.click(BOTTOM["PICK_CARD"])



                while True:
                    self.image = capture(self.hwnd)
                    if is_pcards(self.image):
                        break
                    self.click(BOTTOM["PICK_CARD"])

                #update image
                self.get_state(["BATTLE"])
                #update card information
                cards = getcard(self.image)
                #pick card by cards
                pcards = self.stratege.card_policy(cards, rd)
                self.click_wait_time = SHORT_TIME
            
                self.click(pcards)

                time.sleep(3)
                while(True):
                    image = capture(self.hwnd)
                    if is_pcards(image):
                        self.click([80, 81, 82, 83, 84])
                        time.sleep(0.8)
                    else:
                        break


                #wait to next step
                if self.debug:
                    print("Current state:", self.current_state)
                    print("Current round:", rd)
                    print("Skill strateges:", skills)
                    print("Current cards:", cards)
                    print("Pick cards:", pcards)
                self.current_state = self.get_state(["BATTLE"])            
            else:
                #wait time
                self.current_state = self.get_state(["BATTLE"])
                if self.current_state == "END":
                    break
                elif self.current_state == "BATTLE":
                    continue
                '''
                rd = get_round(self.image)
                if rd == -1:
                    print(1234)
                    while True:
                        windll.user32.SetCursorPos(298,213)    #鼠标移动到
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)    #左键按下
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                        time.sleep(3)
                        image = capture(self.hwnd)
                        if is_comfirm(self.image):
                            print(3456)
                            self.click(50)
                            break
                '''
                # self.click(BOTTOM["APPLE"])
                self.click(90)
                time.sleep(1)
        
        self.end()
        '''
        #buffer time to avoid make error in judgment
        time.sleep(0.25)
        self.current_state = self.get_state()
        if self.current_state == "END":
            #end mission
            self.end()
        # recursion
        else:
            self.battle()
        '''
    def end(self):
        """
        """
        while self.current_state is not "HOME":
            #click one posion while state is Home
            self.click(BOTTOM["NEXT"])
            time.sleep(1)
            self.current_state = self.get_state(["HOME"])
        return True
    #########################################################
    def get_state(self, state=None):
        """
        """
        image = capture(self.hwnd)
        self.image = image
        state = getstate(self, image, state)
        if state:
            print("current state:", state)
        return state
    ########################################
    def click(self, position,until=None):
        """鼠标点击操作SendMessage
            PostMessage
        """
        print("click", position)
        if isinstance(position, int):
            positions = [position]
        elif isinstance(position, list):
            positions = position
        else:
            raise ValueError("input error data type")
        
        for position in positions:
            #print("click position:", position)
            win32api.keybd_event(position, 0, 0, 0)    #左键按下
            win32api.keybd_event(position, 0, win32con.KEYEVENTF_KEYUP, 0)
            # win32api.SendMessage(self.hwnd, win32con.WM_KEYDOWN, position, 0)
            # win32api.SendMessage(self.hwnd, win32con.WM_KEYUP, position, 0)  
            time.sleep(self.click_wait_time)
            if until:
                state = self.get_state([until])
                while state != until:
                    time.sleep(SHORT_TIME)
                    state = self.get_state([until])

if __name__ == '__main__':
    fgo = FGO_Scripts()
    while True:
        try:
            fgo.get_state()
            get_round(fgo.image)
        except(RuntimeError, IndexError):
            print("sssss")
        time.sleep(1)


