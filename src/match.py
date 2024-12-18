from termcolor import colored
from time import sleep
import chess

class Match():
    def __init__(self, bot1class, bot2class):
        self.board = chess.Board()
        self.bot1 = bot1class(self.board, chess.WHITE)
        self.bot2 = bot2class(self.board, chess.BLACK)
        self.last_move = None

    def color_board(self, board_str):
        colored_str = ""
        for i, char in enumerate(board_str):
            if char.isupper():
                piece_color = 'green'
            elif char.islower():
                piece_color = 'red'
            else:
                piece_color = None

            if self.last_move and self.last_move.to_square == i:
                colored_str += colored(char, piece_color, attrs=['bold'])
            else:
                colored_str += colored(char, piece_color) if piece_color else char
        return colored_str

    def display_board(self):
        print(self.color_board(str(self.board)))
        print(f"White: {self.bot1}\nBlack: {self.bot2}\n")

    def play(self, display = False, delay = 0):
        while not self.board.is_game_over():
            if self.board.turn == chess.WHITE:
                move = self.bot1.move(self.board)
                if display:
                    print(f"{self.bot1} plays {move}")
            else:
                move = self.bot2.move(self.board)
                if display:
                    print(f"{self.bot2} plays {move}")
            
            self.board.push(move)
            if display:
                self.last_move = move
                self.display_board()
                print("\n")
            if delay:
                sleep(delay)
        return self.board.result()
