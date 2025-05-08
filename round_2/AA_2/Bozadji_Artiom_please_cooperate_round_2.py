def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    my_moves = my_history[opponent_id]
    opponent_moves = opponents_history[opponent_id]
    move = 0 
    
    if not opponent_moves:
        move = 0
    else:
        cooperation, rejection = 0, 0
        for i in opponent_moves:
            if i == 0:
                rejection += 1
            else:
                cooperation += 1
        if len(my_moves) >= 2 and my_moves[-2:] == [1, 0]:
            move = 0
        elif 95 <= len(opponent_moves) < 100:
            move = 0
        elif cooperation == 0 and rejection < 25:
            move = 1
        elif rejection - cooperation == 21:
            move = 1
        elif len(opponent_moves) >= 10 and all(move == 0 for move in opponent_moves[-10:]):
            move = 1
        else:
            move = 0
    
    best_opponent = opponent_id 
    best_score = -1
    
    for opp_id in my_history:
        if len(my_history[opp_id]) >= 200:
            continue
            
        opp_moves = opponents_history[opp_id]
        score = 0
        
        if not opp_moves:
            score = 50
        else:
            coop_rate = sum(opp_moves) / len(opp_moves)
            
            if coop_rate > 0.7:
                score = 90

            elif len(opp_moves) > 0:
                defect_diff = sum(1 for m in opp_moves if m == 0) - sum(1 for m in opp_moves if m == 1)
                if 19 <= defect_diff <= 23:  
                    score = 80
                else:
                    score = int(coop_rate * 60)
        

        round_total = sum(len(hist) for hist in my_history.values())
        score = (score + (opp_id * 7 + round_total * 13) % 20) % 100
        
        rounds_played = len(my_history[opp_id])
        if rounds_played < 50:
            score += 10

        if score > best_score:
            best_score = score
            best_opponent = opp_id
    
    return move, best_opponent
