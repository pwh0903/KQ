import time

from kq.decision import check_if_turn2move, get_board_info, get_board_status, check_should_call, check_card_equity
from kq.window_utils import get_full_game_window
from kq.position_utils import get_position_info
from kq.money_utils import get_call_money


if __name__ == '__main__':
    print('Start new game...')

    big_blind = 6.0
    small_blind = big_blind / 2

    # total game statistic
    total_hand = 0
    win_hand = 0
    lose_hand = 0
    equal_hand = 0
    profit = 0

    new_hand_start = True
    len_board_cards_last_bet = 0

    my_money_start = big_blind * 100
    my_money_last_hand = my_money_start
    my_money_last_bet = my_money_last_hand
    my_cards_last_hand = None
    button_position_last_hand = None

    # start poker bot
    while True:
        full_game_window = get_full_game_window()

        # 1. get control list, if no controls, not my turn
        # continue to my turn
        turn2move, control_list = check_if_turn2move(full_game_window)
        if not turn2move:
            continue

        # get all players' window from full screenshot
        # get players' hand cards, money, position
        my_position, my_cards, my_money, button_position, opponent_info = get_position_info(full_game_window)
        my_cards_str = ''.join(my_cards)
        if my_cards_last_hand != my_cards_str and button_position != button_position_last_hand and total_hand != 0:
            new_hand_start = True
            total_hand += 1

        # if can't get opponent's money, wait for 1.2s, start a new screenshot
        wait_s = False
        for op in opponent_info:
            if opponent_info[op] == -1:
                wait_s = True
                break
        if wait_s:
            time.sleep(1.2)
            continue

        # get board money, board cards
        board_cards, pot_money = get_board_info(full_game_window)

        # check which phrase in this hand
        board_status = get_board_status(board_cards)

        call_money = 0
        if 'call' in control_list:
            call_money = get_call_money(full_game_window)

        # save my new hand start status for new hand
        if new_hand_start:
            if total_hand != 0:
                my_money_last_hand = my_money
                profit = my_money - my_money_start
                win_lose = my_money - my_money_last_hand
                if win_lose < 0:
                    lose_hand += 1
                elif win_lose > 0:
                    win_hand += 1
                else:
                    equal_hand += 1
            print('==========Total Hand {}, win: {}, lose: {},equal: {}, profit: {}=========='\
                  .format(total_hand, win_hand, lose_hand, equal_hand, profit))
            print('Player in position {}'.format(my_position))
            # save this hand's info as history, set new hand false
            my_cards_last_hand = my_cards_str
            new_hand_start = False

        print('==============={}==============='.format(board_status))
        print('Board Cards: {}'.format(board_cards))
        print('My cards: {}'.format(my_cards))
        if len(board_cards) > 1:
            board_cards_str = ''.join(board_cards)
            my_win, my_lose = check_card_equity(my_cards_str, board_cards_str)
            money_this_hand = my_money_last_hand - my_money
            should_call = check_should_call(my_win, my_lose, pot_money, call_money)
            print('My winning percentage: {}'.format(my_win))
            print('Call money: {}'.format(call_money))
            print('Should Call: {}'.format(should_call))
        # print('Pot money: {}'.format(pot_money))
        # print('My money: {}'.format(my_money))
        # print('Available controls: {}'.format(control_list))

        # make_controls(player_win, pot_money, control_list)
        time.sleep(5)

