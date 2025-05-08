def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:

  
    max_rounds_per_opponent = 200
    all_opponents = set(opponents_history.keys())
    
    def opponent_type(opp_moves: list[int], my_moves: list[int]) -> str:
        if not opp_moves:
            return "unknown"
        coop_rate = sum(opp_moves) / len(opp_moves)
        if coop_rate < 0.3:
            return "exploiter"
        elif abs(sum(opp_moves) - sum(my_moves)) <= 2:
            return "mirror"
        else:
            return "random"
    
    def choose_move(opp_moves: list[int], my_moves: list[int]) -> int:
        o_type = opponent_type(opp_moves, my_moves)
        if o_type == "exploiter":
            return 0
        elif o_type == "mirror":
            quantum_state = (sum(my_moves) * len(opp_moves)) % 7
            return 1 if quantum_state > 3 else 0
        else:
            last_three = opp_moves[-3:] if len(opp_moves) >= 3 else [1]
            return 0 if sum(last_three) == 0 else 1
    
    current_my_moves = my_history.get(opponent_id, [])
    current_opp_moves = opponents_history.get(opponent_id, [])
    move = choose_move(current_opp_moves, current_my_moves)
    
    possible_opponents = [op_id for op_id in all_opponents if len(my_history.get(op_id, [])) < max_rounds_per_opponent]
    
    if not possible_opponents:
        next_opponent = opponent_id  
    else:
        best_opponent = opponent_id
        best_coop_rate = -1
        
        for op_id in possible_opponents:
            opp_moves = opponents_history.get(op_id, [])
            if opp_moves:
                coop_rate = sum(opp_moves) / len(opp_moves)
            else:
                coop_rate = 1  # if no moves => friendly
            
            if coop_rate > best_coop_rate:
                best_coop_rate = coop_rate
                best_opponent = op_id
        
        next_opponent = best_opponent
    
    return move, next_opponent
