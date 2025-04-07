def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    if not my_history:
        return 1  # Start with cooperation

    r = len(my_history)

    # --- Score tracking ---
    score = 0
    for m, o in zip(my_history, opponent_history):
        if m == 1 and o == 1:
            score += 3
        elif m == 0 and o == 1:
            score += 5
        elif m == 0 and o == 0:
            score += 1
    avg_score = score / r

    # --- Betrayal detection ---
    betrayal_total = opponent_history.count(0)
    betrayal_ratio = betrayal_total / r

    recent_window = 5 if r >= 5 else r
    recent = opponent_history[-recent_window:]
    recent_betrayals = recent.count(0) / recent_window if recent_window else 0

    # --- Endgame farming ---
    if rounds is not None and r >= rounds - 2:
        return 0

    # --- If they're always defecting, return 0 always
    if r >= 6 and opponent_history[-6:] == [0, 0, 0, 0, 0, 0]:
        return 0

    # --- If they're always cooperating, farm them
    if r >= 5 and opponent_history[-5:] == [1, 1, 1, 1, 1]:
        return 0

    # --- Tit-for-Tat detection ---
    if r >= 2 and all(opponent_history[i] == my_history[i - 1] for i in range(1, r)):
        return 1

    # --- If recent betrayal spike or we’re not scoring well, switch to defense ---
    if recent_betrayals >= 0.5 or avg_score < 2.3:
        return 0

    # --- Mirror last move if it worked ---
    if my_history[-1] == opponent_history[-1]:
        return my_history[-1]

    # --- Forgive if opponent came back to cooperation ---
    if opponent_history[-1] == 1 and opponent_history[-2] == 0:
        return 1

    # --- Default: mirror opponent ---
    return opponent_history[-1]
