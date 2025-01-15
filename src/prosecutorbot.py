from chessbot import ChessBotAbstract

class ProsecutorBot(ChessBotAbstract):
    """In some wat, the opposite of LawyerBot. Tries to minimize the number of legal moves the opponent has."""
    def __init__(self, name="ProsecutorBot"):
        super().__init__(name)
    
    def move(self, board):
        legal_moves = list(board.legal_moves)
        best_move = None
        best_score = float('inf')
        for move in legal_moves:
            board.push(move)
            opponent_legal_moves = len(list(board.legal_moves))
            board.pop()
            if opponent_legal_moves < best_score:
                best_score = opponent_legal_moves
                best_move = move
        return best_move