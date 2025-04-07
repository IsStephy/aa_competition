import matplotlib.pyplot as plt

# --- Strategy Function ---
def exploit_with_coop(my_history, opponent_history, rounds=None):
    """
    Strategy: Begins with defection, learns opponent pattern, punishes defection,
    and offers minimal cooperation to stay ahead in scoring.
    """
    turn = len(my_history)

    if turn == 0:
        return 0

    if opponent_history[-1] == 0:
        return 0

    def detect_pattern(history, min_len=2, max_len=5):
        for pattern_len in range(min_len, min(max_len, len(history) // 2) + 1):
            pattern = history[-pattern_len:]
            if history[-2 * pattern_len:-pattern_len] == pattern:
                return pattern
        return None

    pattern = detect_pattern(opponent_history)
    if pattern:
        predicted_move = pattern[(turn) % len(pattern)]
        if predicted_move == 1:
            return 0
        else:
            return 1 if turn % 5 == 0 else 0

    return 1 if turn % 7 == 0 else 0

# --- Opponent Strategies ---
def always_cooperate(_, __):
    return 1

def always_defect(_, __):
    return 0

def tit_for_tat(_, opponent_history):
    return 1 if not opponent_history else opponent_history[-1]

def periodic_pattern(_, __):
    pattern = [1, 1, 0]
    return pattern[len(__) % len(pattern)]

# --- Simulation Logic ---
def simulate(opponent_strategy, total_rounds=60):
    my_history = []
    opponent_history = []

    for _ in range(total_rounds):
        opponent_move = opponent_strategy(my_history, opponent_history)
        my_move = exploit_with_coop(my_history, opponent_history)
        my_history.append(my_move)
        opponent_history.append(opponent_move)

    return my_history, opponent_history

# --- Display Round-by-Round Simulation ---
def print_game_simulation(name, my_history, opponent_history):
    print(f"\nSimulation vs {name}")
    print(f"{'Round':>5} | {'Me':>2} | {'Opponent':>8}")
    print("-" * 24)
    for i, (me, opp) in enumerate(zip(my_history, opponent_history), 1):
        print(f"{i:>5} | {me:>2} | {opp:>8}")
    print("-" * 24)
    print()

# --- Run and Display Simulations ---
strategies = {
    "Always Cooperate": always_cooperate,
    "Always Defect": always_defect,
    "Tit for Tat": tit_for_tat,
    "Periodic Pattern [1,1,0]": periodic_pattern
}

results = {}
rounds = 60

for name, strategy in strategies.items():
    my_hist, opp_hist = simulate(strategy, rounds)
    results[name] = (my_hist, opp_hist)
    print_game_simulation(name, my_hist, opp_hist)

# --- Plot Results ---
fig, axs = plt.subplots(len(results), 1, figsize=(12, 2.5 * len(results)), sharex=True)

for i, (name, (my_hist, opp_hist)) in enumerate(results.items()):
    axs[i].plot(my_hist, label="My Moves (0=Defect, 1=Coop)", marker='o', linestyle='-')
    axs[i].plot(opp_hist, label="Opponent Moves (0=Defect, 1=Coop)", marker='x', linestyle='--')
    axs[i].set_title(f"Strategy vs {name}")
    axs[i].set_yticks([0, 1])
    axs[i].set_yticklabels(["0", "1"])
    axs[i].legend(loc="upper right")
    axs[i].grid(True)

plt.xlabel("Round")
plt.tight_layout()
plt.show()
