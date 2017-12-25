from kq.window_utils import get_control_window, get_board_window, get_pot_money_window
from kq.control_utils import get_controls
from kq.money_utils import get_pot_money
from kq.card_utils import get_card_list


def check_if_turn2move(full_window):
    turn2move = False
    player_control_window = get_control_window(full_window)
    player_control_list = get_controls(player_control_window)
    if len(player_control_list) > 1:
        turn2move = True
    return turn2move


def check_should_call(my_win, my_lose, pot_money, money_this_hand, call_money=0):
    s_call = False
    if my_win > my_lose:
        s_call = True
    else:
        ev = ((pot_money + call_money) * my_win - call_money * my_lose) / 100
        print('money spend in this hand: {}, ev: {}'.format(money_this_hand, ev))
        if ev > money_this_hand:
            s_call = True
    return s_call


def get_board_info(full_window):
    board_window = get_board_window(full_window)
    pot_money_window = get_pot_money_window(full_window)
    pot_money = get_pot_money(pot_money_window)
    board_cards = get_card_list(board_window)
    return board_cards, pot_money


def get_board_status(board_cards):
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