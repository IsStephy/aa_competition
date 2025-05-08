import os
import importlib.util
import csv
import random
import traceback
import sys
from statistics import mean

MAX_TOTAL_ROUNDS = 1000
MAX_ROUNDS_PER_OPPONENT = 200
NUM_RUNS = 10

def compute_score(a, b):
    if a == 1 and b == 1:
        return 3, 3
    elif a == 0 and b == 0:
        return 1, 1
    elif a == 1 and b == 0:
        return 0, 5
    else:
        return 5, 0

def load_strategies(folder):
    strategies = {}
    id_to_name = {}
    name_to_id = {}
    index = 1
    for filename in sorted(os.listdir(folder)):
        if filename.endswith(".py"):
            strategy_name = filename.replace(".py", "")
            path = os.path.join(folder, filename)
            module_name = f"mod_{strategy_name.replace('.', '_')}"
            spec = importlib.util.spec_from_file_location(module_name, path)
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
                if hasattr(module, "strategy_round_2"):
                    strategies[index] = module.strategy_round_2
                    id_to_name[index] = strategy_name
                    name_to_id[strategy_name] = index
                    index += 1
                else:
                    print(f"[ERROR] {strategy_name} has no 'strategy_round_2'")
            except Exception as e:
                print(f"[ERROR] Failed to load {strategy_name}")
                traceback.print_exc()
                with open("crash_log.txt", "a", encoding="utf-8") as log:
                    log.write(f"\n[LOADING ERROR] {strategy_name}:\n")
                    traceback.print_exc(file=log)
    return strategies, id_to_name, name_to_id

def simulate_as_main(main_id, main_func, strategies):
    all_ids = list(strategies.keys())
    opponents = {k: v for k, v in strategies.items() if k != main_id}
    my_history = {k: [] for k in all_ids if k != main_id}
    opponents_history = {k: [] for k in all_ids if k != main_id}
    score = 0
    friendly_scores = {k: 0 for k in all_ids if k != main_id}
    round_log = []
    pairwise = {k: [0, 0, 0] for k in all_ids if k != main_id}  # opponent_id: [rounds, my_score, their_score]
    rounds_played = 0
    current_opponent = random.choice(list(opponents))

    while rounds_played < MAX_TOTAL_ROUNDS:
        if len(my_history[current_opponent]) >= MAX_ROUNDS_PER_OPPONENT:
            available = [i for i in my_history if len(my_history[i]) < MAX_ROUNDS_PER_OPPONENT]
            if not available:
                break
            current_opponent = random.choice(available)

        try:
            move, next_opponent = main_func(current_opponent, my_history, opponents_history)
        except Exception:
            print(f"[ERROR] Strategy {main_id} crashed on round {rounds_played}")
            traceback.print_exc()
            with open("crash_log.txt", "a", encoding="utf-8") as log:
                log.write(f"\n[MAIN CRASH] strategy {main_id} vs {current_opponent}:\n")
                traceback.print_exc(file=log)
            break

        opp_my_history = {k: [] for k in strategies if k != current_opponent}
        opp_opp_history = {k: [] for k in strategies if k != current_opponent}
        opp_my_history[main_id] = opponents_history[current_opponent]
        opp_opp_history[main_id] = my_history[current_opponent]

        try:
            opp_func = opponents[current_opponent]
            opp_move, _ = opp_func(main_id, opp_my_history, opp_opp_history)
        except Exception:
            print(f"[ERROR] Opponent {current_opponent} crashed when called by {main_id}")
            traceback.print_exc()
            with open("crash_log.txt", "a", encoding="utf-8") as log:
                log.write(f"\n[OPPONENT CRASH] {current_opponent} (vs {main_id}):\n")
                traceback.print_exc(file=log)
            opp_move = 0

        my_history[current_opponent].append(move)
        opponents_history[current_opponent].append(opp_move)

        my_points, opp_points = compute_score(move, opp_move)
        score += my_points
        friendly_scores[current_opponent] += opp_points
        pairwise[current_opponent][0] += 1
        pairwise[current_opponent][1] += my_points
        pairwise[current_opponent][2] += opp_points

        rounds_played += 1
        round_log.append((main_id, current_opponent, rounds_played, move, opp_move))

        if next_opponent in my_history and len(my_history[next_opponent]) < MAX_ROUNDS_PER_OPPONENT:
            current_opponent = next_opponent
        else:
            remaining = [k for k in my_history if len(my_history[k]) < MAX_ROUNDS_PER_OPPONENT]
            if remaining:
                current_opponent = random.choice(remaining)
            else:
                break

    return score, friendly_scores, round_log, pairwise

def run_tournament(folder):
    strategies, id_to_name, _ = load_strategies(folder)
    main_scores_runs = {k: [] for k in strategies}
    friendly_totals = {k: 0 for k in strategies}
    all_logs = []
    pairwise_stats = []

    for main_id, main_func in strategies.items():
        print(f"[RUNNING] {id_to_name[main_id]} (ID={main_id}) as main...")
        for _ in range(NUM_RUNS):
            score, friendly, logs, pairwise = simulate_as_main(main_id, main_func, strategies)
            main_scores_runs[main_id].append(score)
            for opp_id, points in friendly.items():
                friendly_totals[opp_id] += points
            all_logs.extend(logs)
            for opp_id, (rounds, main_pts, opp_pts) in pairwise.items():
                if rounds > 0:
                    pairwise_stats.append([
                        main_id, id_to_name[main_id],
                        opp_id, id_to_name[opp_id],
                        rounds,
                        main_pts, round(main_pts / rounds, 2),
                        opp_pts, round(opp_pts / rounds, 2)
                    ])

    with open("main_scores.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["strategy_id", "strategy_name", "avg_main_score"])
        for k, runs in main_scores_runs.items():
            writer.writerow([k, id_to_name[k], round(mean(runs))])

    with open("friendly_scores.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["strategy_id", "strategy_name", "friendly_score"])
        for k, v in friendly_totals.items():
            writer.writerow([k, id_to_name[k], round(v / NUM_RUNS)])

    with open("round_history.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["main_id", "opponent_id", "round", "main_move", "opponent_move"])
        for row in all_logs:
            writer.writerow(row)

    with open("pairwise_stats.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "main_id", "main_name",
            "opponent_id", "opponent_name",
            "rounds_played",
            "main_total_score", "main_avg_per_round",
            "opponent_total_score", "opponent_avg_per_round"
        ])
        writer.writerows(pairwise_stats)

    print("\n✅ Tournament complete. Results written to CSV files.")

if __name__ == "__main__":
    run_tournament("AA_2")
