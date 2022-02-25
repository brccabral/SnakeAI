import torch
import random
import numpy as np
from collections import deque
from snake_game import SnakeGameAI, Direction, Point

# how many previous moves will be stored in memory_deque
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:
    def __init__(self):
        pass

    def get_state(self, game: SnakeGameAI):
        pass

    def get_move(self, state, action, reward, next_state, game_over):
        pass

    def train_long_memory(self):
        pass

    def train_short_memory(self):
        pass

    def get_action(self, state):
        pass


def train():
    pass


if __name__ == "__main__":
    train()
