def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    """
    Simple Baseline Plus - A straightforward strategy that cooperates initially
    and adapts based on opponent's cooperation rate and recent behavior.

    Parameters:
        my_history (list[int]): List of player's past moves (0=defect, 1=cooperate)
        opponent_history (list[int]): List of opponent's past moves (0=defect, 1=cooperate)
        rounds (int | None): Total number of rounds to be played or None if unknown

    Returns:
        int: 0 for defection or 1 for cooperation
    """
    # First move: always cooperate
    if not opponent_history:
        return 1

    current_round = len(my_history)

    # End-game strategy if rounds are known
    if rounds is not None and current_round >= rounds - 3:
        return 0  # Defect in the final 3 rounds

    # Calculate opponent's cooperation rate
    coop_rate = sum(opponent_history) / len(opponent_history)

    # Check recent behavior (last 3 moves)
    recent_window = min(3, len(opponent_history))
    recent_defections = recent_window - sum(opponent_history[-recent_window:])

    # If opponent has defected in the last two consecutive rounds, defect
    if len(opponent_history) >= 2 and opponent_history[-1] == 0 and opponent_history[-2] == 0:
        return 0

    # If opponent has been mostly cooperative (>70%), cooperate most of the time
    if coop_rate > 0.7:
        # Occasionally defect to avoid being too predictable
        if current_round % 7 == 0:
            return 0
        return 1

    # If opponent has been mostly defecting (<30%), defect
    if coop_rate < 0.3:
        return 0

    # In the middle ground, mirror opponent's last move
    return opponent_history[-1]