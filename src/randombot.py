from chessbot import ChessBotAbstract
import chess
import random

class randomBot(ChessBotAbstract):
    def __init__(self, name="RandomBot"):
        super().__init__(name)

    def move(self, board):
        legal_moves = list(board.legal_moves)
        return random.choice(legal_moves)
