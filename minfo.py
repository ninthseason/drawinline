import time

import pyautogui as ag

print("屏幕大小", ag.size())
print("鼠标位置", ag.position())

while True:
    print("鼠标位置", ag.position())
    time.sleep(2)

