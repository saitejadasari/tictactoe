"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def initial_state(board_size):
    """
    Returns starting state of the board.
    """
    return [[EMPTY for j in range(board_size)] for i in range(board_size)]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if terminal(board):
        return EMPTY
    else:
        x = 0
        o = 0
        for row in board:
            for c in row:
                if c == 'X':
                    x += 1
                elif c == 'O':
                    o += 1
                else:
                    continue
        # print("Number of moves by X ", x)
        # print("Number of moves by O ", o)
        if o < x:
            return 'O'
        elif x <= o:
            return 'X'


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_list = set()

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:
                actions_list.add((i, j))

    return actions_list



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # print("board is", board)
    # print("action is", action)
    board_copy = copy.deepcopy(board)
    i, j = action
    if board[i][j] != EMPTY:
        raise Exception
    else:
        player_turn = player(board)
        board_copy[i][j] = player_turn
    # print("new board is", board_copy)
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    board_size = len(board)
    for player in (X, O):
        
        # Horizontal check
        for row in board:
            if row == [player] * board_size:
                return player

        # Vertical check
        for i in range(len(board)):
            win = [player]*board_size
            pos = []
            for j in range(len(board)):
                if board[j][i] == player:
                    pos.append(board[j][i])
            
            if pos == win:
                return player

        # Diagonal check
        diag_check = []
        rev_diag_check = []
        for i in range(len(board)):
            for j in range(len(board)):
                if i == j:
                    diag_check.append(board[i][j])
                if (i + j) == (len(board) - 1):
                    rev_diag_check.append(board[i][j])

        if diag_check == [player]*board_size or rev_diag_check == [player]*board_size:
            return player


    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    game_over = True
    winr = winner(board)
    if winr == 'X' or winr == 'O':
        return True
    for row in board:
        for c in row:
            if not (c == 'X' or c == 'O'):
                game_over = False
                break
    return game_over


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == 'X':
            return 1
        elif winner(board) == 'O':
            return -1
        else:
            return 0
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    else:
        actions_list = actions(board)
        curr_player = player(board)
        print("Actions list", actions_list)

        if curr_player == X:
            my_best_move = -100
            alpha = -float('inf')
            beta = float('inf')
            for act in actions_list:
                new_board = result(board, act)
                opp_best_move = minimize(new_board, alpha, beta)
                print("For player:", curr_player, "Opp best move for Action:", act, "is", opp_best_move)
                if my_best_move < opp_best_move:
                    my_best_move = opp_best_move
                    final_act = act
                alpha = max(alpha, my_best_move)
                if alpha >= beta:
                    break
            print("Final action by X", final_act, my_best_move)
            return final_act
        elif curr_player == O:
            my_best_move = 100
            alpha = -float('inf')
            beta = float('inf')
            for act in actions_list:
                new_board = result(board, act)
                opp_best_move = maximize(new_board, alpha, beta)
                print("For player:", curr_player, "Opp best move for Action:", act, "is", opp_best_move)
                if opp_best_move < my_best_move:
                    my_best_move = opp_best_move
                    final_act = act
                beta = min(beta, my_best_move)
                if alpha >= beta:
                    break
            print("Final action by O", final_act, my_best_move)
            return final_act


def maximize(board, alpha, beta):
    val = -100
    if terminal(board):
        return utility(board)
    else:
        actions_list = actions(board)
        for act in actions_list:
            new_board = result(board, act)
            val = max(val, minimize(new_board, alpha, beta))
            alpha = max(alpha, val)
            if alpha >= beta:
                break
    return val


def minimize(board, alpha, beta):
    val = 100
    if terminal(board):
        return utility(board)
    else:
        actions_list = actions(board)
        for act in actions_list:
            new_board = result(board, act)
            val = min(val, maximize(new_board, alpha, beta))
            beta = min(beta, val)
            if alpha >= beta:
                break
    return val

# def minimax(board):
#     """
#     Returns the optimal action for the current player on the board.
#     """
#     print("Starting Minimax process...")
#     if terminal(board):
#         return None
#     else:
#         actions_list = actions(board)
#         curr_player = player(board)
#         print("Actions list", actions_list)

#         if curr_player == X:
#             my_best_move = -100
#             for act in actions_list:
#                 new_board = result(board, act)
#                 opp_best_move = minimize(new_board)
#                 print("For player:", curr_player, "Opp best move for Action:", act, "is", opp_best_move)
#                 if my_best_move < opp_best_move:
#                     my_best_move = opp_best_move
#                     final_act = act
#             print("Final action by X", final_act, my_best_move)
#             return final_act
#         elif curr_player == O:
#             my_best_move = 100
#             for act in actions_list:
#                 new_board = result(board, act)
#                 opp_best_move = maximize(new_board)
#                 print("For player:", curr_player, "Opp best move for Action:", act, "is", opp_best_move)
#                 if opp_best_move < my_best_move:
#                     my_best_move = opp_best_move
#                     final_act = act
#             print("Final action by O", final_act, my_best_move)
#             return final_act

        

# def maximize(board):

#     val = -100
#     if terminal(board):
#         return utility(board)
#     else:
#         actions_list = actions(board)
#         for index, act in enumerate(actions_list):
#             print("index", index, "action", act, "in maximize")
#             if index >=1:
#                 print('breaking')
#                 return val
#             new_board = result(board, act)
#             val = max(val, minimize(new_board))

#     return val


# def minimize(board):
    
#     val = 100
#     if terminal(board):
#         return utility(board)
#     else:
#         actions_list = actions(board)
#         for index, act in enumerate(actions_list):
#             print("index", index, "action", act, "in minimize")
#             if index >=1:
#                 print('breaking')
#                 return val
#             new_board = result(board, act)
#             val = min(val, maximize(new_board))

#     return val
