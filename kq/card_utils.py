import os
import cv2
import numpy as np


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
