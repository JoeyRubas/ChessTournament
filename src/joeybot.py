from chessbot import ChessBotAbstract

class JoeyBot(ChessBotAbstract):
    """Plays the most common move from DB of joeys games"""
    
    def load_pgn(self):
        file_path = "joeychess.pgn"
        """Load all games from a PGN file and parse positions."""
        with open(file_path, "r") as pgn_file:
            while True:
                game = chess.pgn.read_game(pgn_file)
                if game is None:
                    break
                board = game.board()
                for move in game.mainline_moves():
                    fen = board.fen()
                    position_database[fen][move.uci()] += 1
                    board.push(move)
