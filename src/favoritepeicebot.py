import time
from chessbot import ChessBotAbstract
from chess import Move
import random
from stockfish import Stockfish


class FavoritePieceBot(ChessBotAbstract):
    """Favorite piece bot has some strong opinions about pieces, and its not afraif to show it!
    It will always try move its favorite piece that's available to move!
    Its order of prefrences is as follows:
    Promote to Queen
    Move the Queen
    Move the king
    Move the Rook
    Move the Bishop
    Move the Pawn
    Move the Knight
    """

    def __init__(self, name="FavoritepieceBot"):
        super().__init__(name)
        self.favorite_pieces = [0, 2, 1, 3, 4, 5, 0]

    def move(self, board):
        best_moves = []
        best_score = -1
        for move in board.legal_moves:
            score = 0
            if move.promotion == 5:
                return move
            if board.piece_at(move.from_square) is not None:
                score = self.favorite_pieces[board.piece_at(move.from_square).piece_type]
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)
        return random.choice(best_moves)
