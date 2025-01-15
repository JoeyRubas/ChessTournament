import random
from chessbot import ChessBotAbstract


class ScaredyCatBot(ChessBotAbstract):
    """ScaredyCatBot is a bot that tries to minimize captures and checks."""

    def __init__(self, name="ScaredyCatBot"):
        super().__init__(name)
        self.piece_values = [0, 1, 3, 3, 5, 9, 1000]

    def move(self, board):
        best_moves = []
        best_score = -float("inf")
        for move in list(board.legal_moves):
            board.push(move)
            movescore = 0
            for opponent_move in list(board.legal_moves):
                if board.is_capture(opponent_move):
                    if board.piece_at(opponent_move.to_square) is not None:
                        movescore -= self.piece_values[board.piece_at(opponent_move.to_square).piece_type]
                    else:
                        # en passant
                        movescore -= 1
                if move.promotion:
                    movescore = self.piece_values[move.promotion] - 1
                board.push(opponent_move)
                if board.is_checkmate():
                    movescore = -float("inf")
                elif board.is_check():
                    movescore -= 2
                board.pop()
            board.pop()
            if movescore > best_score:
                best_score = movescore
                best_moves = [move]
            elif movescore == best_score:
                best_moves.append(move)
        return random.choice(best_moves)
