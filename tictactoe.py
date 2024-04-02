"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

current_move = "X"


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    global current_move

    x_count = sum(row.count("X") for row in board)
    o_count = sum(row.count("O") for row in board)

    if x_count > o_count:
        current_move = "O"
        return "O"
    else:
        current_move = "X"
        return "X"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    if terminal(board):
        return set()

    actions = set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] is None:
                actions.add((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if len(action) != 2:
        raise Exception("Invalid input")

    row, col = action[0], action[1]

    board_copy = copy.deepcopy(board)

    if board_copy[row][col] != EMPTY:
        raise Exception("Spot already taken")
    else:
        board_copy[row][col] = player(board)

    return board_copy


def check_horizontal(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    return False


def check_vertical(board, player):
    for col in range(len(board[0])):
        if all(board[row][col] == player for row in range(len(board))):
            return True
    return False


def check_diagonal(board, player):
    diag1 = all(board[i][i] == player for i in range(len(board)))
    diag2 = all(board[i][len(board) - 1 - i] == player for i in range(len(board)))
    return diag1 or diag2


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for player in ["X", "O"]:
        if check_horizontal(board, player) or check_vertical(board, player) or check_diagonal(board, player):
            return player
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None or all(cell is not None for row in board for cell in row):
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == "X":
        return 1
    elif winner(board) == "O":
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == "X":
        score = -math.inf
        action_to_take = None

        for action in actions(board):
            min_val = minvalue(result(board, action))

            if min_val > score:
                score = min_val
                action_to_take = action

        return action_to_take

    elif player(board) == "O":
        score = math.inf
        action_to_take = None

        for action in actions(board):
            max_val = maxvalue(result(board, action))

            if max_val < score:
                score = max_val
                action_to_take = action

        return action_to_take


def minvalue(board):
    """
    Returns the minimum value
    """

    if terminal(board):
        return utility(board)

    max_value = math.inf
    for action in actions(board):
        max_value = min(max_value, maxvalue(result(board, action)))

    return max_value


def maxvalue(board):
    """
    Returns the maximum value
    """

    if terminal(board):
        return utility(board)

    min_val = -math.inf
    for action in actions(board):
        min_val = max(min_val, minvalue(result(board, action)))

    return min_val
