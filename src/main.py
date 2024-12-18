import chess
from src.randombot import randomBot
from src.alphabot import AlphaBot
from src.match import Match


def main():
    score = [0, 0]
    for i in range(10):
        result = Match(randomBot, AlphaBot).play()
        if result == "1-0":
            score[0] += 1
        elif result == "0-1":
            score[1] += 1
        elif result == "1/2-1/2":
            score[0] += 0.5
            score[1] += 0.5
        print("Score: ", score)
    for i in range(10):
        result = Match(AlphaBot, randomBot).play()
        if result == "1-0":
            score[0] += 1
        elif result == "0-1":
            score[1] += 1
        elif result == "1/2-1/2":
            score[0] += 0.5
            score[1] += 0.5

if __name__ == "__main__":
    main()
