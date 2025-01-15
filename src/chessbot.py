import chess

class ChessBotAbstract():
    def __init__(self, name):
        self.name = name

    def move(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def play(self):
        while not self.board.is_game_over():
            self.move()
            print(self.board)
            
    def evaluate(self):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def __str__(self):
        return self.name