import os
import cv2
import numpy as np

from kq.window_utils import get_call_money_window, get_player_window


def get_pot_money(pot_money_window):
    """
    :param pot_money_window:
    :return: pot money
    """
    dot_name = 'dot'
    img_folder = '../pot_number'
    nums_list = dict()
    pot_money = -1
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
            pot_money = float(parsed_number) / 10 ** count
        else:
            pot_money = float(parsed_number)
    except Exception as e:
        pass
    return pot_money


def get_player_money(player_window):
    """
    :param player_window:
    :return: player money
    """
    player_money = -1
    dot_name = 'dot'
    img_folder = '../player_money_number'
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


def get_call_money(full_window):
    """
    :param full_window:
    :return: call money
    """
    call_money_window = get_call_money_window(full_window)
    c_money = get_player_money(call_money_window)
    return c_money
