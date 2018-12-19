# -*- coding: utf-8 -*-   
import os
import numpy as np
from PIL import Image, ImageGrab
import time
import matplotlib.pyplot as plt
import pytesseract
import win32api
import win32gui
import win32ui
import win32con
from ctypes import windll
import cv2
############################鼠标点击使用常数########################################
X1 = float(1032)                                         #STEP 1
Y1 = float(578)
################################获取信息的常数################
X6 = float(1032)  
tem = float(578)   
Y6A = float(331/tem)
Y6B = float(487/tem)
Y6C = float(87/tem)
Y6D = float(243/tem)

CARDS_POSITONS = [(float(45/X6), Y6A, float(165/X6), Y6B), (float(250/X6), Y6A, float(370/X6), Y6B),\
                  (float(455/X6), Y6A, float(575/X6), Y6B), (float(660/X6), Y6A, float(780/X6), Y6B),\
                  (float(865/X6), Y6A, float(985/X6), Y6B), (float(275/X6), Y6C, float(395/X6), Y6D),\
                  (float(460/X6), Y6C, float(580/X6), Y6D), (float(645/X6), Y6C, float(765/X6), Y6D)]

BATTLE = (float(850/1025) , float(433/581), float(975/1025) , float(550/581))
ROUND = [float(690/X1), float(6/Y1), float(746/X1), float(34/Y1)]          #第几回合
# END = (float(45/X1), float(340/Y1), float(989/X1), float(442/Y1))          #结束界面判定
END = (float(800/X1), float(520/Y1), float(990/X1), float(570/Y1))          #结束界面判定

CHOICE_CHECK_BOX = (float(880/X1), float(516/Y1), 1, 1)   #主界面
CHECK_APPLE_BOX = (float(258/X1), float(96/Y1), float(346/X1), float(193/Y1))    #确认苹果界面


BORDER = [40, 55, 0, 0]

BOXS = {
    "HOME":  CHOICE_CHECK_BOX,
    "APPLE": CHECK_APPLE_BOX,
    "BATTLE":BATTLE,
#    "END":   END,
    "ROUND": ROUND,
    "CARDS": CARDS_POSITONS
}
################################对比的常数#########################
path = os.path.join(os.path.abspath(os.path.dirname(os.path.realpath('__file__'))), "data")
CHECK_POINT = Image.open(os.path.join(path,"check.png"))    #选关卡图片  用来对比
CHECK_APPLE = Image.open(os.path.join(path,"apple.png"))          #吃苹果图片
BATTLE_SCREEM = Image.open(os.path.join(path,"battle.png"))       #人物头像，用来确认是否在技能界面
CHECH_SUPPORT = Image.open(os.path.join(path,"teasupport.png"))
QP_SUPPORT = Image.open(os.path.join(path,"qpsupport.png"))

# END_SCREEM = Image.open(os.path.join(path,"end.png"))
# STATE = ["HOME", "APPLE", "BATTLE", "END"]
STATE = ["HOME", "APPLE", "BATTLE"]
# IMAGES = {"HOME":CHECK_POINT, "APPLE":CHECK_APPLE, "BATTLE":BATTLE_SCREEM, "END": END_SCREEM}
IMAGES = {"HOME":CHECK_POINT, "APPLE":CHECK_APPLE, "BATTLE":BATTLE_SCREEM}

##################################################################外部方法
def True_Type(input):
    if input:
        return False
    else:
        return True

def show_plot(image):
    plt.figure("Image")
    plt.imshow(image)
    plt.show()

def Absolute_Position(position, size):
    """return Absolute position in image
    """
    rp = position*np.array(size*2)
    return rp.astype(np.int32)
'''
def Crop_Border(image):
    """crop windows border to get game image
    """
    size = image.size
    box = [6, 46, 1286 ,766]
    # box = [BORDER[2], BORDER[0], size[0] - BORDER[3], size[1] - BORDER[1]]
    image = image.crop(box)
    return image
'''
def Crop(image, box):
    """crop image using box Relative_Box get image to confirm state
    """
    true_box = Absolute_Position(box, list(image.size))
    image = image.crop(true_box)
    return image
########################################################################################
def is_end(image):
    image = np.array(image)
    size = np.size(image)
    energy = np.sum(image)/size
    dark = np.sum(image < 30)/size
    color = np.sum(image > 235)/size
    if dark > 0.8 and color > 0.025:
        print(dark, color)
        return True
    else:
        False

def getcolor(image):
    COLOR = ["R", "G", "B"]
    image = np.array(image.convert("RGB"))
    c_min = np.min(image, axis=2)
    array = image - np.expand_dims(c_min, axis=2)
    c_max = [np.max(array[:,:,i]) for i in range(3)]
    c_sum = [np.sum(array[:,:,i]) for i in range(3)]
    if (c_max > np.array([233, 233, 233])).any():
        idx = np.argmax(c_sum)
        color = COLOR[idx]
        return color
    else:
        return None

