import cv2
import os
import time

count = 0
while True:
    # PIL.ImageGrab is too slow, about 0.3s
    # found solution https://stackoverflow.com/questions/44140586/imagegrab-grab-method-is-too-slow, 0.1s
    screenshot = 'tmp_screenshot.png'
    # # for mbp-cisco
    # os.system("screencapture -R 0,46,791,548 {}".format(screenshot))

    # for my mac
    os.system("screencapture -R 0,22,794,591 {}".format(screenshot))
    im = cv2.imread(screenshot, 0)
    cv2.imwrite('poker/{}.png'.format(count), im)
    count += 1
    time.sleep(4)
    #     break
