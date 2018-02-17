import time

from kq.decision import get_board_info, get_board_status, check_should_call, check_card_equity
from kq.window_utils import get_full_game_window, get_control_window
from kq.position_utils import get_position_info
from kq.money_utils import get_call_money
from kq.common_utils import get_logger
from kq.control_utils import get_controls


def main(bb, buy_in):
    log = get_logger()
    log.info('Start new game...')

    # init game status
    total_hand = 0
    win_hand = 0
    lose_hand = 0
    equal_hand = 0

    # money status
    my_money_last_hand = buy_in
    bb_count = buy_in // bb
    my_profit = 0

    # some tags, used to check if this hand is new hand
    new_hand = True
    my_cards_last_hand = None
    button_position_last_hand = None

    # start poker bot
    while True:
        full_game_window = get_full_game_window()

        # 1. get control list, if no controls, not my turn
        # continue loop until I can control
        control_window = get_control_window(full_game_window)
        control_list = get_controls(control_window)
        if len(control_list) < 2:
            log.info("Wait for my move, sleep 2s")
            time.sleep(2)
            continue

        # get all players' window from full screenshot
        # get players' hand cards, money, position
        my_position, my_cards, my_money, button_position, opponent_info = get_position_info(full_game_window)
        my_cards_str = ''.join(my_cards)

        # if can't get opponent's money, wait for 0.5s, start a new screenshot
        wait_s = False
        for op in opponent_info:
            if opponent_info[op] == -1:
                wait_s = True
                break
        if wait_s:
            time.sleep(0.5)
            continue

        # check if this hand is new hand
        if my_cards_last_hand != my_cards_str and button_position != button_position_last_hand:
            if my_cards_last_hand:
                new_hand = True
                total_hand += 1

        # get board money, board cards
        board_cards, pot_money = get_board_info(full_game_window)

        # check which phrase in this hand
        board_status = get_board_status(board_cards)

        call_money = 0
        if 'call' in control_list:
            call_money = get_call_money(full_game_window)

        # save my new hand start status for new hand
        if new_hand:
            if total_hand != 0:
                my_money_last_hand = my_money
                my_profit = my_money - buy_in
                win_lose = my_money - my_money_last_hand
                if win_lose < 0:
                    lose_hand += 1
                elif win_lose > 0:
                    win_hand += 1
                else:
                    equal_hand += 1
            log.info('==========Total Hand {}, win: {}, lose: {},equal: {}, profit: {}=========='.format(total_hand, win_hand, lose_hand, equal_hand, my_profit))
            log.info('Player in position {}'.format(my_position))
            # save this hand's info as history, set new hand false
            my_cards_last_hand = my_cards_str
            new_hand = False

        log.info('==============={}==============='.format(board_status))
        log.info('Board Cards: {}'.format(board_cards))
        log.info('My cards: {}'.format(my_cards))
        if len(board_cards) > 1:
            board_cards_str = ''.join(board_cards)
            my_win, my_lose = check_card_equity(my_cards_str, board_cards_str)
            money_this_hand = my_money_last_hand - my_money
            should_call = check_should_call(my_win, my_lose, pot_money, call_money)
            log.info('My winning percentage: {}'.format(my_win))
            log.info('Call money: {}'.format(call_money))
            log.info('Should Call: {}'.format(should_call))
        # print('Pot money: {}'.format(pot_money))
        # print('My money: {}'.format(my_money))
        # print('Available controls: {}'.format(control_list))
        # make_controls(player_win, pot_money, control_list)


if __name__ == "__main__":
    main(bb=6.0)
