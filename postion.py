import numpy as np
import cv2
import os


def get_button_postion(full_window):
    ret, full = cv2.threshold(full_window, 180, 255, cv2.THRESH_BINARY)
    template = cv2.imread('postion/button.png', 0)
    res = cv2.matchTemplate(full, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.9
    h, w = np.where(res >= threshold)
    if 880 < w < 980 and 640 < h < 710:
        button_p = 0
    elif 375 < w < 445 and 575 < h < 635:
        button_p = 1
    elif 480 < w < 560 and 620 < h < 680:
        button_p = 1
    elif 325 < w < 395 and 310 < h < 370:
        button_p = 2
    elif 270 < w < 350 and 380 < h < 460:
        button_p = 2
    elif 645 < w < 710 and 205 < h < 265:
        button_p = 3
    elif 335 < w < 405 and 305 < h < 375:
        button_p = 3
    elif 1215 < w < 1285 and 320 < h < 380:
        button_p = 4
    elif 545 < w < 615 and 220 < h < 280:
        button_p = 4
    elif 1145 < w < 1215 and 575 < h < 635:
        button_p = 5
    elif 1000 < w < 1080 and 220 < h < 280:
        button_p = 5
    elif 1190 < w < 1260 and 310 < h < 375:
        button_p = 6
    elif 1240 < w < 1320 and 380 < h < 450:
        button_p = 7
    elif 1050 < w < 1150 and 600 < h < 670:
        button_p = 8
    print(button_p)
    return button_p


def get_player_postion(full_window):
    player_p = 0
    ret, full = cv2.threshold(full_window, 70, 255, cv2.THRESH_BINARY)
    template = cv2.imread('postion/me.png', 0)
    res = cv2.matchTemplate(full, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.7
    h, w = np.where(res >= threshold)
    print(h, w)
    w = w[0]
    h = h[0]
    if 745 < w < 820 and 760 < h < 790:
        player_p = 0
    elif 80 < w < 140 and 575 < h < 600:
        player_p = 1
    elif 70 < w < 120 and 230 < h < 250:
        player_p = 2
    elif 660 < w < 720 and 95 < h < 115:
        player_p = 3
    elif 1340 < w < 1390:
        if 230 < h < 245:
            player_p = 4
        elif 575 < h < 590:
            player_p = 5
    print(player_p)
    return player_p


if __name__ == '__main__':
    test_imgs = os.listdir('poker')
    for img in test_imgs:
        print(img)
        if not img.endswith('png'):
            continue
        im = cv2.imread('poker/{}'.format(img), 0)
        # get_button_postion(im)
        get_player_postion(im)
        # ret, im = cv2.threshold(im, 80, 255, cv2.THRESH_BINARY)
        cv2.imshow('card_window', im)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


# im = cv2.imread('t.png', 0)
# print(im[30])
# ret, im = cv2.threshold(im, 100, 255, cv2.THRESH_BINARY)
# r_start = 0
# for i in im:
#     if np.sum(i) == 0:
#         r_start += 1
#     else:
#         break
#
# im = im[r_start:]
#
# r_end = 0
# for i in im:
#     if np.sum(i) != 0:
#         r_end += 1
#     else:
#         break
#
# im = im[:r_end]
# c_start = 0
# for c in im.T:
#     if np.sum(c) == 0:
#         c_start += 1
#     else:
#         break
# im = im[:, c_start:]
#
# c_end = 0
# for c in im.T[::-1]:
#     print(c)
#     if np.sum(c) == 0:
#         c_end += 1
#     else:
#         break
# print(c_end)
# im = im[:, :-c_end]

# cv2.imwrite('postion/me.png', im)
# #
# cv2.imshow('card_window', im)
# cv2.waitKey(0)
# cv2.destroyAllWindows()