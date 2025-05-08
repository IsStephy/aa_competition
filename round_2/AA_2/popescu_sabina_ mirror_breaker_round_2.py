def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    MAX_ROUNDS = 200

    my_moves = my_history.get(opponent_id, [])
    opp_moves = opponents_history.get(opponent_id, [])
    rounds = len(my_moves)

    if rounds == 0:
        move = 1 

    elif rounds == MAX_ROUNDS - 1:
        move = 0 

    elif rounds < 6:
        move = opp_moves[-1] if opp_moves else 1

    elif len(my_moves) >= 2 and my_moves[-1] == opp_moves[-1] and my_moves[-2] == opp_moves[-2]:
        move = 0 if opp_moves[-1] else 1 

    else:
        coop_rate = sum(opp_moves) / rounds if rounds else 1

        if coop_rate > 0.8:
            move = 0

        elif coop_rate < 0.4:
            move = 0 if rounds % 2 == 0 else 1

        else:
            move = 1

   
    available_opponents = [pid for pid, moves in my_history.items() if len(moves) < MAX_ROUNDS]
    if opponent_id not in available_opponents and len(my_moves) < MAX_ROUNDS:
        available_opponents.append(opponent_id)

    if not available_opponents:
        next_opponent = opponent_id
    else:
       
        best_score = -1
        next_opponent = opponent_id 

        for pid in available_opponents:
            opp_hist = opponents_history.get(pid, [])
            if not opp_hist:
                score = 1
            else:
                score = sum(opp_hist) / len(opp_hist)

            if score > best_score:
                best_score = score
                next_opponent = pid

    return move, next_opponent
