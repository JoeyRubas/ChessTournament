
from chessbot import ChessBotAbstract
from naive_weights import pawnweights, knightweights, bishopweights, rookweights, queenweights, kingearly, kinglate
from stockfish import Stockfish



class RealBot(ChessBotAbstract):
    """A real attempt at a relatively lightweight chess engine built from scratch."""


    def __init__(self, name="RealBot"):
        super().__init__(name)
        self.piece_values = [0, 1, 3, 3, 5, 9, 0]


        self.piece_weights = [
            [
                -1,
                pawnweights,
                knightweights,
                bishopweights,
                rookweights,
                queenweights,
                [kingearly[i] * stage / 79 + kinglate[i] * (1 - stage / 79) for i in range(64)],
            ]
            for stage in range(224)
        ]
        self.lookup_table = {}
        params = {
        "Debug Log File": "",
        "Contempt": 0,
        "Min Split Depth": 0,
        "Threads": 1, # More threads will make the engine stronger, but should be kept at less than the number of logical processors on your computer.
        "Ponder": "false",
        "Hash": 32, # Default size is 16 MB. It's recommended that you increase this value, but keep it as some power of 2. E.g., if you're fine using 2 GB of RAM, set Hash to 2048 (11th power of 2).
        "MultiPV": 1,
        "Skill Level": 20,
        "Move Overhead": 10,
        "Minimum Thinking Time": 2,
        "Slow Mover": 100,
        "UCI_Chess960": "false",
        "UCI_LimitStrength": "false",
        "UCI_Elo": 3500
        }
        self.turn = board.turn
        self.engine = Stockfish("/usr/games/stockfish", parameters=params)


    def move(self, board):
        self.lookup_table = {}
        self.turn = int(board.turn)
        for depth in range(1, 5):
            score, best_move = self.minimax(board, depth, float("-inf"), float("inf"))
        return best_move



    def minimax(self, board, depth, alpha, beta, sequence = ""):
        # If we have reached the maximum search depth or game is over, switch to quiescence search
        if depth == 0 or board.is_game_over():
            eval_ = self.evaluate(board)
            if depth + self.turn % 2 == 0:
                return eval_, None
            return -eval_, None

        moves = list(board.legal_moves)
        moves.sort(key = lambda x: self.lookup_table.get(sequence+x.uci(), (0, 0)), reverse = True)
        best_move = moves[0]
        best_score = float("-inf")
       
        # Iterate over possible moves
        for move in moves:
            new_sequence = sequence + move.uci()
            lookup, ldepth = self.lookup_table.get(new_sequence, (0, 0))
            if ldepth >= depth:
                score = lookup
            else:
                board.push(move)                    
                # Negamax framework: we negate the score returned by the recursive call
                score, _ = self.minimax(board, depth - 1, -beta, -alpha, new_sequence)
                score = -score
                self.lookup_table[new_sequence] = (score, depth)
                board.pop()
               
            if score > best_score:
                best_score = score
                best_move = move

            # Alpha-beta updates
            if best_score > alpha:
                alpha = best_score
            if alpha >= beta:
                # Beta cutoff
                break


        return best_score, best_move


    def evaluate(self, board):
        if board.is_checkmate():
            return -float("inf") if board.turn == chess.WHITE else float("inf")
        if board.is_stalemate():
            return 0


        cached_piece_map = list(board.piece_map().items())
        # Basic material calculation
        my_material = 0
        their_material = 0
        for square, piece in cached_piece_map:
            if piece.color == chess.WHITE:
                my_material += self.piece_values[piece.piece_type]
            else:
                their_material += self.piece_values[piece.piece_type]


        # Game stage calculation for king weighting


        my_position = 0
        their_position = 0
        white_pawns = []
        black_pawns = []
        white_rooks = []
        black_rooks = []
        white_king_square = None
        black_king_square = None


        stage = my_material + their_material
        # Collect positional data
        for square, piece in cached_piece_map:
            position_score = self.piece_weights[stage][piece.piece_type][square]
            if piece.color == chess.WHITE:
                my_position += position_score
                if piece.piece_type == chess.PAWN:
                    white_pawns.append(square)
                elif piece.piece_type == chess.ROOK:
                    white_rooks.append(square)
                elif piece.piece_type == chess.KING:
                    white_king_square = square
            else:
                their_position += self.piece_weights[stage][piece.piece_type][63 - square]
                if piece.piece_type == chess.PAWN:
                    black_pawns.append(square)
                elif piece.piece_type == chess.ROOK:
                    black_rooks.append(square)
                elif piece.piece_type == chess.KING:
                    black_king_square = square


        # Base evaluation
        finaleval = (my_material + my_position / 100) - (their_material + their_position / 100)


        # -----------------------------------------------------
        # Additional Considerations
        # -----------------------------------------------------


        # 1. Rooks on open or semi-open files
        #    We'll define:
        #    - open file: no pawns on that file (either color)
        #    - semi-open file: no friendly pawns on that file
        rook_open_file_bonus = 0.5
        rook_semi_open_file_bonus = 0.25


        def file_has_pawn_of_color(pawn_squares, f):
            return any(chess.square_file(p) == f for p in pawn_squares)


        # White rooks
        for r in white_rooks:
            f = chess.square_file(r)
            has_white_pawn = file_has_pawn_of_color(white_pawns, f)
            has_black_pawn = file_has_pawn_of_color(black_pawns, f)
            if not has_white_pawn and not has_black_pawn:
                finaleval += rook_open_file_bonus
            elif not has_white_pawn and has_black_pawn:
                finaleval += rook_semi_open_file_bonus


        # Black rooks
        for r in black_rooks:
            f = chess.square_file(r)
            has_white_pawn = file_has_pawn_of_color(white_pawns, f)
            has_black_pawn = file_has_pawn_of_color(black_pawns, f)
            if not has_white_pawn and not has_black_pawn:
                finaleval -= rook_open_file_bonus
            elif not has_black_pawn and has_white_pawn:
                finaleval -= rook_semi_open_file_bonus


        # 2. Stacked (Doubled/Tripled) pawns
        #    For each file, count how many pawns each side has. If more than one, apply a penalty.
        stacked_pawn_penalty = 0.2
        white_pawn_files = [chess.square_file(p) for p in white_pawns]
        black_pawn_files = [chess.square_file(p) for p in black_pawns]


        from collections import Counter


        white_counts = Counter(white_pawn_files)
        black_counts = Counter(black_pawn_files)


        for f, count in white_counts.items():
            if count > 1:
                # penalty for each extra pawn beyond the first
                finaleval -= (count - 1) * stacked_pawn_penalty
        for f, count in black_counts.items():
            if count > 1:
                finaleval += (count - 1) * stacked_pawn_penalty


        # 3. King Safety
        #    A simple heuristic is to check if the king still has a "pawn shield."
        #    For white: pawns on the king's file and adjacent files in front ranks.
        #    For black: similarly, but looking down from black's perspective.


        king_pawn_shield_bonus = 0.1


        # We'll define a small function to count protective pawns in front of the king.
        def king_pawn_shield_score(king_square, pawns, color):
            # For white, pawns in front means ranks > king_rank up to rank 7
            # For black, pawns in front means ranks < king_rank down to rank 0
            king_file = chess.square_file(king_square)
            king_rank = chess.square_rank(king_square)
            files_to_check = [f for f in [king_file - 1, king_file, king_file + 1] if 0 <= f < 8]


            shield_count = 0
            for p in pawns:
                pf = chess.square_file(p)
                pr = chess.square_rank(p)
                if pf in files_to_check:
                    if color == chess.WHITE and pr > king_rank and pr <= 6:
                        shield_count += 1
                    elif color == chess.BLACK and pr < king_rank and pr >= 1:
                        shield_count += 1
            return shield_count


        if white_king_square is not None:
            white_shield = king_pawn_shield_score(white_king_square, white_pawns, chess.WHITE)
            # If the shield is low, penalize white; if high, reward slightly
            # Scale the bonus or penalty by difference from an ideal shield count (like 2 or 3)
            ideal_shield = 2
            finaleval += (white_shield - ideal_shield) * king_pawn_shield_bonus


        if black_king_square is not None:
            black_shield = king_pawn_shield_score(black_king_square, black_pawns, chess.BLACK)
            ideal_shield = 2
            finaleval -= (black_shield - ideal_shield) * king_pawn_shield_bonus


        return finaleval



