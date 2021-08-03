import numpy as np
from Board import Board


class Table():
    def __init__(self):
        self.init_board = np.zeros([6, 7]).astype(str)
        self.init_board[self.init_board == "0.0"] = " "
        self.player = 0
        self.current_board = self.init_board

    def drop_piece(self, column):
        if self.current_board[0, column] != " ":
            return "Invalid move"
        else:
            row = 0
            pos = " "
            while (pos == " "):
                if row == 6:
                    row += 1
                    break
                pos = self.current_board[row, column]
                row += 1
            if self.player == 0:
                self.current_board[row-2, column] = "O"
                self.player = 1
                return row-2
            elif self.player == 1:
                self.current_board[row-2, column] = "X"
                self.player = 0
                return row-2

    def check_winner(self):
        if self.player == 1:
            for row in range(6):
                for col in range(7):
                    if self.current_board[row, col] != " ":
                        # rows
                        try:
                            if self.current_board[row, col] == "O" and self.current_board[row + 1, col] == "O" and \
                                    self.current_board[row + 2, col] == "O" and self.current_board[row + 3, col] == "O":
                                # print("row")
                                return True
                        except IndexError:
                            next
                        # columns
                        try:
                            if self.current_board[row, col] == "O" and self.current_board[row, col + 1] == "O" and \
                                    self.current_board[row, col + 2] == "O" and self.current_board[row, col + 3] == "O":
                                # print("col")
                                return True
                        except IndexError:
                            next
                        # \ diagonal
                        try:
                            if self.current_board[row, col] == "O" and self.current_board[row + 1, col + 1] == "O" and \
                                    self.current_board[row + 2, col + 2] == "O" and self.current_board[row + 3, col + 3] == "O":
                                # print("\\")
                                return True
                        except IndexError:
                            next
                        # / diagonal
                        try:
                            if self.current_board[row, col] == "O" and self.current_board[row + 1, col - 1] == "O" and \
                                    self.current_board[row + 2, col - 2] == "O" and self.current_board[row + 3, col - 3] == "O"\
                                    and (col-3) >= 0:
                                # print("/")
                                return True
                        except IndexError:
                            next
        if self.player == 0:
            for row in range(6):
                for col in range(7):
                    if self.current_board[row, col] != " ":
                        # rows
                        try:
                            if self.current_board[row, col] == "X" and self.current_board[row + 1, col] == "X" and \
                                    self.current_board[row + 2, col] == "X" and self.current_board[row + 3, col] == "X":
                                return True
                        except IndexError:
                            next
                        # columns
                        try:
                            if self.current_board[row, col] == "X" and self.current_board[row, col + 1] == "X" and \
                                    self.current_board[row, col + 2] == "X" and self.current_board[row, col + 3] == "X":
                                return True
                        except IndexError:
                            next
                        # \ diagonal
                        try:
                            if self.current_board[row, col] == "X" and self.current_board[row + 1, col + 1] == "X" and \
                                    self.current_board[row + 2, col + 2] == "X" and self.current_board[row + 3, col + 3] == "X":
                                return True
                        except IndexError:
                            next
                        # / diagonal
                        try:
                            if self.current_board[row, col] == "X" and self.current_board[row + 1, col - 1] == "X" and \
                                    self.current_board[row + 2, col - 2] == "X" and self.current_board[row + 3, col - 3] == "X"\
                                    and (col-3) >= 0:
                                return True
                        except IndexError:
                            next

    def actions(self):  # returns all possible moves
        acts = []
        for col in range(7):
            if self.current_board[0, col] == " ":
                acts.append(col)
        return acts


class Connect4(Board):
    num_actions = 7
    shape = (6, 7, 3)

    def __init__(self):
        self.board = Table()
        self.split_board = np.zeros((6, 7, 3))
        self.split_board[:, :, 2] = 1
        self.move_history = []

    def check_win(self):
        game_over = self.board.check_winner()
        if game_over:
            if self.board.player == 0:
                return -1
            else:
                return 1
        if not any(self.board.current_board[0, :] == ' '):
            return 0
        return None

    def make_move(self, action):
        successful = self.board.drop_piece(action)
        if type(successful) == str:
            raise ValueError("Incorrect index")
        # Need to do 1- because drop_piece changes whose turn it is
        self.split_board[successful, action, 1-self.board.player] = 1
        self.split_board[successful, action, 2] = 0
        self.move_history.append(action)

    def which_turn(self):
        if self.board.player == 0:
            return 1
        else:
            return -1

    def get_possible_moves(self):
        return self.board.actions()

    def clone(self):
        temp = Connect4()
        temp.board.current_board = np.copy(self.board.current_board)
        temp.split_board = np.copy(self.split_board)
        temp.move_history = self.move_history.copy()
        return temp

    def image(self):
        if self.board.player == 0:
            return self.split_board
        else:
            temp = np.copy(self.split_board)
            temp[:, :, 0] = self.split_board[:, :, 1]
            temp[:, :, 1] = self.split_board[:, :, 0]
            return temp

    def tobytes(self):
        return self.board.current_board.tobytes()

    def splitbytes(self):
        return self.split_board.tobytes()
