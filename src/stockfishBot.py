from chessbot import ChessBotAbstract
from chess import Move
import random
from stockfish import Stockfish


class StockfishBot(ChessBotAbstract):
    """Stockfish used as a reference for the other bots to play against.
        - Concentration and percentile used to more granularly measure 
        other bots by reducing Stockfish's strength by regular intervals.
        
        Concentration: Float [0.0, 1.0]
            - Percentage of moves played by Stockfish. Remaining moves selected randomly.
            - Values can be any float between 0.0 and 1.0 inclusive.
    """
    def __init__(self, concentration = 1,  name=None):
        if name is None:
            name = f"StockfishBot {concentration}"
        super().__init__(name)
        self.concentration = concentration
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
        
        self.engine = Stockfish("/usr/games/stockfish", parameters=params)
        
    
    def move(self, board):
        self.engine.set_fen_position(board.fen())
        if random.random() < self.concentration:
            return Move.from_uci(self.engine.get_best_move())
        else:
            return random.choice(list(board.legal_moves))
