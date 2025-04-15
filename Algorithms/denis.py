<<<<<<< HEAD
def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    if not opponent_history:
        return 1  # Start friendly

    r = len(my_history)
    opp_coop = opponent_history.count(1)
    opp_defect = r - opp_coop
    coop_rate = opp_coop / r

    # --- Scoring-based greed mode ---
    score = 0
    for my, op in zip(my_history, opponent_history):
        if my == 1 and op == 1:
            score += 3
        elif my == 0 and op == 1:
            score += 5
        elif my == 0 and op == 0:
            score += 1
    avg_score = score / r

    # --- Endgame farming logic ---
    if rounds is not None and r >= rounds - 3:
        if coop_rate > 0.6:
            return 0  # Farm the nice ones
        if avg_score < 2:
            return 0  # Too risky, play selfish

    # --- Betrayal pattern detection ---
    if len(opponent_history) >= 3 and opponent_history[-3:] == [1, 1, 0]:
        return 0  # Punish fake cooperation

    # --- Detect tit-for-tat or mirrored types ---
    def is_tit_for_tat():
        if len(opponent_history) < 3 or opponent_history[0] != 1:
            return False
        return all(opponent_history[i] == my_history[i - 1] for i in range(1, r))

    if is_tit_for_tat():
        return 1  # Exploit the mutual trust

    # --- Betrayal spike detection (last 5 moves) ---
    recent = opponent_history[-5:] if r >= 5 else opponent_history
    recent_betray = recent.count(0) / len(recent)
    if recent_betray > 0.6:
        return 0  # Aggro

    # --- Adaptive Trust Evolution ---
    if coop_rate > 0.7:
        return 1  # Maximize points vs friendly players
    elif coop_rate < 0.4 or avg_score < 2.1:
        return 0  # You're losing, get greedy

    # --- Controlled mirror fallback with revenge memory ---
    if len(opponent_history) >= 2:
        if opponent_history[-1] == 0 and opponent_history[-2] == 0:
            return 0  # Double stab, no mercy
        elif opponent_history[-1] == 1 and my_history[-1] == 1:
            return 1  # Continue peace

    return opponent_history[-1]  # Basic mirror as fallback
=======
def strategy(my_history, opponent_history, rounds):
    if not opponent_history:
        return 1  # Cooperate first

    current_round = len(my_history)

    # --- Defect in the final round ---
    if rounds is not None and current_round == rounds - 1:
        return 0  # Defect in the final round

    # --- Early Punishment for Frequent Betrayal ---
    betrayal_count = opponent_history.count(0)
    if betrayal_count >= 3:  # If opponent defects 3 times in total, punish
        return 0

    # --- Immediate Retaliation to Recent Betrayal ---
    if current_round >= 3 and opponent_history[-3:] == [0, 0, 0]:
        return 0  # Punish after 3 consecutive defections

    # --- Punish if opponent defects after cooperation ---
    if current_round >= 2 and my_history[-2:] == [1, 1] and opponent_history[-2:] == [1, 0]:
        return 0  # Retaliate if the opponent defects after we cooperated

    # --- Cooperative Forgiveness with Pattern Detection ---
    # Forgive if opponent cooperates after a defection (attempt to restore cooperation)
    if current_round >= 4 and opponent_history[-4:] == [1, 0, 1, 0]:
        return 1  # Restore cooperation after minor defection patterns

    # --- Strategic Cooperation Based on Betrayal Rate ---
    betrayal_rate = opponent_history.count(0) / len(opponent_history)
    if betrayal_rate < 0.3:
        return 1  # Cooperate if betrayal is below 30% of the total moves

    # --- Adaptive Punishment Based on Betrayal Evolution ---
    if betrayal_rate > 0.5:  # Increase defection if betrayal rate is higher than 50%
        return 0

    # --- Default: Cooperate if no defection detected ---
    return 1  # Default behavior: cooperate
>>>>>>> abc990e81ef04e0bbb4e2266f3641bedb1a15709
