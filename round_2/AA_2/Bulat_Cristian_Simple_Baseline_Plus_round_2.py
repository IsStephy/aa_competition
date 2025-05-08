def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]],
                     opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    """
    Simple Baseline Plus - A strategy that cooperates initially and adapts based on
    opponent's cooperation rate and recent behavior. Also selects next opponents strategically.

    Parameters:
        opponent_id (int): ID of the current opponent
        my_history (dict[int, list[int]]): Dictionary of player's past moves against each opponent
        opponents_history (dict[int, list[int]]): Dictionary of opponents' past moves against the player

    Returns:
        tuple[int, int]: (move, next_opponent) where move is 0 for defect or 1 for cooperate,
                         and next_opponent is the ID of the next opponent to play against
    """
    # Get current opponent's history
    current_opp_history = opponents_history.get(opponent_id, [])
    my_moves_vs_current = my_history.get(opponent_id, [])

    # DECIDE MOVE
    # First move against this opponent: always cooperate
    if not current_opp_history:
        move = 1
    else:
        # Calculate opponent's cooperation rate
        coop_rate = sum(current_opp_history) / len(current_opp_history)
        current_round = len(my_moves_vs_current)

        # If opponent has defected in the last two consecutive rounds, defect
        if len(current_opp_history) >= 2 and current_opp_history[-1] == 0 and current_opp_history[-2] == 0:
            move = 0
        # If opponent has been mostly cooperative (>70%), cooperate most of the time
        elif coop_rate > 0.7:
            # Occasionally defect to avoid being too predictable
            if current_round % 7 == 0:
                move = 0
            else:
                move = 1
        # If opponent has been mostly defecting (<30%), defect
        elif coop_rate < 0.3:
            move = 0
        # In the middle ground, mirror opponent's last move
        else:
            move = current_opp_history[-1]

    # SELECT NEXT OPPONENT
    # Find valid opponents (those with whom we've played fewer than 200 rounds)
    valid_opponents = {}
    for opp_id in opponents_history:
        # Check if we've played with this opponent
        rounds_played = len(my_history.get(opp_id, []))
        if rounds_played < 200:
            opp_moves = opponents_history.get(opp_id, [])
            if opp_moves:
                # Calculate cooperation rate for this opponent
                valid_opponents[opp_id] = sum(opp_moves) / len(opp_moves)
            else:
                # No history yet, assign neutral value
                valid_opponents[opp_id] = 0.5

    # If no valid opponents, stick with current if possible
    if not valid_opponents:
        # Check if current opponent is still valid
        current_rounds_played = len(my_history.get(opponent_id, []))
        if current_rounds_played < 200:
            return move, opponent_id
        # Otherwise, try to find any valid opponent
        for opp_id in opponents_history:
            rounds_played = len(my_history.get(opp_id, []))
            if rounds_played < 200:
                return move, opp_id
        # If all are maxed out, return current (tournament shouldn't reach this)
        return move, opponent_id

    # Sort opponents by cooperation rate (highest first) and choose the most cooperative
    sorted_opponents = sorted(valid_opponents.items(), key=lambda x: x[1], reverse=True)
    next_opponent = sorted_opponents[0][0]

    return move, next_opponent