def Compare(img1, img2, size = (64, 64)):
    img1 = np.array(img1.resize(size).convert("RGB"))/256
    img2 = np.array(img2.resize(size).convert("RGB"))/256
    loss = np.max(np.abs(img1 - img2), axis=2)
    loss = np.sum(loss < 0.2)/(64*64)
    if loss > 0.75:
        return True
    else:
        return False
######################################################################
def getcard(image):
    # image = Crop_Border(image)
    cards = [Crop(image, box) for box in BOXS["CARDS"]]
    cards = [getcolor(card) for card in cards]
    return cards

def getstate(self, image, s = None):
    # image = Crop_Border(image)

    '''
    b = image.getpixel((923, 56))
    print(b)
    print(b==(123,124,124))
    '''

    # image.save("test.png")
    if s:
        search_state = s
    else:
        search_state = STATE
    
    for i in search_state:
        img = Crop(image, BOXS[i])
        # img.save(i+".png")
        if IMAGES[i]:
            if Compare(img, IMAGES[i]):
                if i == "APPLE":
                    self.click(49)
                    self.click(50)
                    time.sleep(1)
                    break
                return i
    # print(image.getpixel((1006,682)))
    # if image.getpixel((949, 675))==(0xB4,0xAF,0x9E) and image.getpixel((1006,682)) == (0xD2,0xD2,0xD2) and image.getpixel((1059,693))==(0x5A,0x66,0x75) and image.getpixel((1155,685))==(0x2C,0x33,0x68):
    if image.getpixel((912, 59))==(0x8E,0x8E,0x8E) and image.getpixel((923,57)) == (0x8D,0x8D,0x8D) and image.getpixel((911,29))==(0x77,0x77,0x77) and image.getpixel((913,53))==(0x83,0x83,0x83):
        return "END"
    elif image.getpixel((273,158))==(0xc3,0x92,0x70) and image.getpixel((282,159))==(0x47,0x42,0x46)\
        and image.getpixel((282,162))==(0x55,0xe9,0xd3)and image.getpixel((316,162))==(0xfb,0xc6,0x88):
        print("REBOOTING")
        while True:
            windll.user32.SetCursorPos(298,213)    #鼠标移动到
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)    #左键按下
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            time.sleep(3)
            image = capture(self.hwnd)
            if is_comfirm(image):
                print("REBOOT SUCCESS")
                self.click(50)
                break
            elif is_cha(image):
                print("click cha")
                self.click(55)
                break

        self.click(90)

    elif image.getpixel((832,557))==(0x7c,0x7c,0x7c) and image.getpixel((776,557))==(0x04,0x04,0x04)\
        and image.getpixel((776,559))==(0x22,0x22,0x22) and image.getpixel((776,560))==(8,8,8)\
        and image.getpixel((776,567))==(3,3,3) and image.getpixel((842,557))==(0x8d,0x8d,0x8d):
        print("network error")
        self.click(50)
        time.sleep(2)
    elif (i!="APPLE"):
        return False
    image = capture(self.hwnd)
    self.image=image
    s=getstate(self,image)
    return s


def is_support(image):
    # image = Crop_Border(image)
    # print(image.getpixel((859,275)))
    if image.getpixel((843,258))==(21,106,1) and image.getpixel((928,258))==(25,59,116) and image.getpixel((1013,258))==(123,17,8):
        return True
    return False

def is_pcards(image):
    # image = Crop_Border(image)
    # print(image.getpixel((859,275)))
    if image.getpixel((1059,59))==(0xff,0xff,0xff) and image.getpixel((1147,680))==(0x0f,0xac,0xd6) and image.getpixel((1180,681))==(0xbd,0xdc,0xfa)and image.getpixel((1212,681))==(0x0d,0x3f,0x64):
        return True
    return False

# 师匠红茶学妹
require =[
    (51, 326, 96, 126, 172), (129,340, 203, 159, 176), (162,351, 255, 241, 233), (191, 359, 248, 251, 179),
    (57, 288, 216, 158, 249), (80, 266, 69, 31, 67), (143, 260, 167, 77, 77), (190, 286, 195, 222, 118),
    (1138, 343, 0x7E, 0xB2, 0x37), (1160, 332, 0xDF, 0xFF, 0xAD)]
