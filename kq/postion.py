import numpy as np
import cv2
import os


def get_player_window(full_window, postion):
    if postion == 0:
        player_window_start_x = 1240
        player_window_start_y = 880

        player_window_end_x = 1750
        player_window_end_y = 1290

    elif postion == 1:
        player_window_start_x = 540
        player_window_start_y = 880

        player_window_end_x = 1060
        player_window_end_y = 1290

    elif postion == 3:
        player_window_start_x = 540
        player_window_start_y = 70

        player_window_end_x = 1060
        player_window_end_y = 460

    elif postion == 4:
        player_window_start_x = 1240
        player_window_start_y = 70

        player_window_end_x = 1750
        player_window_end_y = 460

    elif postion == 2:
        player_window_start_x = 5
        player_window_start_y = 530

        player_window_end_x = 715
        player_window_end_y = 780

    elif postion == 5:
        player_window_start_x = 1640
        player_window_start_y = 530

        player_window_end_x = 2340
        player_window_end_y = 780

    player_window = full_window[player_window_start_y:player_window_end_y,
                    player_window_start_x:player_window_end_x]
    return player_window


def get_player_money(player_window):
    money = -1
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
            parsed_number = float(parsed_number) / 10 ** count
        else:
            parsed_number = float(parsed_number)
    except Exception as e:
        parsed_number = None
    return parsed_number

    return money


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
    my_name = cv2.imread('positions/name.png', 0)
    button = cv2.imread('positions/button.png', 0)
    card_back = cv2.imread('positions/card_back.png', 0)

    test_imgs = os.listdir('poker')
    for img in test_imgs:
        my_cards = list()
        my_money = -1
        play_now = False
        my_postion = -1
        opponent_info = dict()
        button_postion = -1
        all_seats = dict()
        print(img)
        if not img.endswith('.png'):
            continue
        im = cv2.imread('poker/{}'.format(img), 0)

        # get all 6 player's window
        for i in range(6):
            player_window = get_player_window(im, i)
            all_seats[i] = player_window
            # cv2.imshow('p', player_window)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

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
                my_postion = i
                my_money = get_player_money(player_window)

                my_cards = get_card_list(player_window)

            # check button position
            button_res = cv2.matchTemplate(player_window, button, cv2.TM_CCOEFF_NORMED)
            h, w = np.where(button_res >= threshold)
            if len(h) > 0 and len(w) > 0:
                button_postion = i

        print('my_cards: {}, my_p: {}, my_money: {}, button_p: {}, opp_p: {}'.format(my_cards, my_postion, my_money, button_postion, opponent_info))

        # ret, im = cv2.threshold(im, 80, 255, cv2.THRESH_BINARY)
        cv2.imshow('card_window', im)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


# im = cv2.imread('t.png', 0)
# print(im[30])
# ret, im = cv2.threshold(im, 100, 255, cv2.THRESH_BINARY)
# r_start = 0
# for i in im:
#     if np.sum(i) == 0:
#         r_start += 1
#     else:
#         break
#
# im = im[r_start:]
#
# r_end = 0
# for i in im:
#     if np.sum(i) != 0:
#         r_end += 1
#     else:
#         break
#
# im = im[:r_end]
# c_start = 0
# for c in im.T:
#     if np.sum(c) == 0:
#         c_start += 1
#     else:
#         break
# im = im[:, c_start:]
#
# c_end = 0
# for c in im.T[::-1]:
#     print(c)
#     if np.sum(c) == 0:
#         c_end += 1
#     else:
#         break
# print(c_end)
# im = im[:, :-c_end]

# cv2.imwrite('postion/me.png', im)
# #
# cv2.imshow('card_window', im)
# cv2.waitKey(0)
# cv2.destroyAllWindows()