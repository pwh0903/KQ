import cv2
import numpy as np

from kq.window_utils import get_player_window
from kq.money_utils import get_player_money
from kq.card_utils import get_card_list


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
            my_status = 'Middle'
        elif me_button == 4:
            my_status = 'Big_Blind'
        elif me_button == 5:
            my_status = 'Small_Blind'

    return my_status, opponent_info
