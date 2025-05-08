def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], 
                     opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    
    my_moves = my_history.get(opponent_id, [])
    opponent_moves = opponents_history.get(opponent_id, [])
    
    if not opponent_moves:
        current_move = 1
    else:
        opponent_cooperation_rate = sum(opponent_moves) / len(opponent_moves)
        recent_window = min(5, len(opponent_moves))
        recent_opponent_behavior = opponent_moves[-recent_window:]
        recent_cooperation_rate = sum(recent_opponent_behavior) / len(recent_opponent_behavior)
        
        tit_for_tat_likelihood = 0
        for i in range(1, len(my_moves)):
            if opponent_moves[i] == my_moves[i-1]:
                tit_for_tat_likelihood += 1
        if len(my_moves) > 1:
            tit_for_tat_likelihood /= (len(my_moves) - 1)
        
        last_move_defect = opponent_moves[-1] == 0
        
        betrayal_pattern = False
        if len(opponent_moves) >= 3:
            for i in range(len(opponent_moves) - 2):
                if opponent_moves[i:i+3] == [1, 1, 0] and my_moves[i:i+2] == [1, 1]:
                    betrayal_pattern = True
        
        consecutive_defections = 0
        for move in reversed(opponent_moves):
            if move == 0:
                consecutive_defections += 1
            else:
                break
        
        endgame = False
        rounds = None
        if rounds is not None:
            remaining = rounds - len(my_moves)
            if remaining <= 3:
                endgame = True
        
        if endgame:
            current_move = 0
        elif opponent_cooperation_rate > 0.8:
            current_move = 0 if len(my_moves) % 10 == 0 else 1
        elif tit_for_tat_likelihood > 0.8:
            current_move = 1
        elif recent_cooperation_rate > opponent_cooperation_rate and recent_cooperation_rate > 0.6:
            current_move = 1
        elif last_move_defect:
            current_move = 1 if consecutive_defections > 3 else 0
        elif betrayal_pattern:
            current_move = 0
        elif opponent_moves[-1] == 1:
            current_move = 1
        else:
            current_move = 1 if len(my_moves) % 5 == 0 else 0

    opponent_stats = {}
    for opp_id in opponents_history.keys():
        if len(my_history.get(opp_id, [])) >= 200:
            continue
        opp_moves = opponents_history.get(opp_id, [])
        my_moves_opp = my_history.get(opp_id, [])
        if not opp_moves:
            opponent_stats[opp_id] = {'cooperation_rate': 1.0, 'rounds_played': 0}
            continue
        my_score = 0
        for i in range(len(my_moves_opp)):
            if my_moves_opp[i] == 1 and opp_moves[i] == 1:
                my_score += 3
            elif my_moves_opp[i] == 0 and opp_moves[i] == 1:
                my_score += 5
            elif my_moves_opp[i] == 0 and opp_moves[i] == 0:
                my_score += 1
        avg_score = my_score / len(my_moves_opp)
        cooperation_rate = sum(opp_moves) / len(opp_moves)
        opponent_stats[opp_id] = {
            'avg_score': avg_score,
            'cooperation_rate': cooperation_rate,
            'rounds_played': len(my_moves_opp)
        }

    if not opponent_stats:
        next_opponent = opponent_id
    else:
        best_opponent = None
        best_value = -1
        for opp_id, stats in opponent_stats.items():
            if 'avg_score' in stats:
                value = stats['avg_score'] + (stats['cooperation_rate'] * 0.5)
            else:
                value = stats['cooperation_rate'] * 3
            if stats['rounds_played'] == 0:
                value += 0.3
            if value > best_value:
                best_value = value
                best_opponent = opp_id
        next_opponent = best_opponent if best_opponent is not None else opponent_id

    return (current_move, next_opponent)
