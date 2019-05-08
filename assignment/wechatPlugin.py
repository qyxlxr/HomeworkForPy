import sqlite3
import time
import cv2
import numpy as np
from aip import AipOcr
import os
import pyautogui
import win32api
import win32gui

selfFrame = '27292c'
selfSearch = 'dbd9d8'
chatBackground = 'f5f5f5'
chatItForeground = 'ffffff'

WeChatPos = {}


def changeColor(value):
    value = value.upper()
    digit = list(map(str, range(10))) + list("ABCDEF")
    if isinstance(value, tuple):
        string = '#'
        for i in value:
            a1 = i // 16
            a2 = i % 16
            string += digit[a1] + digit[a2]
        return string
    elif isinstance(value, str):
        a1 = digit.index(value[1]) * 16 + digit.index(value[2])
        a2 = digit.index(value[3]) * 16 + digit.index(value[4])
        a3 = digit.index(value[5]) * 16 + digit.index(value[6])
        return a1, a2, a3


# 计算欧几里德距离：
def euclidean(p, q):
    # # 如果两数据集数目不同，计算两者之间都对应有的数
    # same = 0
    # for i in p:
    #     if i in q:
    #         same += 1

    # 计算欧几里德距离,并将其标准化
    e = sum([float(p[i] - q[i]) ** 2 for i in range(p.__len__())])
    return 1 / (1 + e ** .5)


def getWeChatpos():
    """返回值：窗口左上角和右下角坐标"""
    classname = "WeChatMainWndForPC"
    titlename = "微信"
    # 获取句柄
    hwnd = win32gui.FindWindow(classname, titlename)
    # 获取窗口左上角和右下角坐标
    return win32gui.GetWindowRect(hwnd)


def openWechat():
    win32api.ShellExecute(0, 'open', r'C:\Program Files (x86)\Tencent\WeChat\Wechat.exe', '', '', 1)
    # screenWidth, screenHeight = pyautogui.size()
    # currentMouseX, currentMouseY = pyautogui.position()
    # initx, inity = pyautogui.position()
    # print(pyautogui.locateOnScreen("wechat.png"))
    # pyautogui.moveTo()
    # pyautogui.click()
    # pyautogui.moveTo(initx, inity)


def BaiduOCR(imagefile):
    # 百度OCR识别
    APP_ID = '16205886'
    API_KEY = '11cgmBlpYydUMCTIe0MzcecW'
    SECRET_KEY = 'teW5LS8oR7dwSkGYoBmHC1ua51c6DhC2'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    """ 读取图片 """

    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    image = get_file_content(imagefile)
    """ 调用通用文字识别, 图片参数为本地图片 """
    print(client.basicGeneral(image))


""" 带参数调用通用文字识别, 图片参数为本地图片 """


# """ 如果有可选参数 """
# options = {}
# options["language_type"] = "CHN_ENG"
# options["probability"] = "true"
# print(client.basicGeneral(image, options))


# _, binary1 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
# _, binary2 = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY_INV)
# binary = cv2.bitwise_and(binary1, binary2)
# cv2.imshow("img", binary)
# cv2.waitKey(0)
def getchatMyForeground():
    _, binary1 = cv2.threshold(gray, 195, 255, cv2.THRESH_BINARY)
    _, binary2 = cv2.threshold(gray, 197, 255, cv2.THRESH_BINARY_INV)
    binary = cv2.bitwise_and(binary1, binary2)
    cv2.imshow("img", binary)
    cv2.waitKey(0)
    return cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


def get_chatFrame_chatItForeground():
    _, binary1 = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)
    _, binary2 = cv2.threshold(gray, 255, 255, cv2.THRESH_BINARY_INV)
    binary = cv2.bitwise_and(binary1, binary2)
    cv2.imshow("img", binary)
    cv2.waitKey(0)
    return cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


def get_chatFrame():
    contours, hierarchy = get_chatFrame_chatItForeground()
    tempimg = img.copy()
    return maxContours(contours, tempimg)


def get_chatItForeground():
    contours, hierarchy = get_chatFrame_chatItForeground()
    return otherContours(contours)


def getItName():
    _, binary1 = cv2.threshold(gray, 188, 255, cv2.THRESH_BINARY)
    _, binary2 = cv2.threshold(gray, 195, 255, cv2.THRESH_BINARY_INV)
    binary = cv2.bitwise_and(binary1, binary2)
    cv2.imshow("img", binary)
    cv2.waitKey(0)
    return cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


def maxContours(contours, img):
    # c_max = []
    max_area = 0
    max_cnt = 0
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(contours[i])
        # find max countour
        if area > max_area:
            if max_area != 0:
                c_min = [max_cnt]
                cv2.drawContours(img, c_min, -1, (0, 0, 0), cv2.FILLED)
            max_area = area
            max_cnt = cnt
        else:
            c_min = [cnt]
            cv2.drawContours(img, c_min, -1, (0, 0, 0), cv2.FILLED)

    # c_max.append(max_cnt)
    return max_cnt
    # cv2.drawContours(img, c_max, -1, (0, 0, 255), thickness=3)
    # cv2.imwrite("mask.png", img)
    # cv2.imshow('mask', img)
    # cv2.waitKey()


