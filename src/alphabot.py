from chessbot import ChessBotAbstract
import chess

class AlphaBot(ChessBotAbstract):
    def __init__(self, name="AlphaBot"):
        super().__init__(name)

    def move(self, board):
        legal_moves = list(board.legal_moves)
        legal_moves.sort(key = lambda move: str(move))
        return legal_moves[0]