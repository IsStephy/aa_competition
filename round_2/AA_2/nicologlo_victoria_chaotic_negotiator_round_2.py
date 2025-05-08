def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> \
tuple[int, int]:
    # Initial moves sequence (cooperate, defect, cooperate)
    if opponent_id not in my_history or len(my_history[opponent_id]) < 3:
        initial_moves = [1, 0, 1]
        move = initial_moves[len(my_history.get(opponent_id, []))] if len(my_history.get(opponent_id, [])) < 3 else 1
        return (move, opponent_id)  # Stay with same opponent initially

    # Get current opponent's history
    current_opponent_moves = opponents_history[opponent_id]
    my_moves_with_opponent = my_history[opponent_id]
    rounds_played = len(my_moves_with_opponent)

    # Analysis phase (first 20% of max rounds with this opponent)
    if rounds_played < 40:  # 20% of max 200 rounds
        trust_score = sum(current_opponent_moves) / len(current_opponent_moves)
        if (rounds_played % 7 == 0) and (trust_score > 0.6):
            move = 0  # Occasional betrayal
        else:
            move = 1 if trust_score > 0.5 else 0
    else:
        # Main phase: dynamic adaptation
        recent_moves = current_opponent_moves[-5:] if len(current_opponent_moves) >= 5 else current_opponent_moves
        opponent_trend = sum(recent_moves) / len(recent_moves) if recent_moves else 0.5

        if opponent_trend < 0.3:  # Aggressive opponent
            move = 0 if (rounds_played % 10 != 0) else 1  # 10% forgiveness
        elif 0.3 <= opponent_trend <= 0.7:  # Unpredictable opponent
            move = 1 if ((rounds_played * 13) % 100) < 55 else 0
        else:  # Cooperative opponent
            move = 0 if (rounds_played % 8 == 0) else 1  # 12.5% betrayal rate

    # Select next opponent
    # First, find all opponents we haven't played with yet
    all_opponent_ids = set(opponents_history.keys())
    played_opponents = set(my_history.keys())
    unplayed_opponents = list(all_opponent_ids - played_opponents)

    if unplayed_opponents:
        # Explore new opponents first
        next_opponent = unplayed_opponents[0]
    else:
        # Find the most cooperative opponent we haven't maxed out rounds with
        cooperation_scores = {}
        for opp_id in all_opponent_ids:
            if len(my_history.get(opp_id, [])) < 200:  # Haven't reached max rounds
                if opp_id in opponents_history and len(opponents_history[opp_id]) > 0:
                    cooperation_scores[opp_id] = sum(opponents_history[opp_id]) / len(opponents_history[opp_id])
                else:
                    cooperation_scores[opp_id] = 0.5  # Default score for unknown

        if cooperation_scores:
            # Choose opponent with highest cooperation score
            next_opponent = max(cooperation_scores.keys(), key=lambda x: cooperation_scores[x])
        else:
            # Fallback - stay with current opponent if no better options
            next_opponent = opponent_id

    return (move, next_opponent)