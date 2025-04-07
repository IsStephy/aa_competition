import os
import importlib.util
import random
import time

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
def play_match(strategy1, strategy2, rounds=None, custom=None):
    history1 = []
    history2 = []
    score1 = 0
    score2 = 0
    round = rounds
    if rounds == None:
        rounds = custom
    for _ in range(rounds):
        move1 = strategy1(history1, history2, round)
        move2 = strategy2(history2, history1, round)

        # Normalize moves
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
        else:  # both defect
            score1 += 1
            score2 += 1

        history1.append(move1)
        history2.append(move2)

    return score1, score2

# Run tournament
def run_tournament(folder, rounds=100, custom = None):
    strategies = load_strategies(folder)
    scores = {name: 0 for name in strategies}

    names = list(strategies.keys())
    for i in range(len(names)):
        for j in range(len(names)):
            if i!=j:
                name1, name2 = names[i], names[j]
                if name1 == "denis":
                    print("Begining:   "+
                        str(scores[name1]) + "   " + name1 + "      -----       " + name2)

                s1, s2 = play_match(strategies[name1], strategies[name2], rounds, custom)
                scores[name1] += s1
                if name1 == "denis":
                    print("End:    "+
                        str(scores[name1]) + "   " + name1 + "      -----       " +name2)

                #print(f"{name1} vs {name2} => {s1}:{s2}")
    i = 1
    print("\n Final Scores:")
    for name, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        print(f"{i} {name}: {score}")
        i+= 1

if __name__ == "__main__":
    folder_path = "Algorithms" 
    default_rounds = 100

    print("=== ROUND 1: 100 games each ===")
    start = time.time()
    run_tournament(folder_path, rounds=default_rounds)
    end = time.time()
    print(f"time taken for first round {end-start}")

    print("\n=== ROUND 2: Random custom number of games ===")
    custom_rounds = int(input("Enter number of rounds for next tournament: "))
    start = time.time()
    run_tournament(folder_path, rounds=None, custom=custom_rounds)
    end = time.time()
    print(f"time taken for second round {end-start}")