# def getNowChatName(func,img):
#     point=getContoursRectPoint(func,img)
#     for


def otherContours(contours, img):
    c_other = []
    max_area = 0
    max_cnt = 0
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(contours[i])
        # find max countour
        if area > max_area:
            if max_area != 0:
                c_min = [max_cnt]
                cv2.drawContours(img, c_min, -1, (0, 0, 0), cv2.FILLED)
            max_area = area
            max_cnt = cnt
        else:
            c_min = [cnt]
            cv2.drawContours(img, c_min, -1, (0, 0, 0), cv2.FILLED)

    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(contours[i])
        if area != max_area:
            c_other.append(cnt)
    return c_other


def getContoursRectPoint(func, img):
    # step7：裁剪。box里保存的是绿色矩形区域四个顶点的坐标。我将按下图红色矩形所示裁剪昆虫图像。
    # 找出四个顶点的x，y坐标的最大最小值。新图像的高=maxY-minY，宽=maxX-minX。
    rect = cv2.minAreaRect(func())  # 得到最小外接矩形的（中心(x,y), (宽,高), 旋转角度）
    return cv2.boxPoints(rect)  # 通过box绘出矩形框


def getContoursImages(func, img):
    # step7：裁剪。box里保存的是绿色矩形区域四个顶点的坐标。我将按下图红色矩形所示裁剪昆虫图像。
    # 找出四个顶点的x，y坐标的最大最小值。新图像的高=maxY-minY，宽=maxX-minX。
    rect = cv2.minAreaRect(func())  # 得到最小外接矩形的（中心(x,y), (宽,高), 旋转角度）
    box = np.int0(getContoursRectPoint(func, img))  # 通过box绘出矩形框
    Xs = [i[0] for i in box]
    Ys = [i[1] for i in box]
    x1 = min(Xs)
    x2 = max(Xs)
    y1 = min(Ys)
    y2 = max(Ys)
    hight = y2 - y1
    width = x2 - x1
    cropImg = img[y1:y1 + hight, x1:x1 + width]
    cv2.imshow("cropImg", cropImg)
    cv2.waitKey()


def getNewsNumber(img):
    redNews = "ff3b30"
    color1 = [0, 0, 0]
    color2 = [0, 0, 0]
    color2[0], color2[1], color2[2] = changeColor(redNews)
    height = WeChatPos["EndY"] - WeChatPos["StartY"]
    width = WeChatPos["EndX"] - WeChatPos["StartX"]
    for x in range(WeChatPos["StartX"], WeChatPos["EndX"]):
        for y in range(WeChatPos["StartY"], WeChatPos["EndY"]):
            color1[0], color1[1], color1[2] = pyautogui.pixel(x, y)
            if euclidean(color1, color2) > 0.9:
                for i in range(0, 11):
                    if height / 11 * i < y < height / 11 * (i + 1):
                        return i


if __name__ == '__main__':
    openWechat()
    time.sleep(1)
    WeChatPos["startX"], WeChatPos["startY"], WeChatPos["EndX"], WeChatPos["EndY"] = getWeChatpos()
    # color1[0], color1[1], color1[2] = pyautogui.pixel(WeChatPos["startX"] + 10, WeChatPos["startY"] + 10)
    # color2[0], color2[1], color2[2] = pyautogui.pixel(WeChatPos["startX"] + 12, WeChatPos["startY"] + 10)
    # print(euclidean(color1, color2))
    pyautogui.screenshot("test.jpg")
    img = cv2.imread("test.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    contours, ha = getchatMyForeground()
    cv2.drawContours(img, contours, -1, (0, 0, 255), 3)
    cv2.imshow("img", img)
    cv2.waitKey(0)
    # if os.path.exists('test.db') is False:
    #     conn = sqlite3.connect("test.db")
    #     c = conn.cursor()
    #     c.execute('''create table friends(_friendId integer primary key autoincrement,
    #     name text''')
    #     c.execute('''create table message(__message_Id integer primary key autoincrement,
    #     messageContent text,
    #     _friendId integer,
    #     isWithdraw integer,
    #     messageTime text,''')
    #     c.close()
    #     conn.close()

print(BaiduOCR("test.png"))
# cv2.imshow("img", img)
# cv2.waitKey(0)
# time.sleep(0.5)
# pyautogui.press('up')
# time.sleep(0.5)
# pyautogui.press('up')
# pyautogui.doubleClick()
# pyautogui.moveTo(500, 500, duration=2,
#                  tween=pyautogui.easeInOutQuad)  # use tweening/easing function to move mouse over 2 seconds.
# pyautogui.typewrite('Hello world!', interval=0.25)  # type with quarter-second pause in between each key

# pyautogui.keyDown('shift')
# pyautogui.press(['left', 'left', 'left', 'left', 'left', 'left'])
# pyautogui.keyUp('shift')
# pyautogui.hotkey('ctrl', 'c')