'''
require =[
    (51, 326, 103, 134, 173), (129,340, 231, 182, 206), (162,351, 255, 241, 230), (191, 359, 248, 251, 179),
    (57, 288, 216, 158, 249), (80, 266, 62, 22, 71), (143, 260, 156, 59, 59), (190, 286, 195, 222, 118),
    (1138, 343, 0x7E, 0xB2, 0x37), (1160, 332, 0xDF, 0xFF, 0xAD)]
'''
'''
# 蒙娜丽莎
require =[(61,335,73,96,192),(110,353,22,47,72),(130,364,255,189,148),(190,358,254,254,168),
    (1138, 343, 0x7E, 0xB2, 0x37), (1160, 332, 0xDF, 0xFF, 0xAD)]
'''
def Compare_support(img1, img2, size = (64, 64)):
    img1 = np.array(img1.resize(size).convert("RGB"))/256
    img2 = np.array(img2.resize(size).convert("RGB"))/256
    loss = np.max(np.abs(img1 - img2), axis=2)
    loss = np.sum(loss < 0.2)/(64*64)
    if loss > 0.95:
        return True
    else:
        return False

def is_comfirm(image):
    # image = Crop_Border(image)
    if image.getpixel((736,376))==(0xff,0,0) and image.getpixel((746,555))==(0xdc,0xdd,0xdd)\
        and image.getpixel((770,560))==(5,5,5)and image.getpixel((898,575))==(0x33,0x33,0x34):
        return True
    return False

def is_cha(image):
    if image.getpixel((1210,0))==(0x5c,0x5d,0x5d) and image.getpixel((1211,0))==(0xe5,0xe5,0xe5)\
        and image.getpixel((1213,2))==(0x99,0x99,0x99)and image.getpixel((1213,3))==(0x32,0x32,0x32)\
        and image.getpixel((1214,2))==(0x7f,0x7f,0x7f):
        return True
    return False

def is_pool(image):
    if image.getpixel((454,686))==(0x12,0x7a,0xb3) and image.getpixel((458,686))==(0xaf,0xb9,0xc5)\
        and image.getpixel((475,686))==(0xc7,0xda,0xe0)and image.getpixel((501,686))==(0xd1,0xd5,0xd9)\
        and image.getpixel((449,361))==(0xf8,0x88,0x39):
        return True
    return False

def if_pool_re(image):
    print(image.getpixel((200,426)),image.getpixel((200,440)),image.getpixel((200,463)),image.getpixel((203,485)))

    if image.getpixel((200,426))==(0x09,0x50,0x6f) and image.getpixel((200,440))==(0x07,0x5a,0x75)\
        and image.getpixel((200,463))==(0x05,0x5f,0x78)and image.getpixel((203,485))==(0xff,0xff,0xff):
        return True
    return False

def is_requiresupport(image):
    # return -1
    # image = Crop_Border(image)
    '''
    if image.getpixel((191,359))==(248,251,179) and image.getpixel((190,286))==(195,222,118)\
        and image.getpixel((1138,343))==(0x7e,0xb2,0x37)and image.getpixel((1160,332))==(0xdf,0xff,0xad):
        box = [51, 326, 208, 370]
        image1 = image.crop(box)
        if Compare_support(image1, QP_SUPPORT):
            return 1
    if image.getpixel((191,559))==(248,251,179) and image.getpixel((190,486))==(195,222,118)\
        and image.getpixel((1138,543))==(0x7e,0xb2,0x37)and image.getpixel((1160,532))==(0xdf,0xff,0xad):
        box = [51, 526, 208, 570]
        image2 = image.crop(box)
        if Compare_support(image2, QP_SUPPORT):
            return 2
    '''
    '''
    if image.getpixel((191,359))==(248,251,179) and image.getpixel((190,286))==(195,222,118)\
        and image.getpixel((1138,343))==(0x85,0xb7,0x33) and image.getpixel((1160,332))==(0xe1,0xfe,0xaf):
        # and image.getpixel((1138,343))==(0x7e,0xb2,0x37)and image.getpixel((1160,332))==(0xdf,0xff,0xad):
 
        box = [51, 240, 208, 370]
        image1 = image.crop(box)
        if Compare_support(image1, CHECH_SUPPORT):
            return 1
    if image.getpixel((191,559))==(248,251,179) and image.getpixel((190,486))==(195,222,118)\
        and image.getpixel((1138,343))==(0x85,0xb7,0x33) and image.getpixel((1160,332))==(0xe1,0xfe,0xaf):
        # and image.getpixel((1138,543))==(0x7e,0xb2,0x37)and image.getpixel((1160,532))==(0xdf,0xff,0xad):
        box = [51, 440, 208, 570]
        image2 = image.crop(box)
        if Compare_support(image2, CHECH_SUPPORT):
            return 2
    '''
    
    # 刷池子cba助战
    if image.getpixel((53,376))==(0xe6,0xbc,0x50) and image.getpixel((62,376))==(0xef,0xcd,0x66)\
        and image.getpixel((70,288))==(0xd7,0x9e,0xf8) and image.getpixel((114,277))==(0xff,0xff,0xe0)\
        and image.getpixel((163,275))==(0x80,0x3e,0x70) and image.getpixel((190,286))==(195,222,118) \
        and image.getpixel((1138,343))==(0x85,0xb7,0x33) and image.getpixel((1160,332))==(0xe1,0xfe,0xaf)\
        and image.getpixel((191,359))==(248,251,179):
        return 1
    if image.getpixel((53,576))==(0xe6,0xbc,0x50) and image.getpixel((62,576))==(0xef,0xcd,0x66)\
        and image.getpixel((70,488))==(0xd7,0x9e,0xf8) and image.getpixel((114,477))==(0xff,0xff,0xe0)\
        and image.getpixel((163,475))==(0x80,0x3e,0x70) and image.getpixel((190,486))==(195,222,118)\
        and image.getpixel((1138,543))==(0x85,0xb7,0x33) and image.getpixel((1160,532))==(0xe1,0xfe,0xaf)\
        and image.getpixel((191,559))==(248,251,179): 
        return 2
    
    return 0
    '''
    for i in require:
        if image.getpixel((i[0], i[1])) == (i[2], i[3], i[4]):
            print(True)
        else: print(False)
    
    for i in require:
        if image.getpixel((i[0], i[1])) != (i[2], i[3], i[4]):
            flag=2
            break
    if flag == 1:
        return 1
    for i in require:
        if image.getpixel((i[0], i[1]+200)) != (i[2], i[3], i[4]):
            flag=0
            break
    return flag
    '''

