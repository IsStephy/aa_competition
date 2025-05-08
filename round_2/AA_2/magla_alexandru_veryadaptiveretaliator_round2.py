def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> \
tuple[int, int]:
    # Current opponent's history
    my_hist = my_history.get(opponent_id, [])
    opp_hist = opponents_history.get(opponent_id, [])

    if len(my_hist) == 0:
        move = 1
    else:
        cooperation_count = opp_hist.count(1)
        defection_count = opp_hist.count(0)

        if len(my_hist) < 5:
            move = 1 if cooperation_count >= defection_count else 0
        elif defection_count > cooperation_count:
            move = 0
        elif cooperation_count > defection_count:
            move = 1
        else:
            move = 1 if my_hist[-1] == 0 else 0

    available_opponents = [pid for pid, history in my_history.items() if len(history) < 200]

    best_opponent = None
    best_score = -1

    for pid in available_opponents:
        opponent_moves = opponents_history.get(pid, [])
        if not opponent_moves:
            return move, pid

        coop = opponent_moves.count(1)
        defect = opponent_moves.count(0)
        total = len(opponent_moves)

        if total == 0:
            coop_rate = 1.0
        else:
            coop_rate = coop / total

        if coop_rate > best_score:
            best_score = coop_rate
            best_opponent = pid

    if best_opponent is None:
        next_opponent = opponent_id
    else:
        next_opponent = best_opponent

    return move, next_opponent
