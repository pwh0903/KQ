import pyautogui
import cv2
import os
import numpy as np

from kq.window_utils import get_control_window


def get_controls(full_window):
    """
    :param full_window:
    :return: control list
    """
    control_window = get_control_window(full_window)

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


