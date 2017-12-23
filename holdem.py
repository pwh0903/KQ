import cv2
import numpy as np
import subprocess
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


def get_control_window(full_window):
    control_window_start_x = 145
    control_window_start_y = 465
    control_window_w = 510
    control_window_h = 105
    control_window = full_window[control_window_start_y:control_window_start_y+control_window_h,
                     control_window_start_x:control_window_start_x+control_window_w]
    return control_window


def get_board_window(full_window):
    board_window_start_x = 255
    board_window_start_y = 170
    board_window_w = 282
    board_window_h = 49
    board_window = full_window[board_window_start_y:board_window_start_y + board_window_h,
                   board_window_start_x:board_window_start_x + board_window_w]
    return board_window


def get_player_window(full_window, postion):
    if postion == 0:
        player_window_x = 420
        player_window_y = 305

        player_window_w = 185
        player_window_h = 125

    elif postion == 1:
        player_window_x = 185
        player_window_y = 305

        player_window_w = 185
        player_window_h = 125

    elif postion == 3:
        player_window_x = 185
        player_window_y = 35

        player_window_w = 180
        player_window_h = 125

    elif postion == 4:
        player_window_x = 420
        player_window_y = 35

        player_window_w = 185
        player_window_h = 125

    elif postion == 2:
        player_window_x = 5
        player_window_y = 185

        player_window_w = 240
        player_window_h = 85

    elif postion == 5:
        player_window_x = 550
        player_window_y = 185

        player_window_w = 240
        player_window_h = 85

    player_window = full_window[player_window_y:player_window_y+player_window_h,
                                player_window_x:player_window_x+player_window_w]
    return player_window


def get_position_info(full_window):
    my_name = cv2.imread('positions/name.png', 0)
    button = cv2.imread('positions/button.png', 0)
    card_back = cv2.imread('positions/card_back.png', 0)

    my_position = -1
    opponent_info = dict()
    button_position = -1

    # get all 6 player's window
    for i in range(6):
        player_window = get_player_window(im, i)

        threshold = 0.7
        # check if this player is playing now
        card_back_res = cv2.matchTemplate(player_window, card_back, cv2.TM_CCOEFF_NORMED)
        h, w = np.where(card_back_res >= threshold)
        if len(h) > 0 and len(w) > 0:
            opp_info = dict()
            opp_money = get_money(player_window)
            opp_info['money'] = opp_money
            opponent_info[i] = opp_info

        # check my position
        my_res = cv2.matchTemplate(player_window, my_name, cv2.TM_CCOEFF_NORMED)
        h, w = np.where(my_res >= threshold)
        if len(h) > 0 and len(w) > 0:
            my_position = i
            my_money = get_money(player_window)

        # check button position
        button_res = cv2.matchTemplate(player_window, button, cv2.TM_CCOEFF_NORMED)
        h, w = np.where(button_res >= threshold)
        if len(h) > 0 and len(w) > 0:
            button_position = i

        print('my_p: {}, my_money: {}, button_p: {}, opp_p: {}'.format(my_position, my_money, button_position, opponent_info))
        return my_position, my_money, button_position, opponent_info


def parse_position(my_position, button_position, opponent_info):
    my_status = None

    all_player_position = list()
    all_player_position.append(my_position)
    all_player_position.extend(list(opponent_info.keys))
    all_player_position.sort()
    player_nums = len(all_player_position)


    for p in all_player_position:
        p_status = None
        if button_position == my_position:
            my_status = 'Button'
        elif (button_position - my_position) :
            pass

        if p == my_position:
            my_status = p_status

    return my_status, opponent_info


def control_action(control, click_count=1):
    control_map = {
        'fold': (450, 565),
        'call': (590, 565),
        'check': (590, 565),
        'raise': (720, 565),
        'slider': (640, 520),
        'min': (550, 488),
        '3bb': (620, 488),
        'half': (620, 488),
        'pot': (690, 488),
        'max': (750, 488),
    }
    row, col = control_map.get(control)
    click_count = 2
    pyautogui.click(row, col, clicks=click_count, interval=0.2)


