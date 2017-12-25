import os
import cv2


def get_full_game_window(img='../tmp/tmp.png'):
    """
    :param img:
    :return: full game window, gray type
    """
    os.system("screencapture -m -R 0,22,1174,852 {}".format(img))
    full_game_window = cv2.imread(img, 0)
    return full_game_window


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
    pot_money_window = full_window[pot_money_window_start_y:pot_money_window_end_y,
                                   pot_money_window_start_x:pot_money_window_end_x]
    return pot_money_window


def get_player_window(full_window, position):
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


def get_call_money_window(full_window):
    call_money_window_start_x = 1100
    call_money_window_start_y = 1420
    call_money_window_end_x = 1300
    call_money_window_end_y = 1460
    call_money_window = full_window[call_money_window_start_y:call_money_window_end_y,
                                    call_money_window_start_x:call_money_window_end_x]
    return call_money_window

