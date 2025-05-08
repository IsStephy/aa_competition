def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:

    current_opponent_history = opponents_history.get(opponent_id, [])
    my_history_with_opponent = my_history.get(opponent_id, [])
    
    defection_count = 0
    for move in current_opponent_history:
        if move == 0:
            defection_count += 1
        else:
            defection_count = max(0, defection_count - 0.5)
    
    combined_history = str(my_history_with_opponent[-20:]) + str(current_opponent_history[-20:])
    total = hash(combined_history)
    
    move = 1
    
    if hash(total * 663937) % 17 == 0:
        move = 0
    
    elif defection_count >= 1:
        recent_history = str(my_history_with_opponent[-5:]) + str(current_opponent_history[-5:])
        total_recent = hash(recent_history)
        if (total_recent % 3) == 0:
            move = 0
    

    all_opponents = set(opponents_history.keys())
    
    eligible_opponents = [op_id for op_id in all_opponents 
                         if len(my_history.get(op_id, [])) < 200]
    
    if opponent_id in eligible_opponents and len(my_history.get(opponent_id, [])) >= 199:  # 199 because we're about to add one more
        eligible_opponents.remove(opponent_id)
    
    if not eligible_opponents:
        return (move, next(iter(all_opponents)))
    
    unplayed_opponents = [op_id for op_id in eligible_opponents 
                         if not opponents_history.get(op_id, [])]
    
    if unplayed_opponents:
        selection_hash = hash(str(my_history) + str(opponent_id))
        next_opponent = unplayed_opponents[selection_hash % len(unplayed_opponents)]
    else:
        cooperation_rates = {}
        for op_id in eligible_opponents:
            history = opponents_history.get(op_id, [])
            if history:
                cooperation_rate = sum(history) / len(history)
                cooperation_rates[op_id] = cooperation_rate
        
        if opponent_id in cooperation_rates and hash(str(my_history) + str(opponents_history)) % 5 == 0:
            next_opponent = opponent_id
        elif cooperation_rates:
            sorted_opponents = sorted(cooperation_rates.items(), key=lambda x: x[1], reverse=True)
            next_opponent = sorted_opponents[0][0]
        else:
            selection_hash = hash(str(my_history) + str(opponent_id))
            next_opponent = eligible_opponents[selection_hash % len(eligible_opponents)]
    
    return (move, next_opponent)