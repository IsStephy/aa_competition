def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    my_moves_vs_current = my_history.get(opponent_id, [])
    opponent_moves = opponents_history.get(opponent_id, [])
    current_round = len(my_moves_vs_current)
    
    if not opponent_moves:
        next_move = 0
    else:
        opponent_coop_rate = sum(opponent_moves) / len(opponent_moves)
        recent_coop_rate = sum(opponent_moves[-5:]) / 5 if len(opponent_moves) >= 5 else opponent_coop_rate
        
        if current_round >= 197:
            next_move = 0
        elif opponent_coop_rate > 0.7:
            next_move = 0
        elif len(my_moves_vs_current) >= 5 and all(opponent_moves[i] == my_moves_vs_current[i-1] for i in range(1, 5)):
            if my_moves_vs_current[-1] == 1:
                next_move = 0
            else:
                next_move = 1
        elif recent_coop_rate < 0.3:
            next_move = 0
        elif recent_coop_rate > 0.5:
            if current_round % 3 != 0:
                next_move = 1
            else:
                next_move = 0
        else:
            next_move = 0
    
    opponent_scores = {}
    available_opponents = []
    
    for pid in opponents_history.keys():
        if len(my_history.get(pid, [])) >= 200:
            continue
        available_opponents.append(pid)
        
        if pid in opponents_history and opponents_history[pid]:
            moves = opponents_history[pid]
            my_moves = my_history.get(pid, [])
            coop_rate = sum(moves) / len(moves)
            points = 0
            rounds_played = min(len(moves), len(my_moves))
            
            for i in range(rounds_played):
                if my_moves[i] == 1 and moves[i] == 1:
                    points += 3
                elif my_moves[i] == 0 and moves[i] == 1:
                    points += 5
                elif my_moves[i] == 0 and moves[i] == 0:
                    points += 1
            
            expected_value = points / rounds_played if rounds_played > 0 else 0
            
            if coop_rate > 0.7:
                expected_value += 0.5
            

            is_tit_for_tat = True
            if len(my_moves) >= 5 and len(moves) >= 5:
                for i in range(1, 5):
                    if i < len(moves) and i-1 < len(my_moves) and moves[i] != my_moves[i-1]:
                        is_tit_for_tat = False
                        break
                
                if is_tit_for_tat:
                    expected_value += 0.3
            
            opponent_scores[pid] = expected_value
    
    if not available_opponents:
        return (next_move, opponent_id)
    
    for pid in opponents_history.keys():
        if pid not in opponent_scores and pid in available_opponents:
            opponent_scores[pid] = 2.0
    
    best_opponent = opponent_id
    highest_value = opponent_scores.get(opponent_id, 0)
    
    for pid in available_opponents:
        expected_value = opponent_scores.get(pid, 2.0)
        if expected_value > highest_value or (expected_value == highest_value and 
                                             len(my_history.get(pid, [])) < len(my_history.get(best_opponent, []))):
            highest_value = expected_value
            best_opponent = pid
    
    return (next_move, best_opponent)