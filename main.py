import os
import importlib.util
import random
import time
import csv
import tkinter as tk
from tkinter import ttk

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

# Run tournament and export results step by step
def run_tournament_step_by_step(folder, round_name="round", rounds=100, update_callback=None):
    strategies = load_strategies(folder)
    scores = {name: 0 for name in strategies}
    win_stats = {name: {"wins": 0, "total": 0} for name in strategies}
    match_results = []

    names = list(strategies.keys())
    def play_and_update(i):
        if i < len(names):
            name1 = names[i]
            # Play matches against all other strategies
            for j in range(len(names)):
                if i != j:
                    name2 = names[j]
                    s1, s2, h1, h2 = play_match(strategies[name1], strategies[name2], rounds)

                    scores[name1] += s1
                    win_stats[name1]["total"] += 1

                    if s1 > s2:
                        win_stats[name1]["wins"] += 1

                    match_results.append([name1, name2, s1, s2, h1, h2])

            # Update leaderboard after the algorithm has played with all others
            if update_callback:
                update_callback(scores, win_stats)

            # Wait for 1 second before moving to the next algorithm
            root.after(1000, lambda: play_and_update(i + 1))

    # Start the step-by-step tournament
    play_and_update(0)

# Update leaderboard with alternating row colors
def update_leaderboard(scores, win_stats, leaderboard):
    leaderboard.delete(*leaderboard.get_children())
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for idx, (name, score) in enumerate(sorted_scores):
        wins = win_stats[name]["wins"]
        total = win_stats[name]["total"]
        win_ratio = round(wins / total, 4) if total > 0 else 0

        # Alternate row colors based on the index (even/odd)
        row_color = "#f9eac2" if idx % 2 == 0 else "#c2e3f9"
        
        leaderboard.insert('', 'end', values=(name, score, wins, total, f"{win_ratio*100:.2f}%"), tags=(row_color,))

    # Apply alternating row colors
    leaderboard.tag_configure("#f9eac2", background="#f9eac2")
    leaderboard.tag_configure("#c2e3f9", background="#c2e3f9")

# Start tournament when button is pressed
def start_tournament():
    folder_path = "AA_Tournament"
    default_rounds = 100

    # Run tournament and get results step by step
    print("=== Running Tournament Step by Step ===")
    run_tournament_step_by_step(folder_path, round_name="round1", rounds=default_rounds, update_callback=lambda scores, win_stats: update_leaderboard(scores, win_stats, leaderboard))

# Create the Tkinter interface
root = tk.Tk()
root.title("Tournament Leaderboard")

# Set full screen
root.attributes('-fullscreen', True)
root.configure(bg='white')

# Frame for leaderboard
frame = ttk.Frame(root)
frame.pack(padx=10, pady=10, fill='both', expand=True)

# Leaderboard table
leaderboard = ttk.Treeview(frame, columns=("Name", "Score", "Wins", "Matches", "Win Ratio"), show="headings")
leaderboard.heading("Name", text="Name")
leaderboard.heading("Score", text="Score")
leaderboard.heading("Wins", text="Wins")
leaderboard.heading("Matches", text="Matches")
leaderboard.heading("Win Ratio", text="Win Ratio")
leaderboard.pack(fill='both', expand=True)

# Start button
start_button = ttk.Button(root, text="Start Tournament", command=start_tournament)
start_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
