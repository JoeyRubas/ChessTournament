from chess import Move
from chessbot import ChessBotAbstract
from naive_weights import pawnweights, knightweights, bishopweights, rookweights, queenweights, kingearly, kinglate


class NaiveBot(ChessBotAbstract):
    """A first foray at some **good** chess software, naive bot uses a legitimae evaluation function,
    but seems completely unaware that his opponent can move too."""

    def __init__(self, name=None, depth=2):
        self.depth = depth
        if name is None:
            name = f"NaiveBot Depth {depth}"
        super().__init__(name)

    def move(self, board):
        result = self.maximax(board, self.depth)
        if result is not None:
            try: 
                move = result[1]
                if move is not None:
                    return move
            except:
                pass
        return board.legal_moves[0]

    def maximax(self, board, depth):
        if depth == 0:
            return self.evaluate(board), None
        best_move = None
        best_score = -float("inf")
        for move in board.legal_moves:
            board.push(move)
            if board.is_checkmate():
                board.pop()
                return float("inf"), move
            else:
                board.push(Move.null())
                score, _ = self.maximax(board, depth - 1)
            board.pop()
            board.pop()
            if score > best_score:
                best_score = score
                best_move = move
        return best_score, best_move

    def evaluate(self, board):
        # Checkmate and stalemate evaluation
        if board.is_checkmate():
            return float("inf")
        if board.is_stalemate():
            return 0

        # Piece values
        piece_values = [0, 1, 3, 3, 5, 9, 0]

        # Material evaluation
        my_material = 0
        their_material = 0
        for square, piece in board.piece_map().items():
            if piece.color == board.turn:
                my_material += piece_values[piece.piece_type]
            else:
                their_material += piece_values[piece.piece_type]

        # Calculate game stage factor (1 in the opening, 0 in the endgame)
        stage = (my_material + their_material) / 79
        king_weights = [kingearly[i] * stage + kinglate[i] * (1 - stage) for i in range(64)]

        # Piece-square tables
        piece_weights = [-1, pawnweights, knightweights, bishopweights, rookweights, queenweights, king_weights]

        # Positional evaluation
        my_position = 0
        their_position = 0
        for square, piece in board.piece_map().items():
            position_score = piece_weights[piece.piece_type][square]
            if piece.color == board.turn:
                my_position += position_score if board.turn == 0 else piece_weights[piece.piece_type][63 - square]
            else:
                their_position += piece_weights[piece.piece_type][63 - square] if board.turn == 0 else position_score
        finaleval = my_material + my_position / 100 - their_material - their_position / 100
        # Final evaluation score
        return finaleval
