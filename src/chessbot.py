import chess

class ChessBotAbstract():
    def __init__(self, board, color):
        self.board = board
        self.color = color

    def move(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def play(self):
        while not self.board.is_game_over():
            self.move()
            print(self.board)
            
    def evaluate(self):
        raise NotImplementedError("Subclass must implement abstract method")