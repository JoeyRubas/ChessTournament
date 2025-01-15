from chessbot import ChessBotAbstract

class LawyerBot(ChessBotAbstract):
    """Stolen from Tom7 YouTube Comment Section
        Does a low depth search for the move which maximizes its own legal moves.
        """
    def __init__(self, name="LawyerBot"):
        super().__init__(name)
    
    def move(self, board):
        legal_moves = list(board.legal_moves)
        best_move = None
        best_score = -1
        for move in legal_moves:
            board.push(move)
            opponent_legal_moves = list(board.legal_moves)
            total = 0
            count = 0
            for opponent_move in opponent_legal_moves:
                board.push(opponent_move)
                total += len(list(board.legal_moves))
                count += 1
                board.pop()
            board.pop()
            score = (total / count) if count > 0 else 0
            if score > best_score:
                best_score = score
                best_move = move
        return best_move
    