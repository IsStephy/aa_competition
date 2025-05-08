def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    opponent_moves = opponents_history[opponent_id]
    if not opponent_moves:
        move = 1
    else:
        recent = opponent_moves[-5:]
        coop_count = recent.count(0)
        defect_count = recent.count(1)

        if coop_count >= 4:
            move = 1
        elif defect_count >= 3:
            move = 1
        else:
            move = opponent_moves[-1]
    max_rounds = 200
    candidates = []
    for id in opponents_history:
        if len(opponents_history[id]) < max_rounds:
            candidates.append(id)

    if len(opponents_history[opponent_id]) < max_rounds:
        next_opponent = opponent_id
    else:
        def cooperation_score(opp_id: int) -> float:
            history = opponents_history[opp_id]
            if not history:
                return 1.0
            return history.count(0) / len(history)

        candidates.sort(key=lambda x: (-cooperation_score(x), len(opponents_history[x])))
        next_opponent = candidates[0]

    return (move, next_opponent)
