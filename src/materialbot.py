import random
from chessbot import ChessBotAbstract
from chess import Move

class MaterialBot(ChessBotAbstract):
    def __init__(self, name="MaterialBot"):
        super().__init__(name)
        self.piece_values = [0, 1, 3, 3, 5, 9, 1000]
    
    def move(self, board):
        best_moves = []
        best_score = -1
        for move in board.legal_moves:
            score = 0
            if move.promotion:
                score += self.piece_values[move.promotion] -1 # -1 to account for the pawn that was promoted
            if board.piece_at(move.to_square) is not None:
                score += self.piece_values[board.piece_at(move.to_square).piece_type]
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)
        if best_score < 1:
            for move1 in board.legal_moves:
                board.push(move1)
                board.push(Move.null())
                max_attack = -1
                for move2 in board.legal_moves:
                    if board.piece_at(move2.to_square) is not None:
                        max_attack = max(max_attack, self.piece_values[board.piece_at(move2.to_square).piece_type])
                board.pop()
                board.pop()
                if max_attack > best_score:
                    best_score = max_attack
                    best_moves = [move1]
                elif max_attack == best_score:
                    best_moves.append(move1)
        return random.choice(best_moves)
    