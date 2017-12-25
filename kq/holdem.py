import cv2
import numpy as np
import subprocess
import os
import pyautogui
import time


def get_controls(control_window):
    """
    :param control_window:
    :return: control list
    """
    control_list = []
    imgs = os.listdir('controls')
    for img in imgs:
        if not img.endswith('png'):
            continue
        file_name, file_extension = os.path.splitext(img)
        template = cv2.imread('controls/{}'.format(img), 0)
        res = cv2.matchTemplate(control_window, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        a1, a2 = loc
        if len(a1) > 0 and len(a2) > 0:
            control_list.append(file_name)
    return control_list


def get_card_list(cards_window):
    """
    :param cards_window:
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


def get_pot_money(pot_money_window):
    """
    :param board_window:
    :return: board money, float
    """
    dot_name = 'dot'
    img_folder = 'pot_number'
    nums_list = dict()
    board_money = -1
    imgs = os.listdir(img_folder)
    for img in imgs:
        if not img.endswith('.png'):
            continue
        file_name, file_extension = os.path.splitext(img)
        template = cv2.imread('{}/{}'.format(img_folder, img), 0)
        res = cv2.matchTemplate(pot_money_window, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.95
        loc = np.where(res >= threshold)
        row, col = loc
        if len(row) > 0 and len(col) > 0:
            start_c = 0
            for c in col:
                diff_c = c - start_c
                if diff_c < 5:
                    start_c = c
                    continue
                start_c = c
                nums_list[c] = file_name
    num_position = [p for p in nums_list]
    num_position.sort()
    parsed_number = ''

    # find dot position in numbers
    find_dot = False
    count = 0
    for p in num_position[::-1]:
        if nums_list[p] == dot_name:
            find_dot = True
            continue
        if not find_dot:
            count += 1

    for p in num_position:
        if nums_list[p] == dot_name:
            continue
        parsed_number += nums_list[p]
    try:
        if find_dot:
            board_money = float(parsed_number) / 10 ** count
        else:
            board_money = float(parsed_number)
    except Exception as e:
        pass
    return board_money


def get_player_money(player_window):
    """
    :param player_window:
    :return: player money
    """
    player_money = -1
    dot_name = 'dot'
    img_folder = 'player_money_number'
    nums_list = dict()
    imgs = os.listdir(img_folder)
    for img in imgs:
        if not img.endswith('.png'):
            continue
        file_name, file_extension = os.path.splitext(img)
        template = cv2.imread('{}/{}'.format(img_folder, img), 0)
        res = cv2.matchTemplate(player_window, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.95
        loc = np.where(res >= threshold)
        row, col = loc
        if len(row) > 0 and len(col) > 0:
            start_c = 0
            for c in col:
                diff_c = c - start_c
                if diff_c < 5:
                    start_c = c
                    continue
                start_c = c
                nums_list[c] = file_name
    num_position = [p for p in nums_list]
    num_position.sort()
    parsed_number = ''

    # find dot position in numbers
    find_dot = False
    count = 0
    for p in num_position[::-1]:
        if nums_list[p] == dot_name:
            find_dot = True
            continue
        if not find_dot:
            count += 1

    for p in num_position:
        if nums_list[p] == dot_name:
            continue
        parsed_number += nums_list[p]
    try:
        if find_dot:
            player_money = float(parsed_number) / 10 ** count
        else:
            player_money = float(parsed_number)
    except Exception as e:
        pass
    return player_money


def get_control_window(full_window):
    control_start_x = 140
    control_start_y = 1370
    control_end_x = 1930
    control_end_y = 1650
    control_window = full_window[control_start_y:control_end_y, control_start_x:control_end_x]
    return control_window


def get_board_window(full_window):
    board_window_start_x = 770
    board_window_start_y = 480
    board_window_end_x = 1560
    board_window_end_y = 590
    board_window = full_window[board_window_start_y:board_window_end_y,
                               board_window_start_x:board_window_end_x]
    return board_window


def get_pot_money_window(full_window):
    pot_money_window_start_x = 1000
    pot_money_window_start_y = 435
    pot_money_window_end_x = 1360
    pot_money_window_end_y = 475
    pot_money_windo = full_window[pot_money_window_start_y:pot_money_window_end_y,
                   pot_money_window_start_x:pot_money_window_end_x]
    return pot_money_windo


def get_player_window(full_window, position):
    """
    :param full_window:
    :param position:
    :return: player window
    """
    if position == 0:
        player_window_start_x = 1240
        player_window_start_y = 880

        player_window_end_x = 1750
        player_window_end_y = 1290

    elif position == 1:
        player_window_start_x = 540
        player_window_start_y = 880

        player_window_end_x = 1060
        player_window_end_y = 1290

    elif position == 3:
        player_window_start_x = 540
        player_window_start_y = 70

        player_window_end_x = 1060
        player_window_end_y = 460

    elif position == 4:
        player_window_start_x = 1240
        player_window_start_y = 70

        player_window_end_x = 1750
        player_window_end_y = 460

    elif position == 2:
        player_window_start_x = 5
        player_window_start_y = 530

        player_window_end_x = 715
        player_window_end_y = 780

    elif position == 5:
        player_window_start_x = 1640
        player_window_start_y = 530

        player_window_end_x = 2340
        player_window_end_y = 780

    player_window = full_window[player_window_start_y:player_window_end_y,
                                player_window_start_x:player_window_end_x]
    return player_window


def get_position_info(full_window):
    """
    :param full_window:
    :return: my_position, my_cards, my_money, button_position, opponent_info
    """
    my_name = cv2.imread('positions/name.png', 0)
    button = cv2.imread('positions/button.png', 0)
    card_back = cv2.imread('positions/card_back.png', 0)

    my_position = -1
    my_cards = list()
    my_money = -1
    opponent_info = dict()
    button_position = -1

    # get all 6 player's window
    for i in range(6):
        player_window = get_player_window(full_window, i)

        threshold = 0.8
        # check if this player is playing now
        card_back_res = cv2.matchTemplate(player_window, card_back, cv2.TM_CCOEFF_NORMED)
        h, w = np.where(card_back_res >= threshold)
        if len(h) > 0 and len(w) > 0:
            opp_money = get_player_money(player_window)
            opponent_info[i] = opp_money

        # check my position
        my_res = cv2.matchTemplate(player_window, my_name, cv2.TM_CCOEFF_NORMED)
        h, w = np.where(my_res >= threshold)
        if len(h) > 0 and len(w) > 0:
            my_position = i
            my_money = get_player_money(player_window)

            my_cards = get_card_list(player_window)

        # check button position
        button_res = cv2.matchTemplate(player_window, button, cv2.TM_CCOEFF_NORMED)
        h, w = np.where(button_res >= threshold)
        if len(h) > 0 and len(w) > 0:
            button_position = i
    # print('my_cards: {}, my_p: {}, my_money: {}, button_p: {}, opp_p: {}'.format(my_cards, my_postion, my_money, button_postion, opponent_info))
    return my_position, my_cards, my_money, button_position, opponent_info


def parse_position(my_position, button_position, opponent_info):
    """
    :param my_position:
    :param button_position:
    :param opponent_info:
    :return:
    """
    # this part not ready now
    my_status = None

    all_player_position = list()
    all_player_position.append(my_position)
    all_player_position.extend(list(opponent_info.keys))
    all_player_position.sort()
    player_nums = len(all_player_position)

    if button_position in all_player_position and player_nums == 6:
        me_button = button_position - my_position
        if me_button == 0:
            my_status = 'Button'
        elif me_button == 1:
            my_status = 'CO'
        elif me_button == 2:
            my_status = 'LP'
        elif me_button == 3:
            my_status == 'Middle'
        elif me_button == 4:
            my_status = 'Big_Blind'
        elif me_button == 5:
            my_status = 'Small_Blind'

    return my_status, opponent_info


def control_action(control, click_count=1):
    """
    :param control:
    :param click_count:
    :return:
    """
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


def check_if_my_move(full_window):
    on_my_move = False
    player_control_window = get_control_window(full_window)
    player_control_list = get_controls(player_control_window)
    if len(player_control_list) > 1:
        on_my_move = True
    return on_my_move


def get_board_info(full_window):
    board_window = get_board_window(full_window)
    pot_money_window = get_pot_money_window(full_window)
    pot_money = get_pot_money(pot_money_window)
    board_cards = get_card_list(board_window)
    return board_cards, pot_money


def check_board_status(board_cards):
    if len(board_cards) < 2:
        board_status = 'PREFLOP'
        # new_bet = False
    elif len(board_cards) == 3:
        board_status = 'FLOP'
        # new_bet = False
    elif len(board_cards) == 4:
        board_status = 'TURN'
        # new_bet = False
    elif len(board_cards) == 5:
        board_status = 'RIVER'
    return board_status


def get_call_money(full_window):
    call_money_window_start_x = 1100
    call_money_window_start_y = 1420
    call_money_window_end_x = 1300
    call_money_window_end_y = 1460
    call_money_window = full_window[call_money_window_start_y:call_money_window_end_y,
                                    call_money_window_start_x:call_money_window_end_x]
    c_money = get_player_money(call_money_window)
    return c_money


def get_should_call(my_win, my_lose, pot_money, money_this_hand, call_money=0):
    s_call = False
    if my_win > my_lose:
        s_call = True
    else:
        ev = ((pot_money + call_money) * my_win - call_money * my_lose) / 100
        print('money spend in this hand: {}, ev: {}'.format(money_this_hand, ev))
        if ev > money_this_hand:
            s_call = True
    return s_call


if __name__ == '__main__':
    print('Start new game...')

    screenshot = 'tmp/tmp_screenshot.png'

    big_blind = 6.0
    small_blind = big_blind / 2

    # total game statistic
    total_hand = 0
    win_hand = 0
    lose_hand = 0
    equal_hand = 0

    new_hand_start = True
    len_board_cards_last_bet = 0

    my_money_start = 600
    my_money_last_hand = -1
    my_money_last_bet = my_money_last_hand
    my_cards_last_hand = None

    while True:
        os.system("screencapture -m -R 0,22,1174,852 {}".format(screenshot))
        full_game_window = cv2.imread(screenshot, 0)

        # 1. get control list, if no controls, not my turn
        # continue to my turn
        if check_if_my_move(full_game_window):
            pass
        else:
            continue

        # get all players' window from full screenshot
        # get players' hand cards, money, position
        my_position, my_cards, my_money, button_position, opponent_info = get_position_info(full_game_window)
        my_cards_str = ''.join(my_cards)
        if my_cards_last_hand != my_cards_str:
            new_hand_start = True

        # if can't get opponent's money, wait for 2s, start a new screenshot
        wait_2s = False
        for op in opponent_info:
            if opponent_info[op] == -1:
                wait_2s = True
                break
        if wait_2s:
            time.sleep(2)
            continue

        # get board money, board cards
        board_cards, pot_money = get_board_info(full_game_window)

        # check if new bet and show control list
        board_status = check_board_status(board_cards)

        # get controls
        control_window = get_control_window(full_game_window)
        control_list = get_controls(control_window)
        call_money = 0
        if 'call' in control_list:
            call_money = get_call_money(full_game_window)

        # save my new hand start status for new hand
        if new_hand_start:
            profit = my_money - my_money_start
            win_lose = my_money - my_money_last_hand
            if my_money_last_hand == -1:
                total_hand -= 1
            elif win_lose < 0:
                lose_hand += 1
            elif win_lose > 0:
                win_hand += 1
            else:
                equal_hand += 1
            total_hand += 1
            print('==========New hand {}, win: {}, lose: {},equal: {}, profit: {}==========' \
                  .format(total_hand, win_hand, lose_hand, equal_hand, profit))
            print('Player in position {}'.format(my_position))
            # save this hand's info as history, set new hand false
            my_money_last_hand = my_money
            my_cards_last_hand = my_cards_str
            pot_money_last_hand = pot_money
            new_hand_start = False

        print('==============={}==============='.format(board_status))
        print('Board Cards: {}'.format(board_cards))
        print('My cards: {}'.format(my_cards))
        if len(board_cards) > 1:
            board_cards_str = ''.join(board_cards)
            output = subprocess.check_output('ps-eval {} --board {}'.format(my_cards_str, board_cards_str), shell=True)
            output = output.decode('utf-8')
            my_win = float(output.split('\n')[0].split('%')[0].strip().split(' ')[-1])
            my_lose = float(output.split('\n')[1].split('%')[0].strip().split(' ')[-1])
            money_this_hand = my_money_last_hand - my_money
            should_call = get_should_call(my_win, my_lose, pot_money, call_money)
            print('My winning percentage: {}'.format(my_win))
            print('Call money: {}'.format(call_money))
            print('Should Call: {}'.format(should_call))
        # print('Pot money: {}'.format(pot_money))
        # print('My money: {}'.format(my_money))
        # print('Available controls: {}'.format(control_list))

        # make_controls(player_win, pot_money, control_list)
        time.sleep(5)

