import cv2
import numpy as np
import os


def get_card_list(cards_window):
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
    print(cards_list)
    return cards_list


if __name__ == '__main__':
    test_imgs = os.listdir('poker')
    for img in test_imgs:
        print(img)
        if not img.endswith('png'):
            continue
        im = cv2.imread('poker/{}'.format(img), 0)
        board_window_start_x = 770
        board_window_start_y = 480
        board_window_end_x = 1560
        board_window_end_y = 590
        board_window = im[board_window_start_y:board_window_end_y,
                          board_window_start_x:board_window_end_x]
        cards_list = get_card_list(board_window)
        # print(card_list)
        cv2.imshow('b', board_window)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


