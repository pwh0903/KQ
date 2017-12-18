import cv2
import numpy as np
from PIL import ImageGrab
import os
import pyautogui
import time


# get options from option window
def get_controls(option_img):
    control_list = []
    control_folder = 'controls'
    imgs = os.listdir(control_folder)
    for img in imgs:
        if not img.endswith('png'):
            continue
        file_name, file_extension = os.path.splitext(img)
        template = cv2.imread('{}/{}'.format(control_folder, img), 0)
        res = cv2.matchTemplate(option_img, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        row, col = loc
        if len(row) > 0 and len(col) > 0:
            control_list.append(file_name)
    return control_list


def get_card_list(cards_window):
    cards_list = []
    cards_folder = 'cards'
    imgs = os.listdir(cards_folder)
    for img in imgs:
        if not img.endswith('png'):
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


def get_button_postion(full_window):
    postion_folder = 'postion'
    ret, full = cv2.threshold(full_window, 180, 255, cv2.THRESH_BINARY)
    template = cv2.imread('{}/button.png'.format(postion_folder), 0)
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
    postion_folder = 'postion'
    player_p = -1
    ret, full = cv2.threshold(full_window, 70, 255, cv2.THRESH_BINARY)
    template = cv2.imread('{}/me.png'.format(postion_folder), 0)
    res = cv2.matchTemplate(full, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.7
    try:
        h, w = np.where(res >= threshold)
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
    except Exception as e:
        pass
    return player_p


def get_money(window):
    numbers_dir = 'numbers'
    money = ''
    nums_list = dict()
    ret, window = cv2.threshold(window, 100, 255, cv2.THRESH_BINARY)
    imgs = os.listdir(numbers_dir)
    for img in imgs:
        if not img.endswith('png'):
            continue
        file_name, file_extension = os.path.splitext(img)
        template = cv2.imread('{}/{}'.format(numbers_dir, img), 0)
        res = cv2.matchTemplate(window, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.82
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
                nums_list[c] = file_name
    num_position = [p for p in nums_list]
    num_position.sort()
    for p in num_position:
        if nums_list[p] in ['comma', 'dot']:
            continue
        money += nums_list[p]
    try:
        money = float(money)
    except Exception as e:
        money = None
    return money


def get_player_window(full_window, postion):
    player_window_h = 210
    player_window_w = 350
    money_window_h = 70
    if postion == 0:
        player_window_h_start = 660
        player_window_w_start = 620
    elif postion == 1:
        player_window_h_start = 460
        player_window_w_start = 30
    elif postion == 2:
        player_window_h_start = 110
        player_window_w_start = 30
    elif postion == 3:
        player_window_h_start = 15
        player_window_w_start = 620
    elif postion == 4:
        player_window_h_start = 120
        player_window_w_start = 1200
    elif postion == 5:
        player_window_h_start = 460
        player_window_w_start = 1200
    player_window = full_window[player_window_h_start:player_window_h_start+player_window_h,
                                player_window_w_start:player_window_w_start+player_window_w]
    money_window = full_window[player_window_h_start+player_window_h-money_window_h:player_window_h_start+player_window_h,
                                player_window_w_start:player_window_w_start+player_window_w]
    return player_window, money_window


def get_control_window(full_window):
    control_window_start_h = 860
    control_window_h = 320
    control_window_start_w = 750
    control_window_w = 820
    control_window = full_window[control_window_start_h:control_window_start_h+control_window_h,
                     control_window_start_w:control_window_start_w+control_window_w]
    return control_window


if __name__ == '__main__':
    screenshot = 'tmp_screenshot.png'
    new_hand = True
    hand_status = 'PREFLOP'
    player_postion_last = -1

    player_money_start = 10000.0
    player_money_last_hand = player_money_start
    player_money_last_bet = player_money_last_hand
    player_cards_last_hand = None

    total_hand = 1.0
    win_hand = 0.0
    lose_hand = 0.0

    while True:
        os.system("screencapture -R 0,46,791,548 {}".format(screenshot))
        im = cv2.imread(screenshot, 0)
        h, w = im.shape

        # get player's window from full screenshot
        # get player's hand cards, money
        player_postion = get_player_postion(im)
        if player_postion < 0:
            print('Wait for a new game')
            time.sleep(2)
            continue
        player_window, player_money_window = get_player_window(im, player_postion)
        player_cards = get_card_list(player_window)
        if len(player_cards) < 2 and new_hand == True:
            print('Wait for a new hand')
            time.sleep(2)
            continue
        player_money = get_money(player_money_window)

        # get board window from full screenshot
        # get board cards, money
        board_cards_window = im[int(31*h/96):int(39*h/96), int(w/3): int(2*w/3)]
        board_cards = get_card_list(board_cards_window)
        if len(board_cards) < 2:
            hand_status = 'PREFlOP'
        elif len(board_cards) == 3:
            hand_status = 'FlOP'
        elif len(board_cards) == 4:
            hand_status = 'TURN'
        elif len(board_cards) == 5:
            hand_status = 'RIVER'

        pot_window = im[int(148*h/543): int(165*h/543), int(650*w/1580): int(960*w/1580)]
        pot_money = get_money(pot_window)

        control_window = get_control_window(im)
        control_list = get_controls(control_window)

        if len(control_list) > 1:
            if player_money != player_money_last_hand and player_cards != player_cards_last_hand:
                print('==========New hand {}, win: {}, lose: {}, profit: {}=========='.format(total_hand, win_hand, lose_hand,
                                                                                              player_money-player_money_start))
                player_money_last_hand = player_money
                player_cards_last_hand = player_cards
                new_hand = False
            print('Player in postion {}'.format(player_postion))
            print('==============={}==============='.format(hand_status))
            print('Board Cards: {}'.format(board_cards))
            print('My cards: {}'.format(player_cards))
            print('Pot money: {}'.format(pot_money))
            print('My money: {}'.format(player_money))
            print('Available controls: {}'.format(control_list))

        if len(player_cards) < 2:
            new_hand += 1
            new_hand = True

            if player_money:
                if player_money < player_money_last_hand:
                    lose_hand += 1
                else:
                    win_hand += 1
            total_hand += 1

            player_money_last_hand = player_money

        time.sleep(2)

