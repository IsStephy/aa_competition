import os
import importlib.util
import random
import time
import csv

# Load strategy functions from a folder
def load_strategies(folder_path):
    strategies = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".py"):
            filepath = os.path.join(folder_path, filename)
            module_name = filename[:-3]
            spec = importlib.util.spec_from_file_location(module_name, filepath)
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
                if hasattr(module, "strategy"):
                    strategies[module_name] = module.strategy
                else:
                    print(f"  {filename} does not contain a 'strategy' function.")
            except Exception as e:
                print(f" Error loading {filename}: {e}")
    return strategies

# Play a single match of multiple rounds
def play_match(strategy1, strategy2, rounds):
    history1 = []
    history2 = []
    score1 = 0
    score2 = 0
    for _ in range(rounds):
        move1 = strategy1(history1, history2, rounds)
        move2 = strategy2(history2, history1, rounds)

        move1 = int(bool(move1))
        move2 = int(bool(move2))

        if move1 == 1 and move2 == 1:
            score1 += 3
            score2 += 3
        elif move1 == 1 and move2 == 0:
            score1 += 0
            score2 += 5
        elif move1 == 0 and move2 == 1:
            score1 += 5
            score2 += 0
        else:
            score1 += 1
            score2 += 1

        history1.append(move1)
        history2.append(move2)

    return score1, score2, history1, history2

# Run tournament and export results
def run_tournament(folder, round_name="round", rounds=100):
    strategies = load_strategies(folder)
    scores = {name: 0 for name in strategies}
    win_stats = {name: {"wins": 0, "total": 0} for name in strategies}
    match_results = []

    names = list(strategies.keys())
    for i in range(len(names)):
        for j in range(len(names)):
            if i != j:
                name1, name2 = names[i], names[j]
                s1, s2, h1, h2 = play_match(strategies[name1], strategies[name2], rounds)

                scores[name1] += s1
                #scores[name2] += s2

                win_stats[name1]["total"] += 1
                #win_stats[name2]["total"] += 1

                if s1 > s2:
                    win_stats[name1]["wins"] += 1
                #elif s2 > s1:
                    #win_stats[name2]["wins"] += 1

                match_results.append([
                    name1, name2, s1, s2, h1, h2
                ])

    # Export total scores with wins and matches
    with open(f"results_{round_name}_scores.csv", mode="w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Strategy", "Total Score", "Wins", "Matches Played", "Win Ratio"])
        for name, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            wins = win_stats[name]["wins"]
            total = win_stats[name]["total"]
            win_ratio = round(wins / total, 4) if total > 0 else 0
            writer.writerow([name, score, wins, total, win_ratio])

    # Export match details
    with open(f"results_{round_name}_matches.csv", mode="w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Player1", "Player2", "Score1", "Score2", "History1", "History2"])
        for match in match_results:
            writer.writerow(match)

    print("\n Final Scores:")
    for name, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        wins = win_stats[name]["wins"]
        total = win_stats[name]["total"]
        win_ratio = round(wins / total, 4) if total > 0 else 0
        print(f"{name}: {score} | Wins: {wins}/{total} ({win_ratio*100:.2f}%)")

if __name__ == "__main__":
    folder_path = "AA_Tournament"
    default_rounds = 100

    print("=== ROUND 1: 100 games each ===")
    start = time.time()
    run_tournament(folder_path, round_name="round1", rounds=default_rounds)
    end = time.time()
    print(f"time taken for first round {end-start:.2f} seconds")

    print("\n=== ROUND 2: 187 of games ===")
    #custom_rounds = int(input("Enter number of rounds for next tournament: "))
    start = time.time()
    run_tournament(folder_path, round_name="round2", rounds=187)
    end = time.time()
    print(f"time taken for second round {end-start:.2f} seconds")
