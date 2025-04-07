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
