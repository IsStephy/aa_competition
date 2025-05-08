def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> \
tuple[int, int]:

    # Get the current history with this opponent
    my_moves = my_history.get(opponent_id, [])
    opp_moves = opponents_history.get(opponent_id, [])

    # MOVE DETERMINATION LOGIC
    # First move against a new opponent
    if not opp_moves:
        move = 1
    # Initial few moves - mirror opponent's last move
    elif len(opp_moves) < 5:
        move = opp_moves[-1]
    else:
        # Analyze opponent's recent behavior
        last_10 = opp_moves[-10:] if len(opp_moves) >= 10 else opp_moves
        opp_coop_rate = sum(last_10) / len(last_10)

        # Check for defection streaks
        defect_streak = 0
        current_streak = 0
        for m in last_10:
            if m == 0:
                current_streak += 1
                defect_streak = max(defect_streak, current_streak)
            else:
                current_streak = 0

        # Retaliate against frequent defectors
        if opp_coop_rate < 0.3 or defect_streak >= 3:
            move = 0
        # Cooperate with cooperative opponents
        elif opp_coop_rate > 0.7:
            move = 1
        # Look for alternating patterns
        elif len(opp_moves) > 15:
            recent = opp_moves[-15:]
            alternations = sum(1 for i in range(1, len(recent)) if recent[i] != recent[i - 1])
            if alternations > 10:
                move = 0 if opp_moves[-1] == 1 else 1
            # Occasional cooperation after a streak of defection
            elif len(my_moves) > 8 and sum(my_moves[-8:]) == 0:
                move = 1
            # Default behavior: mirror with occasional cooperation
            else:
                move = opp_moves[-1] if (len(my_moves) % 4 != 0) else 1
        # Occasional cooperation after a streak of defection
        elif len(my_moves) > 8 and sum(my_moves[-8:]) == 0:
            move = 1
        # Default behavior: mirror with occasional cooperation
        else:
            move = opp_moves[-1] if (len(my_moves) % 4 != 0) else 1

    # OPPONENT SELECTION LOGIC
    # Maximum rounds allowed per opponent
    MAX_ROUNDS = 200

    # Calculate cooperation rates and average points for each opponent
    opponent_scores = {}
    for opp_id in opponents_history.keys():
        # Skip opponents we've already played maximum rounds with
        if len(my_history.get(opp_id, [])) >= MAX_ROUNDS:
            continue

        opp_history = opponents_history.get(opp_id, [])
        my_history_with_opp = my_history.get(opp_id, [])

        # For opponents we haven't played with yet, give them a slightly positive score
        if not opp_history:
            opponent_scores[opp_id] = 0.5
            continue

        # Calculate cooperation rate
        coop_rate = sum(opp_history) / len(opp_history)

        # Calculate average points earned from this opponent
        points = 0
        for i in range(len(my_history_with_opp)):
            if my_history_with_opp[i] == 1 and opp_history[i] == 1:  # Both cooperate
                points += 3
            elif my_history_with_opp[i] == 0 and opp_history[i] == 1:  # I defect, they cooperate
                points += 5
            elif my_history_with_opp[i] == 0 and opp_history[i] == 0:  # Both defect
                points += 1
            # If I cooperate and they defect, I get 0 points

        avg_points = points / len(my_history_with_opp)

        # Score combines cooperation rate and average points
        # We prefer opponents who give us more points on average
        opponent_scores[opp_id] = avg_points * 0.7 + coop_rate * 0.3

    # If we have no valid opponents left, return the current one
    if not opponent_scores:
        next_opponent = opponent_id
    else:
        # Return the opponent with the highest score
        next_opponent = max(opponent_scores, key=opponent_scores.get)

    return move, next_opponent