def strategy_round_2(
    opponent_id: int,
    my_history: dict[int, list[int]],
    opponents_history: dict[int, list[int]],
) -> tuple[int, int]:
    cycle_length = 6
    current_my = my_history.get(opponent_id, [])
    current_opp = opponents_history.get(opponent_id, [])
    current_round = len(current_my) + 1

    if current_round % cycle_length == 0:
        move = 0
    else:
        if len(current_opp) >= cycle_length and sum(current_opp[-cycle_length:]) < 3:
            move = 0
        else:
            move = 1

    next_opponent = opponent_id
    unplayed = [
        opp
        for opp in opponents_history
        if len(my_history.get(opp, [])) == 0
    ]
    
    if unplayed:
        next_opponent = unplayed[0]
    else:
        best_ratio = -1.0
        for opp, moves in my_history.items():
            if 0 < len(moves) < 200:
                ratio = sum(moves) / len(moves)
                if ratio > best_ratio:
                    best_ratio = ratio
                    next_opponent = opp

    return move, next_opponent
