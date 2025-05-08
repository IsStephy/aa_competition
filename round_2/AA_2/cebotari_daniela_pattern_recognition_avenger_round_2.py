def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    if not my_history.get(opponent_id, []):
        return 0, opponent_id

    my_moves = my_history[opponent_id]
    opp_moves = opponents_history[opponent_id]
    
    # check if opponent defects too much
    if len(opp_moves) >= 5:
        defection_rate = sum(1 for move in opp_moves[-5:] if move == 0) / 5
        if defection_rate > 0.7:
            current_move = 0
        else:
            # calculate trust using last 10 moves
            recent_moves = opp_moves[-10:] if len(opp_moves) > 10 else opp_moves
            trust_score = 0.5
            for i, move in enumerate(recent_moves):
                weight = 0.7 * (i + 1) / len(recent_moves)
                trust_score += weight * (0.1 if move == 1 else -0.2)
            trust_score = max(0.0, min(1.0, trust_score))
            
            # look for patterns
            if len(opp_moves) >= 4:
                latest_pattern = opp_moves[-3:]
                for i in range(len(opp_moves) - 6):
                    if opp_moves[i:i+3] == latest_pattern:
                        current_move = 0
                        break
                else:
                    # use trust to decide
                    if my_moves[-1] == 1:
                        current_move = 1 if trust_score > 0.4 else 0
                    else:
                        current_move = 1 if trust_score > 0.3 else 0
            else:
                current_move = 1 if trust_score > 0.4 else 0
    else:
        current_move = 0

    # pick next opponent
    available_opponents = []
    opponent_scores = {}
    
    for opp_id in opponents_history.keys():
        rounds_played = len(my_history.get(opp_id, []))
        if rounds_played < 200:
            available_opponents.append(opp_id)
            # quick trust check using last 5 moves
            if opp_id in opponents_history and opponents_history[opp_id]:
                recent_moves = opponents_history[opp_id][-5:] if len(opponents_history[opp_id]) > 5 else opponents_history[opp_id]
                trust = 0.5 + sum(0.1 if move == 1 else -0.2 for move in recent_moves) / len(recent_moves)
                trust = max(0.0, min(1.0, trust))
                coop_rate = sum(1 for move in recent_moves if move == 1) / len(recent_moves)
            else:
                trust = 0.5
                coop_rate = 0.5
            
            score = (trust * 0.4 + coop_rate * 0.4 + (1 - rounds_played/200) * 0.2)
            opponent_scores[opp_id] = score

    if not available_opponents:
        return current_move, opponent_id

    next_opponent = max(opponent_scores.items(), key=lambda x: x[1])[0]
    return current_move, next_opponent 