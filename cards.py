import cv2
import numpy as np
import os


def get_card_list(cards_window):
    cards_list = []
    cards_folder = 'cards'
    imgs = os.listdir(cards_folder)
    for img in imgs:
        if not img.endswith('.PNG'):
            continue
        file_name, file_extension = os.path.splitext(img)
        template = cv2.imread('{}/{}'.format(cards_folder, img), 0)
        res = cv2.matchTemplate(cards_window, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.99
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


if __name__ == '__main__':
    test_imgs = os.listdir('poker')
    for img in test_imgs:
        print(img)
        if not img.endswith('png'):
            continue
        im = cv2.imread('poker/{}'.format(img), 0)
        h, w = im.shape
        # pool_window = im
        board_window_start_x = 255
        board_window_start_y = 170
        board_window_w = 282
        board_window_h = 49
        board_window = im[board_window_start_y:board_window_start_y+board_window_h,
                          board_window_start_x:board_window_start_x+board_window_w]
        card_list = get_card_list(board_window)
        print(card_list)
        cv2.imshow('b', board_window)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


