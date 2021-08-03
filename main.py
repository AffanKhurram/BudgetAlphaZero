#%%
from Ac import ActorCritic
import tensorflow
from tensorflow import keras
#%%
from Board import Board
from MCTS import MCTS
import numpy as np
from Connect4 import Connect4

player = ActorCritic(Connect4)

for i in range(10):
  player.generate_games()
  player.train_model(10)



# %%
