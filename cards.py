import cv2
import numpy as np
import os


def get_card_list(cards_window):
    cards_list = []
    imgs = os.listdir('cards')
    for img in imgs:
        if not img.endswith('png'):
            continue
        file_name, file_extension = os.path.splitext(img)
        template = cv2.imread('cards/{}'.format(img), 0)
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
        pool_window = im[int(31*h/96):int(39*h/96), int(w/3): int(2*w/3)]
        card_list = get_card_list(pool_window)
        print(card_list)
        cv2.imshow('card_window', im)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

