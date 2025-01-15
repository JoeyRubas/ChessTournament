import chess
from randombot import randomBot
from alphabot import AlphaBot
from match import Match
from lawyer import LawyerBot
from stockfishBot import StockfishBot
from materialbot import MaterialBot
import concurrent.futures
import time
from tabulate import tabulate
from prosecutorbot import ProsecutorBot
from favoritepeicebot import FavoritePieceBot
from numberbots import BigNumberBot, SmallNumberBot
from naivebot import NaiveBot
from scaredeycatbot import ScaredyCatBot
from realbot import RealBot


def run_match(bot1_class, bot2_class, *args1, **kwargs1):
    bot1 = bot1_class(*args1, **kwargs1)
    bot2 = bot2_class(*args1, **kwargs1)
    match = Match(bot1, bot2, 10)
    result = match.play()
    return (bot1.name, bot2.name), result


def print_results(results, rankings, elo_ratings):
    # Prepare results data for tabulation
    results_table = [[*key, *value] for key, value in results.items()]

    # Prepare rankings data for tabulation (original score-based)
    rankings_table = [
        [i + 1, bot, score, (score[0] - score[1] + 0.5 * score[2]) / sum(score)]
        for i, (bot, score) in enumerate(rankings)
    ]

    # Combine Elo ratings into the rankings table
    # Insert Elo rating as a separate column
    for row in rankings_table:
        bot_name = row[1]
        row.append(elo_ratings[bot_name])

    # Print tabulated results
    print("Results Summary:")
    print(tabulate(results_table, headers=["Bot1", "Bot2", "Bot 1 Wins", "Bot2 Wins", "Draws"], tablefmt="pretty"))

    print("\nRankings (Score-based):")
    print(tabulate(rankings_table, headers=["Rank", "Bot", "Score", "Total", "Elo"], tablefmt="pretty"))


def update_elo(elo_ratings, results, k_factor=20):
    # Elo ratings are updated match by match
    # Note: Because we are doing this after all matches,
    # this is only an approximation and not a true sequential Elo.
    for (bot1, bot2), (bot1_wins, bot2_wins, draws) in results.items():
        # Current ratings
        R_A = elo_ratings[bot1]
        R_B = elo_ratings[bot2]

        # Number of games in the match
        N = bot1_wins + bot2_wins + draws
        if N == 0:
            continue

        # A's actual score
        S_A = bot1_wins + 0.5 * draws
        # A's expected score per game
        E_A = 1.0 / (1 + 10 ** ((R_B - R_A) / 400.0))

        # Update ratings
        elo_ratings[bot1] = R_A + k_factor * (S_A - E_A * N)
        elo_ratings[bot2] = R_B + k_factor * ((N - S_A) - (1 - E_A) * N)


def threaded_tournament():
    start = time.time()
    bot_classes = [
        #AlphaBot,
        randomBot,
        #BigNumberBot,
        #SmallNumberBot,
        #NaiveBot,
        #LawyerBot,
        #FavoritePieceBot,
        #MaterialBot,
        #ProsecutorBot,
        #ScaredyCatBot,
        RealBot,
        #lambda: StockfishBot(concentration=0.1),
        # lambda: StockfishBot(concentration=0.2),
        #lambda: StockfishBot(concentration=0.3),
        # lambda: StockfishBot(concentration=0.4),
        #lambda: StockfishBot(concentration=0.5),
        # lambda: StockfishBot(concentration=0.6),
         #lambda: StockfishBot(concentration=0.7),
        # lambda: StockfishBot(concentration=0.8),
        #lambda: StockfishBot(concentration=0.9),
        # lambda: StockfishBot(concentration=1),
    ]
    results = {}
    botscores = {str(bot_class()): [0, 0, 0] for bot_class in bot_classes}

    # Initialize Elo ratings
    elo_ratings = {str(bot_class()): 1500 for bot_class in bot_classes}

    matches = [
        [bot_classes[i], bot_classes[j]] for i in range(len(bot_classes)) for j in range(i + 1, len(bot_classes))
    ]
    matches = [sorted(match, key=lambda x: str(x())) for match in matches if type(match[0]()) != type(match[1]())]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(run_match, *match) for match in matches]

        for future in concurrent.futures.as_completed(futures):
            bots, result = future.result()
            results[bots] = result
            bot1, bot2 = bots
            botscores[bot1][0] += result[0]  # wins
            botscores[bot1][1] += result[1]  # losses
            botscores[bot1][2] += result[2]  # draws

            botscores[bot2][0] += result[1]  # wins from bot2 perspective
            botscores[bot2][1] += result[0]  # losses from bot2 perspective
            botscores[bot2][2] += result[2]  # draws

    # After all results are in, update Elo ratings
    update_elo(elo_ratings, results, k_factor=20)

    # Sort bots by their score-based performance for the ranking table
    rankings = sorted(botscores.items(), key=lambda x: (x[1][0] - x[1][1] + 0.5 * x[1][2]) / sum(x[1]), reverse=True)

    print_results(results, rankings, elo_ratings)
    print(f"Time taken: {time.time()-start}")


if __name__ == "__main__":
    threaded_tournament()
