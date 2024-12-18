from chessbot import ChessBotAbstract
import chess
import random

class randomBot(ChessBotAbstract):
    def __init__(self, board, color):
        super().__init__(board, color)

    def move(self, board):
        legal_moves = list(board.legal_moves)
        return random.choice(legal_moves)

    def __str__(self):
        return "RandomBot"