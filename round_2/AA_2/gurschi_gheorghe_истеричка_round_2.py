def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    opponent_moves = opponents_history.get(opponent_id, [])
    my_moves = my_history.get(opponent_id, [])
    
    cooperation_rates = {}
    for oid, moves in opponents_history.items():
        if moves:
            cooperation_rates[oid] = moves.count(1) / len(moves)
        else:
            cooperation_rates[oid] = 0.5
    
    if not opponent_moves:
        move = 1
    elif opponent_moves[-1] == 0 and len(opponent_moves) >= 2 and opponent_moves[-2] == 0:
        move = 0
    elif len(opponent_moves) >= 5:
        opp_coop_rate = opponent_moves.count(1) / len(opponent_moves)
        
        if opp_coop_rate < 0.3:
            move = 1 if len(my_moves) % 5 == 0 else 0
        elif opp_coop_rate > 0.7:
            move = 0 if len(my_moves) % 7 == 0 else 1
        else:
            if len(opponent_moves) >= 3 and all(m == 1 for m in opponent_moves[-3:]):
                move = 1
            else:
                move = opponent_moves[-1]
    else:
        move = opponent_moves[-1]
    
    available_opponents = [oid for oid, moves in my_history.items() if len(moves) < 200]
    
    if not available_opponents:
        next_opponent = opponent_id
    else:
        sorted_opponents = sorted(available_opponents, 
                                 key=lambda oid: cooperation_rates.get(oid, 0.5),
                                 reverse=True)
        
        next_opponent = sorted_opponents[0]
        
        unexplored = [oid for oid in available_opponents if oid not in my_history or not my_history[oid]]
        if unexplored and len(my_history) % 10 == 0:
            next_opponent = unexplored[0]
    
    return move, next_opponent