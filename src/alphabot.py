from chessbot import ChessBotAbstract
import chess

class AlphaBot(ChessBotAbstract):
    def __init__(self, board, color):
        super().__init__(board, color)

    def move(self, board):
        legal_moves = list(board.legal_moves)
        legal_moves.sort(key = lambda move: str(move))
        return legal_moves[0]
    
    def __str__(self):
        return "AlphaBot"