def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    my_moves = my_history.get(opponent_id, [])
    opp_moves = opponents_history.get(opponent_id, [])

    if not opp_moves:
        for candidate_id, history in my_history.items():
            if len(history) < 200:
                return 1, candidate_id
        return 1, opponent_id

    total = len(opp_moves)
    coop_ratio = opp_moves.count(1) / total
    defect_ratio = opp_moves.count(0) / total

    if total >= 2 and opp_moves[-2:] == [0, 0]:
        move = 0
    elif total >= 2 and my_moves[-2:] == [0, 0] and opp_moves[-2:] == [1, 1]:
        move = 1
    elif coop_ratio >= 0.7:
        move = 1
    elif defect_ratio > 0.4:
        move = opp_moves[-1]
    else:
        move = 1

    for next_id, history in my_history.items():
        if len(history) < 200:
            return move, next_id

    return move, opponent_id