def make_controls(player_win, pot_money, control_list):
    pass


if __name__ == '__main__':
    print('Start new game...')

    screenshot = 'tmp/tmp_screenshot.png'

    new_hand = True
    len_board_cards_last_bet = 0
    hand_status = 'PREFLOP'
    player_postion_last = -1

    player_money_start = 10000
    player_money_last_hand = -1
    player_money_last_bet = player_money_last_hand
    player_cards_last_hand = None

    total_hand = 0
    win_hand = 0
    lose_hand = 0
    equal_hand = 0

    while True:
        os.system("screencapture -R 0,46,791,548 {}".format(screenshot))
        im = cv2.imread(screenshot, 0)
        h, w = im.shape

        # get player's window from full screenshot
        # get player's hand cards, money
        player_postion = get_player_postion(im)
        if player_postion < 0:
            # print('Wait for a new game')
            # time.sleep(2)
            continue
        player_window, player_money_window = get_player_window(im, player_postion)
        player_cards = get_card_list(player_window)
        if len(player_cards) < 2 and new_hand:
            # print('Wait for a new hand')
            # time.sleep(10)
            continue
        player_cards_str = ''.join(player_cards)

        player_money = get_money(player_money_window)

        pot_window = im[int(148*h/543): int(165*h/543), int(650*w/1580): int(960*w/1580)]
        pot_money = get_money(pot_window)

        control_window = get_control_window(im)
        control_list = get_controls(control_window)

        board_cards_window = get_board_window(im)
        board_cards = get_card_list(board_cards_window)

        if new_hand:
            if player_money_last_hand == -1:
                total_hand -= 1
            elif player_money < player_money_last_hand:
                lose_hand += 1
            elif player_money > player_money_last_hand:
                win_hand += 1
            else:
                equal_hand += 1
            total_hand += 1
            print('==========New hand {}, win: {}, lose: {},equal: {}, profit: {}=========='.format(total_hand, win_hand,
                                                                                                    lose_hand, equal_hand,
                                                                                          player_money-player_money_start))
            print('Money last hand: {}, money now: {}'.format(player_money_last_hand, player_money))
            # save this hand's info as history, set new hand false
            player_money_last_hand = player_money
            player_cards_last_hand = player_cards
            new_hand = False
            pot_money_last_hand = pot_money

        # # if can call, means someone raise bet
        # if 'call' in control_list:
        #     new_bet = True

        # check if new bet and show control list
        # if len(control_list) > 1 and new_bet:
        if len(control_list) > 1:
            # get board window from full screenshot
            # get board cards, money
            if len(board_cards) < 2:
                hand_status = 'PREFlOP'
                # new_bet = False
            elif len(board_cards) == 3:
                hand_status = 'FlOP'
                # new_bet = False
            elif len(board_cards) == 4:
                hand_status = 'TURN'
                # new_bet = False
            elif len(board_cards) == 5:
                hand_status = 'RIVER'
                # new_bet = False

            print('Player in postion {}'.format(player_postion))
            print('==============={}==============='.format(hand_status))
            print('Board Cards: {}'.format(board_cards))
            print('My cards: {}'.format(player_cards))
            if len(board_cards) > 1:
                board_cards_str = ''.join(board_cards)
                print(player_cards_str, board_cards_str)
                output = subprocess.check_output('ps-eval {} --board {}'.format(player_cards_str, board_cards_str), shell=True)
                output = output.decode('utf-8')
                player_win = float(output.split('\n')[0].split('%')[0].strip().split(' ')[-1])
                other_win = float(output.split('\n')[1].split('%')[0].strip().split(' ')[-1])
                print('My winning percentage: {}'.format(player_win))
            print('Pot money: {}'.format(pot_money))
            print('My money: {}'.format(player_money))
            print('Available controls: {}'.format(control_list))

            make_controls(player_win, pot_money, control_list)
            time.sleep(5)

        if len(player_cards) < 2:
            new_hand = True
