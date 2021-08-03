# @title TicTacToe thing
import numpy as np


class Board:
    num_actions = 9
    shape = (3, 3, 3)

    def __init__(self):
        self.board = np.zeros((3, 3))
        self.split_board = np.zeros((3, 3, 3))
        self.move_history = []
        self.split_board[:, :, 2] = 1

    def check_win(self):
        rows = np.sum(self.board, axis=1)
        cols = np.sum(self.board, axis=0)
        main_diag = np.trace(self.board)
        other_diag = np.fliplr(self.board).trace()

        sums = np.array([rows, cols, [main_diag, other_diag, 0]])

        x_rs, x_cs = np.where(sums == 3)
        o_rs, o_cs = np.where(sums == -3)

        if len(x_rs) > 0 and len(o_rs) > 0:
            raise ValueError('Board contains both o and x winning')
        elif len(x_rs) == 1:
            return 1
        elif len(o_rs) == 1:
            return -1
        elif 0 in self.board:
            return None
        else:
            return 0

    def make_move(self, idx):
        if idx not in self.get_possible_moves():
            raise ValueError('Incorrect move given')
        symbol = self.which_turn()
        unravel = np.unravel_index(idx, self.board.shape)
        self.board[unravel] = symbol
        self.split_board[unravel[0], unravel[1], 2] = 0
        if symbol == -1:
            self.split_board[unravel[0], unravel[1], 1] = 1
        else:
            self.split_board[unravel[0], unravel[1], 0] = 1
        self.move_history.append(idx)

    def which_turn(self):
        return 1 if len(self.move_history) % 2 == 0 else -1

    def get_possible_moves(self):
        return np.where(self.board.flatten() == 0)[0]

    def image(self):
        if self.which_turn() == 1:
            return self.split_board
        else:
            temp = np.copy(self.split_board)
            temp[:, :, 0] = self.split_board[:, :, 1]
            temp[:, :, 1] = self.split_board[:, :, 0]
            return temp

    def clone(self):
        ret = Board()
        ret.board = np.copy(self.board)
        ret.split_board = np.copy(self.split_board)
        ret.move_history = self.move_history.copy()
        return ret

    def tobytes(self):
        return self.board.tobytes()

    def splitbytes(self):
        return self.split_board.tobytes()
