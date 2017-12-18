import cv2
import numpy as np
from PIL import ImageGrab
import os
import pyautogui
import time


def process_img(original_img):
    processed_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    return processed_img


count = 0
while True:
    # PIL.ImageGrab is too slow, about 0.3s
    # found solution https://stackoverflow.com/questions/44140586/imagegrab-grab-method-is-too-slow, 0.1s
    screenshot = 'tmp_screenshot.png'
    os.system("screencapture -R 0,46,791,548 {}".format(screenshot))
    im = cv2.imread(screenshot, 0)
    cv2.imwrite('poker/{}.png'.format(count), im)
    count += 1
    # window = (0, 46, 791, 588)
    # im = np.array(ImageGrab.grab(bbox=window))
    # processed_screen = process_img(im)
    time.sleep(10)
    # cv2.imshow('window', im)
    # if cv2.waitKey(25) & 0xFF == ord('q'):
    #     cv2.destroyAllWindows()
    #     break
