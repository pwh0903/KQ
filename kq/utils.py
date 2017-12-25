import numpy as np
import cv2
import time
import os


def cut_blank(im):
    """
    :param im: image need to cut, must be binary value mode
    :return: cut image
    """
    r_start = 0
    for i in im:
        if np.sum(i) == 0:
            r_start += 1
        else:
            break
    # im = im[r_start:]
    r_end = 0
    for i in im[::-1]:
        if np.sum(i) == 0:
            r_end -= 1
        else:
            break
    # im = im[:r_end]
    c_start = 0
    for c in im.T:
        if np.sum(c) == 0:
            c_start += 1
        else:
            break
    # im = im[:, c_start:]
    c_end = 0
    for c in im.T[::-1]:
        if np.sum(c) == 0:
            c_end -= 1
        else:
            break
    # im = im[:, :c_end]
    im = im[r_start:r_end, c_start:c_end]
    return im


def take_screenshot():
    """
    take screenshot and save it as gray
    """
    count = 0
    screenshot = 'tmp_screenshot.png'
    while True:
        # PIL.ImageGrab is too slow, about 0.3s
        # found solution https://stackoverflow.com/questions/44140586/imagegrab-grab-method-is-too-slow, 0.1s
        os.system("screencapture -R 0,22,1174,852 {}".format(screenshot))
        im = cv2.imread(screenshot, 0)
        cv2.imwrite('poker/{}.png'.format(count), im)
        count += 2
        time.sleep(4)


def get_card_list(cards_window):
    """
    :param cards_window: window contains cards in it
    :return: card list ['As', 'Ac']
    """
    cards_list = []
    cards_folder = 'cards'
    imgs = os.listdir(cards_folder)
    for img in imgs:
        if not img.endswith('.png'):
            continue
        file_name, file_extension = os.path.splitext(img)
        template = cv2.imread('{}/{}'.format(cards_folder, img), 0)
        res = cv2.matchTemplate(cards_window, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.95
        loc = np.where(res >= threshold)
        row, col = loc
        if len(row) > 0 and len(col) > 0:
            start_c = 0
            for c in col:
                diff_c = c - start_c
                if diff_c < 12:
                    start_c = c
                    continue
                start_c = c
            cards_list.append(file_name)
    return cards_list
