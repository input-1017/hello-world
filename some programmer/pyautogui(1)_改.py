# -*- coding: utf-8 -*-
import pyautogui
import time
import os

pyautogui.click(x=790, y=853, clicks=1, duration=0.4, tween=pyautogui.linear)
# 进入Google


def inspect(count_len, end, start):  # 后备检查

    os.system('say "I was completed this work"')

    pyautogui.confirm('''完成
    总用时[%s]''' % (end-start), buttons=['确定'])

    if count_len == 30:
        print('good job!')
        pass
    else:
        pyautogui.confirm('还有[%s]个图片没收录' % count_len, buttons=['确定'])


def down():  # 下移
    pyautogui.keyDown('down')
    pyautogui.keyDown('down')
    pyautogui.keyDown('down')
    pyautogui.keyDown('down')
    pyautogui.keyDown('down')
    pyautogui.keyDown('down')


def link(n):  # 行
    # 每行有五张
    pyautogui.click(x=n, y=660, clicks=1, duration=0.8, tween=pyautogui.linear)
    pyautogui.leftClick()


def click_picture():  # 点，拖，存。一体
    pyautogui.moveTo(x=530, y=480, duration=1, tween=pyautogui.linear)
    pyautogui.leftClick()

    pyautogui.moveTo(x=560, y=500, duration=1.6, tween=pyautogui.linear)

    pyautogui.dragTo(x=200, y=850, duration=0.5, button='left')
    # 拖拽至指定位置
    pyautogui.click(x=780, y=44, duration=0.4)


def row():  # 列
    pyautogui.moveTo(x=400, y=660, duration=0.3)
    # 回到当行的第一张图片位置
    down()


def main(n, count, count1, ph_width):

    while count < 6:
        while count1 < 5:
            link(n)
            click_picture()
            n += ph_width
            count1 += 1

        n = 400
        count1 = 0
        count += 1
        row()


if __name__ == '__main__':
    before = os.listdir('/Users/lbq/Desktop/图(各大网站)')
    start_time = time.time()

    main(400, 0, 0, 208)

    end_time = time.time()

    after = os.listdir('/Users/lbq/Desktop/图(各大网站)')
    finely_len = 30 - (len(after) - len(before))

    inspect(finely_len, end_time, start_time)  # 检查
