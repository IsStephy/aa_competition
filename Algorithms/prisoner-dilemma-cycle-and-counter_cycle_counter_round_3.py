def strategy_round_3(opponent_id: int, 
                     my_history: dict[int, list[int]], 
                     opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    cycle_length = 6
    current_my_history = my_history.get(opponent_id, [])
    current_opp_history = opponents_history.get(opponent_id, [])
    current_round = len(current_my_history) + 1

    # determine the move for the current opponent using cycle logic
    if current_round % cycle_length == 0:
        move = 0  # planned defection round
    else:
        if len(current_opp_history) >= cycle_length:
            last_cycle = current_opp_history[-cycle_length:]
            if sum(last_cycle) < 3:
                move = 0  # punish low cooperation in the previous cycle
            else:
                move = 1  # cooperate otherwise
        else:
            move = 1  # not enough history yet, so cooperate
    
    # next opponent selection:
    # pick the opponent with the highest cooperation ratio (from our history)
    # who has not reached 200 rounds; default is to stick with the current opponent
    best_ratio = -1.0
    next_opponent = opponent_id
    for opp, moves in my_history.items():
        if 0 < len(moves) < 200:
            ratio = sum(moves) / len(moves)
            if ratio > best_ratio:
                best_ratio = ratio
                next_opponent = opp
    # if there is any opponent we haven't played yet (empty history), select them
    for opp in opponents_history.keys():
        if opp not in my_history or len(my_history[opp]) == 0:
            next_opponent = opp
            break

    return (move, next_opponent)
