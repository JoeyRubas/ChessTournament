import os
from termcolor import colored
from time import sleep
import chess
from setup import delay, display
from random import choice
import datetime
from chess import pgn


class Match:
    def __init__(self, bot1, bot2, num_games=10, start_from_theory=True):
        self.bot1 = bot1
        self.bot2 = bot2
        self.num_games = num_games
        self.start_from_theory = start_from_theory
        self.games_completed = 0
        self.openings = []
        self.current_opening = []
        self.file_name = f"{bot1}_vs_{bot2}_{num_games}_games_{datetime.datetime.now().strftime('%m-%d')}"
        self.file_name = self.file_name.replace(" ", "_")
        num = 0
        # Add number to the end if file already exists
        while self.file_name + "_" + str(num) + ".pgn" in os.listdir("matchdata"):
            num += 1
        self.file_name = "matchdata/" + self.file_name + "_" + str(num) + ".pgn"
        # create file, but write nothing
        f = open(f"{self.file_name}", "w")
        f.close()

    def pick_opening(self):
        if not self.openings:
            self.openings = [
                "e2e4 e7e5 g1f3 b8c6",  # Ruy Lopez
                "e2e4 e7e5 g1f3 d7d6",  # Philidor Defense
                "e2e4 e7e5 g1f3 f8c5",  # Italian Game
                "e2e4 c7c5 g1f3 d7d6",  # Sicilian Defense
                "d2d4 d7d5 c2c4 e7e6",  # Queen's Gambit Declined
                "d2d4 d7d5 c2c4 d5c4",  # Queen's Gambit Accepted
                "d2d4 g8f6 c2c4 g7g6",  # King's Indian Defense
                "c2c4 e7e5 g1f3 b8c6",  # English Opening
                "e2e4 c7c6 d2d4 d7d5",  # Caro-Kann Defense
                "e2e4 e7e6 d2d4 d7d5",  # French Defense
                "g1f3 d7d5 d2d4 g8f6",  # Reti Opening
                "d2d4 d7d5 g1f3 g8f6",  # Colle System
                "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4",  # Open Sicilian
                "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6",  # Najdorf Sicilian
                "d2d4 g8f6 c2c4 e7e6 g1f3 d7d5",  # Semi-Slav Defense
                "d2d4 g8f6 c2c4 e7e6 g1f3 f8b4",  # Nimzo-Indian Defense
                "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3",  # Scheveningen Variation
                "e2e4 g8f6 e4e5 f6d5",  # Alekhine's Defense
                "e2e4 c7c5 g1f3 e7e6 d2d4 c5d4 f3d4 d7d6",  # Kan Variation
                "e2e4 e7e5 g1f3 g8f6",  # Petrov's Defense
                "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3 e7e6",  # Classical Sicilian
                "d2d4 d7d5 c2c4 c7c6",  # Slav Defense
                "d2d4 d7d5 g1f3 g8f6 c2c4 e7e6",  # Catalan Opening
                "e2e4 g8f6 e4e5 f6d5 d2d4",  # Scandinavian Defense
                "e2e4 c7c5 b1c3 d7d6 f2f4",  # Grand Prix Attack
                "e2e4 e7e5 g1f3 b8c6 f1b5",  # Ruy Lopez: Exchange Variation
                "d2d4 g8f6 c2c4 e7e6 g1f3 d7d5 c4d5",  # Exchange Slav
                "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3 a7a6",  # Najdorf Variation
                "d2d4 g8f6 c2c4 g7g6 g1f3 f8g7",  # King's Indian Fianchetto
                "d2d4 d7d5 g1f3 g8f6 c2c4 e7e6 b1c3",  # Orthodox QGD
                "e2e4 e7e5 f2f4 e5f4",  # King's Gambit Accepted
                "e2e4 e7e5 f2f4 e5f4 g1f3",  # King's Gambit Declined
                "d2d4 f7f5 c2c4 g8f6",  # Dutch Defense
                "e2e4 g8f6 e4e5 f6e4",  # Albin Countergambit
                "d2d4 d7d5 c2c4 e7e5",  # Albin Countergambit
                "e2e4 e7e5 g1f3 b8c6 f1c4",  # Italian Game: Giuoco Piano
                "e2e4 c7c5 b1c3 d7d6 f2f4 g7g6",  # Sicilian: Dragon Variation
                "d2d4 d7d5 c2c4 e7e5 d4e5 d5d4",  # Budapest Gambit
                "e2e4 e7e5 g1f3 b8c6 f1b5 a7a6",  # Ruy Lopez: Morphy Defense
                "d2d4 g8f6 c2c4 e7e6 g1f3 d7d5 c4d5 f6d5",  # Grunfeld Defense
                "e2e4 c7c5 g1f3 d7d6 d2d4 c5d4 f3d4 g8f6 b1c3 e7e6 g2g3",  # Dragon Accelerated
            ]
        self.current_opening = choice(self.openings)
        self.openings.remove(self.current_opening)

    def play(self):
        score = [0, 0, 0]
        for i in range(self.num_games):
            if i % 2 == 0:
                game = Game(self.bot1, self.bot2, self.file_name)
                if self.start_from_theory:
                    self.pick_opening()
            else:
                game = Game(self.bot2, self.bot1)
            game.play_opening(self.current_opening)
            result = game.play()
            if i % 2 == 1:
                result = result[::-1]
            if result == "1-0":
                score[0] += 1
            elif result == "0-1":
                score[1] += 1
            else:
                score[2] += 1
            print(f"Score: {score[0]} - {score[1]} - {score[2]}")
            self.games_completed += 1
        return score


