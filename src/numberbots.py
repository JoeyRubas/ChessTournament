import random
from chessbot import ChessBotAbstract


class BigNumberBot(ChessBotAbstract):
    """BigNumberBot is a bot that tries to move its pieces to the biggest number on the board."""

    def __init__(self, name="BigNumberBot"):
        super().__init__(name)

    def move(self, board):
        best_moves = []
        best_score = -65
        for move in board.legal_moves:
            score = move.from_square - move.to_square
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)
        return random.choice(best_moves)
    
import random
from chessbot import ChessBotAbstract


class SmallNumberBot(ChessBotAbstract):
    """BigNumberBot is a bot that tries to move its pieces to the biggest number on the board."""

    def __init__(self, name="SmallNumberBot"):
        super().__init__(name)

    def move(self, board):
        best_moves = []
        best_score = -65
        for move in board.legal_moves:
            score = move.to_square - move.from_square
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)
        return random.choice(best_moves)

