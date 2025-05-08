def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], 
                   opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    """
    A strategy for the second round of the Iterated Prisoner's Dilemma tournament.
    
    Parameters:
    - opponent_id: ID of the current opponent
    - my_history: Dictionary mapping opponent IDs to lists of my past moves against them
    - opponents_history: Dictionary mapping opponent IDs to lists of their past moves against me
    
    Returns:
    - Tuple of (move, next_opponent) where:
        - move: 0 (defect) or 1 (cooperate)
        - next_opponent: ID of the next opponent to play against
    """
    # Get all available opponent IDs
    all_opponents = list(my_history.keys())
    
    # 1. ANALYZE OPPONENTS' BEHAVIORS
    cooperation_rates = {}
    expected_values = {}
    
    for opp_id in all_opponents:
        # Skip opponents we've already played 200 rounds with
        if len(my_history[opp_id]) >= 200:
            continue
            
        # Calculate cooperation rate for opponents we've played with before
        if len(opponents_history[opp_id]) > 0:
            cooperation_rates[opp_id] = sum(opponents_history[opp_id]) / len(opponents_history[opp_id])
            
            # Calculate expected value of playing with this opponent based on history
            total_points = 0
            for my_move, opp_move in zip(my_history[opp_id], opponents_history[opp_id]):
                if my_move == 1 and opp_move == 1:  # Both cooperate
                    total_points += 3
                elif my_move == 0 and opp_move == 1:  # I defect, they cooperate
                    total_points += 5
                elif my_move == 1 and opp_move == 0:  # I cooperate, they defect
                    total_points += 0
                else:  # Both defect
                    total_points += 1
                    
            expected_values[opp_id] = total_points / len(my_history[opp_id])
        else:
            # For opponents we haven't played with, assign neutral values
            cooperation_rates[opp_id] = 0.5
            expected_values[opp_id] = 2.5  # Midpoint between worst (0) and best (5)
    
    # 2. DETERMINE CURRENT MOVE
    current_move = 1  # Default to cooperation
    
    # If we have history with current opponent
    if opponents_history[opponent_id]:
        opp_coop_rate = cooperation_rates[opponent_id]
        
        # Implement a conditional strategy
        if len(opponents_history[opponent_id]) < 5:
            # In the first few rounds, be nice to establish cooperation
            current_move = 1
        elif opp_coop_rate > 0.7:
            # If opponent is highly cooperative, occasionally defect to exploit
            if len(my_history[opponent_id]) % 7 == 0:
                current_move = 0
            else:
                current_move = 1
        elif opp_coop_rate > 0.4:
            # For moderately cooperative opponents, use tit-for-tat
            current_move = opponents_history[opponent_id][-1]
        else:
            # For mostly defecting opponents, mostly defect but occasionally cooperate
            # to test if they might change behavior
            if len(my_history[opponent_id]) % 5 == 0:
                current_move = 1
            else:
                current_move = 0
    
    # 3. SELECT NEXT OPPONENT
    next_opponent = opponent_id  # Default to continuing with current opponent
    
    # Identify opponents we haven't maxed out rounds with
    available_opponents = [op_id for op_id in all_opponents if len(my_history[op_id]) < 200]
    
    if not available_opponents:
        # If we've maxed out all opponents, just continue with current one
        next_opponent = opponent_id
    else:
        # Try to find the most profitable opponent
        if expected_values:
            # Get the opponent with highest expected value
            best_opponent = max(expected_values, key=expected_values.get)
            
            # If current opponent is highly profitable, stick with them
            if (opponent_id in expected_values and 
                expected_values[opponent_id] > 3.0 and 
                len(my_history[opponent_id]) < 200):
                next_opponent = opponent_id
            else:
                next_opponent = best_opponent
        else:
            # If no history yet, try someone new
            for op_id in available_opponents:
                if len(my_history[op_id]) == 0:
                    next_opponent = op_id
                    break
    
    # Ensure we're not exceeding max rounds with any opponent
    if len(my_history[next_opponent]) >= 200:
        # Find any opponent we haven't maxed out
        for alt_id in available_opponents:
            if alt_id != next_opponent:
                next_opponent = alt_id
                break
    
    return (current_move, next_opponent)