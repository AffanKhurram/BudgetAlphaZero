from tensorflow.keras import Model
import numpy as np
from math import sqrt
from Board import Board

class MCTS:
    def __init__(self, network: Model) -> None:
        self.nn = network
        self.tree = {}

    def run(self, board: Board, num_sims: int, t=1):
        """
        Runs MCTS num_sims time. Returns a policy vector
        """
        for i in range(num_sims):
            temp_board = board.clone()
            self.search(temp_board, max((10 - i)/(10), 0.05))

        _, _, n = self.tree[board.tobytes()]
        adjusted = n**1/t
        return adjusted/np.sum(adjusted)


    def search(self, board: Board, epsilon=0.05, cpuct=4):
        """
        Runs one search of the tree. Keeps going until a leaf node is met and expands it and returns 
        the reward expected for the current player
        """
        if board.tobytes() in self.tree:
            q, p, n = self.tree[board.tobytes()]
            s = sqrt(np.sum(n))
            if np.random.rand() < epsilon:  
                possible_actions = board.get_possible_moves()
                best_action = np.random.choice(possible_actions)
            else:
                best_action = self.select_action(board, cpuct)
            board.make_move(best_action)
            v = -self.search(board)
            n[best_action] += 1
            # TODO make sure that this calculation is okay
            q[best_action] += v/n[best_action]  
            return v
            
        # Reached a leaf node
        else:
            winner = board.check_win()
            if winner is not None:
                turn = board.which_turn()
                # I don't think i need this part, but keeping it for now
                # In theory this will always return 0 or -1 because of the way I have the tree set up
                if winner != 0:
                    return 1 if turn == winner else -1 
                return 0

            return self.expand(board)
        
    def select_action(self, board: Board, cpuct):
        q, p, n = self.tree[board.tobytes()]
        s = sqrt(np.sum(n))
        u = q + cpuct * p * (s)/(1 + n)
        possible_actions = board.get_possible_moves()
        best_action = possible_actions[0]
        max_so_far = u[best_action]
        for action in possible_actions[1:]:
            if u[action] > max_so_far:
                max_so_far = u[action]
                best_action = action

        return best_action

    def expand(self, board: Board):
        """
        Creates the new node and its children and initializes its values
        """
        p, v = self.nn.predict(np.expand_dims(board.image(), axis=0))
        q = np.zeros(board.num_actions)
        n = np.zeros(board.num_actions)
        self.tree[board.tobytes()] = (q, p.squeeze(), n)
        return v

    def reset_tree(self):
        self.tree = {}
        
