import cv2
import numpy as np
import os


# get options from option window
def get_options(option_img):
    print(option_img.shape)
    options_list = []
    imgs = os.listdir('controls')
    for img in imgs:
        if not img.endswith('png'):
            continue
        file_name, file_extension = os.path.splitext(img)
        template = cv2.imread('controls/{}'.format(img), 0)
        print(template.shape)
        res = cv2.matchTemplate(option_img, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.7
        loc = np.where(res >= threshold)
        a1, a2 = loc
        if len(a1) > 0 and len(a2) > 0:
            options_list.append(file_name)
    return options_list


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
        if not img.endswith('png'):
            continue
        im = cv2.imread('poker/{}'.format(img), 0)
        control_window_start_h = 860
        control_window_h = 320
        control_window_start_w = 750
        control_window_w = 820
        control_window = im[control_window_start_h:control_window_start_h+control_window_h,
                         control_window_start_w:control_window_start_w+control_window_w]
        # option_window = cv2.imread('options.png', 0)
        option_list = get_options(control_window)
        print(option_list)
        cv2.imshow('option_window', control_window)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# get option screenshot and save them
# print(option_window.shape)
# h, w = option_window.shape

# check = option_window[-int(h/2):-int(h/6), int(w/3):int(2*w/3)]
# bet = option_window[-int(h/2):-int(h/4), int(2*w/3):]
# half_pot = option_window[:int(h/5), int(w/2):int(2*w/3)]
# fold = option_window[-int(h/2):-int(h/6), :int(w/3)]
# call = option_window[-int(h/2):-int(h/4), int(w/3):int(2*w/3)]
# raise_to = option_window[-int(h/2):-int(h/4), int(2*w/3):]
# min_bet = option_window[:int(h/5), int(w/3):int(w/2)]
# three_bet = option_window[:int(h/5), int(w/2):int(2*w/3)]
# pot_bet = option_window[:int(h/5), int(2*w/3):int(5*w/6)]
# max_bet = option_window[:int(h/5), int(5*w/6):]
# slider = option_window[int(h/5):int(h/2), int(w/3):]

# cv2.imwrite('options/fold.png', fold)
# cv2.imwrite('options/call.png', call)
# cv2.imwrite('options/raise_to.png', raise_to)
# cv2.imwrite('options/min_bet.png', min_bet)
# cv2.imwrite('options/three_bet.png', three_bet)
# cv2.imwrite('options/pot_bet.png', pot_bet)
# cv2.imwrite('options/max_bet.png', max_bet)
# cv2.imwrite('options/slider.png', slider)
# cv2.imwrite('options/check.png', check)
# cv2.imwrite('options/half_pot.png', half_pot)
# cv2.imwrite('options/bet.png', bet)

