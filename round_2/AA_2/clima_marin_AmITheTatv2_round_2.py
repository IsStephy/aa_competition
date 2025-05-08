def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    rounds_played = len(my_history[opponent_id])
    opponent_moves = opponents_history[opponent_id]

    is_blacklisted = 0 in opponent_moves

    if rounds_played + 1 == 200:
        move = 0  
    elif rounds_played == 0:
        move = 1
    else:
        move = 0 if is_blacklisted else opponent_moves[-1]  

    next_opponent = opponent_id 

    if is_blacklisted:
        best_choice = None
        best_score = -1

        for player, history in opponents_history.items():
            if 0 in history or len(history) >= 200:
                continue 

            if not history:
                score = 2.0 
            else:
                coop_rate = history.count(1) / len(history)
                score = coop_rate

            if score > best_score:
                best_score = score
                best_choice = player

        if best_choice is not None:
            next_opponent = best_choice

    return move, next_opponent
