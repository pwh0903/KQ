import numpy as np
import cv2
import os


def get_player_window(full_window, postion):
    # money_window_h = 70
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
    # money_window = full_window[player_window_h_start+player_window_h-money_window_h:player_window_h_start+player_window_h,
    #                             player_window_w_start:player_window_w_start+player_window_w]
    return player_window    #money_window


def get_money(player_window):
    money = -1

    return money


if __name__ == '__main__':
    my_name = cv2.imread('positions/name.png', 0)
    button = cv2.imread('positions/button.png', 0)
    card_back = cv2.imread('positions/card_back.png', 0)

    test_imgs = os.listdir('poker')
    for img in test_imgs:
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

            threshold = 0.7
            # check if this player is playing now
            card_back_res = cv2.matchTemplate(player_window, card_back, cv2.TM_CCOEFF_NORMED)
            h, w = np.where(card_back_res >= threshold)
            if len(h) > 0 and len(w) > 0:
                opp_money = get_money(player_window)
                opponent_info[i] = opp_money

            # check my position
            my_res = cv2.matchTemplate(player_window, my_name, cv2.TM_CCOEFF_NORMED)
            h, w = np.where(my_res >= threshold)
            if len(h) > 0 and len(w) > 0:
                my_postion = i
                my_money = get_money(player_window)

            # check button position
            button_res = cv2.matchTemplate(player_window, button, cv2.TM_CCOEFF_NORMED)
            h, w = np.where(button_res >= threshold)
            if len(h) > 0 and len(w) > 0:
                button_postion = i

        print('my_p: {}, button_p: {}, opp_p: {}'.format(my_postion, button_postion, opponent_info))

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