class Game:
    def __init__(self, whitebot, blackbot, file_name=None):
        self.board = chess.Board()
        self.whitebot = whitebot
        self.blackbot = blackbot
        self.last_move = None
        self.file_name = file_name

    def play_opening(self, opening):
        for move in opening.split():
            self.board.push(chess.Move.from_uci(move))

    def save_game(self):
        game = pgn.Game.from_board(self.board)
        game.headers["Event"] = f"Simulated game with {self.board.fullmove_number} moves"
        game.headers["Site"] = "Online"
        game.headers["Date"] = datetime.datetime.now().strftime("%Y.%m.%d")
        game.headers["Round"] = "1"
        game.headers["White"] = str(self.whitebot)
        game.headers["Black"] = str(self.blackbot)
        game.headers["Result"] = self.board.result()

        with open(self.file_name, "a") as pgn_file:
            print("\n\n", file=pgn_file)
            print(game, file=pgn_file)

    def color_board(self, board_str):
        colored_str = list(board_str)
        for idx in range(0, 127, 2):
            char = board_str[idx]
            if char.isupper():
                piece_color = "green"
                char = chess.UNICODE_PIECE_SYMBOLS[char]
            elif char.islower():
                piece_color = "red"
                char = chess.UNICODE_PIECE_SYMBOLS[char]
            else:
                piece_color = None
            piece_idx = 64 - idx / 2 - (8 - idx % 16)
            if self.last_move and (self.last_move.to_square == piece_idx or self.last_move.from_square == piece_idx):
                colored_str[idx] = colored(char, piece_color, attrs=["bold", "reverse"])

            else:
                colored_str[idx] = colored(char, piece_color) if piece_color else char
        return "".join(colored_str)

    def display_board(self):
        print(self.color_board(str(self.board)))
        print(f"White: {self.whitebot}\nBlack: {self.blackbot}\n")

    def get_move(self, bot):
        try: 
            move = bot.move(self.board)
            if display:
                    print(f"{bot} plays {move}")
            return move
        except Exception as e:
            print(
                    f"Encountered an exception during match between white: {self.whitebot} vs black: {self.blackbot}: {e}"
                )
            print(f"During turn: {self.board.turn} number {self.board.fullmove_number}")
            print(f"Board state: {self.board}")
            print("the error is:", end = " ")
            import traceback
            traceback.print_exc()
        return list(self.board.legal_moves)[0]
    def play(self):
        while not self.board.is_game_over():
            turn = self.board.turn
            if turn == chess.WHITE:
                move = self.get_move(self.whitebot)
            else:
                move = self.get_move(self.blackbot)
            self.board.push(move)
            if display:
                self.last_move = move
                self.display_board()
                print("\n")
            if delay:
                sleep(delay)
        if display or True:
            print(f"{self.whitebot} vs {self.blackbot}:", end=" ")
            if self.board.is_checkmate():
                print(
                    f"{self.whitebot if self.board.turn == chess.BLACK else self.blackbot} wins by checkmate in {self.board.fullmove_number} moves."
                )
            elif self.board.is_stalemate():
                print(f"Game drawn by stalemate in {self.board.fullmove_number} moves.")
            elif self.board.is_insufficient_material():
                print(f"Game drawn by insufficient material in {self.board.fullmove_number} moves.")
            elif self.board.is_seventyfive_moves():
                print(f"Game drawn by 75-move rule in {self.board.fullmove_number} moves.")
            elif self.board.is_fivefold_repetition():
                print(f"Game drawn by fivefold repetition in {self.board.fullmove_number} moves.")
        # Save game PGN
        if self.file_name:
            self.save_game()

        return self.board.result()
