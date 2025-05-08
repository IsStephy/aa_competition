def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], 
                    opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    # Calculate current move against opponent_id
    # If first round with this opponent, cooperate
    if not opponents_history[opponent_id]:
        current_move = 1
    # If last possible round with this opponent, defect
    elif len(my_history[opponent_id]) == 199:  # 0-indexed, so 199 is the 200th round
        current_move = 0
    else:
        # Adaptive tit-for-tat logic
        lookback = 5
        recent_moves = opponents_history[opponent_id][-lookback:] if opponents_history[opponent_id] else []
        if recent_moves:
            defects = len(recent_moves) - sum(recent_moves)
            if defects / len(recent_moves) > 0.4:
                current_move = 0
            elif opponents_history[opponent_id][-1] == 0:
                if len(opponents_history[opponent_id]) >= 3 and sum(opponents_history[opponent_id][-3:]) >= 2:
                    current_move = 1
                else:
                    current_move = 0
            else:
                current_move = 1
        else:
            current_move = 1
    
    # Select next opponent based on cooperation rates
    cooperation_rates = {}
    for opponent, history in opponents_history.items():
        if len(history) > 0 and len(my_history[opponent]) < 200:  # Only consider opponents we haven't maxed out
            cooperation_rates[opponent] = sum(history) / len(history)
    
    # If we have cooperation data, choose the most cooperative opponent
    if cooperation_rates:
        next_opponent = max(cooperation_rates.items(), key=lambda x: x[1])[0]
    # Otherwise, choose the first available opponent
    else:
        for opponent in opponents_history:
            if len(my_history[opponent]) < 200:
                next_opponent = opponent
                break
        else:  # If all opponents have reached max rounds (shouldn't happen in practice)
            next_opponent = opponent_id  # Fallback to current opponent
    
    return (current_move, next_opponent)
