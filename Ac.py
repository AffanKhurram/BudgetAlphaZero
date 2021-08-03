import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import pickle
from pathlib import Path
from tqdm import tqdm
import time
from MCTS import MCTS
from Board import Board

class ActorCritic:
    def __init__(self, board: Board) -> None:
        self.game_type = board
        self.board_size = board.shape
        inputs = layers.Input(shape=self.board_size)
        conv = layers.Conv2D(8, (self.board_size[:2]), activation="relu")(inputs)
        action = layers.Dense(board.num_actions, activation="softmax")(conv)
        critic = layers.Dense(1)(conv)
        self.model = keras.Model(inputs=inputs, outputs=[action, critic])
        self.model.compile(
            loss=['categorical_crossentropy', 'mean_squared_error'])
        self.game_history = []

    def generate_games(self, num_games=10):
        for i in tqdm(range(num_games)):
            self.play_game()
        Path("SelfplayGames").mkdir(parents=True, exist_ok=True)
        pickle.dump(self.game_history, open(
            'SelfplayGames/game_history.pkl', 'wb'))

    def play_game(self):
        board = self.game_type()
        tree = MCTS(self.model)
        moves = []
        # Keep going until the end of the game
        while True:
            pi = tree.run(board, 100)
            possible_actions = board.get_possible_moves()
            dist = pi[possible_actions]/np.sum(pi[possible_actions])
            action = np.random.choice(possible_actions, p=dist)
            moves.append((board.splitbytes(), action, board.which_turn()))
            board.make_move(action)
            winner = board.check_win()
            if winner is not None:
                break
        examples = []
        for s, a, player in moves:
            reward = 0
            if winner != 0:
                reward = 1 if player == winner else -1
            examples.append((s, a, reward))
        self.game_history.append(examples)

    def train_model(self, num_steps, batch_size=32):
        # temp = pickle.load(open('SelfplayGames/game_history.pkl', 'rb'))
        temp = self.game_history
        lst = []
        for r in temp:
            for c in r:
                lst.append(c)

        gh = np.empty(len(lst), dtype=object)
        gh[:] = lst

        # for i in tqdm(range(num_steps)):
        #   indices = np.random.randint(low=0, high=len(lst), size=batch_size)

        examples = np.random.choice(gh, size=batch_size*num_steps)
        states = []
        pis = []
        rewards = []
        for state, pi, reward in examples:
            states.append(np.frombuffer(state, dtype=float).reshape(self.board_size))
            pis.append(pi)
            rewards.append(reward)
        states = np.array(states)
        pis = np.array(pis)
        rewards = np.array(rewards)

        self.model.fit(x=states, y=[np.expand_dims(tf.one_hot(
            pis, 9), axis=[1, 2]), rewards], batch_size=batch_size)
        self.model.save('model' + time.strftime("%Y%m%d-%H%M%S") + '.h5')