'''
def is_xuemei(image):
    image = Crop_Border(image)
    if image.getpixel((51, 326))==(172,126,96) and image.getpixel((129,340)) == (176,158,203) and image.getpixel((162,351))==(233,241,255) and image.getpixel((191,359))==(179,251,248):
        return True
    return False

def is_shijiang(image):
    image = Crop_Border(image)
    if image.getpixel((57, 488))==(249,158,216) and image.getpixel((80,466)) == (67,31,69) and image.getpixel((143,460))==(77,77,167) and image.getpixel((190,486))==(118,222,195):
        return True
    return False
'''
def get_round(image):
    # config = "--psm 10 digits"
    # image = Crop_Border(image)


    # image = Crop(image, BOXS["ROUND"])
    # image = image.convert("L")
    # image.save("round.png")
    # code = pytesseract.image_to_string(image, config=config)[0]

    # print(pytesseract.image_to_string(image, config=config))

    # round 3 876,29 (255,255,255) 870,16 (250,250,250) 875,18 (255,255,255)
    if image.getpixel((873, 31))==(255,255,255) and image.getpixel((873,15)) == (92,92,92) and image.getpixel((871,17))==(234,234,234) and image.getpixel((867,19))==(200,200,200):
        return 0
    elif image.getpixel((866, 17))==(113,113,113) and image.getpixel((873,16)) == (254,254,254) and image.getpixel((876,22))==(235,235,235) and image.getpixel((873,33))==(214,214,214):
        return 1
    elif image.getpixel((867, 16))==(118,118,118) and image.getpixel((875,16)) == (194,194,194) and image.getpixel((875,27))==(198,198,198) and image.getpixel((867,33))==(174,174,174):
        return 2
    elif image.getpixel((273,158))==(0xc3,0x92,0x70) and image.getpixel((282,159))==(0x47,0x42,0x46)\
        and image.getpixel((282,162))==(0x55,0xe9,0xd3)and image.getpixel((316,162))==(0xfb,0xc6,0x88):
        return -1
    else:
        return 3
    
def capture(hwnd):
    """capture applications screem"""
    # left, top, right, bot = win32gui.GetWindowRect(hwnd)
    # w = (right - left)
    # h = (bot - top)
    # 104,37   106,67 
    # print(hwnd)
    # win32gui.ShowWindow(hwnd,win32con.SW_RESTORE)
    # win32gui.SetForegroundWindow(hwnd)
    game_rect=win32gui.GetWindowRect(hwnd)
    src_image=ImageGrab.grab(game_rect)
    # src_image.save("123466.png")
    '''
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()


    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)



    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    im = Image.frombuffer('RGB',(bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                           bmpstr, 'raw', 'BGRX', 0, 1)

    im.save("21234.png")
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
    '''
    # if result == 1:
        # PrintWindow Succeeded
        # im.save("test.png")
        # im.show()
    
    '''
    if w <= 200 or h <= 200:
        raise "captrue error"
    '''    
    return src_image

if __name__ == '__main__':
    scrpt = None
        
