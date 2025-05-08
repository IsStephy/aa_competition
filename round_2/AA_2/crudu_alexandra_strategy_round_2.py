def strategy_round_2(
    opponent_id: int,
    my_history: dict[int, list[int]],
    opponents_history: dict[int, list[int]]
) -> tuple[int, int]:



    past_moves = my_history.get(opponent_id, [])
    past_opp = opponents_history.get(opponent_id, [])
    if not past_moves:
        move = 1
    else:
        move = past_opp[-1]


    eligible = [
        pid for pid, hist in my_history.items()
        if len(hist) < 200
    ]

    if not eligible:
        return move, opponent_id


    coop_rate: dict[int, float] = {}
    for pid in eligible:
        hist = opponents_history.get(pid, [])
        coop_rate[pid] = (sum(hist) / len(hist)) if hist else 1.0


    next_opponent = min(
        coop_rate.keys(),
        key=lambda pid: (-coop_rate[pid], pid)
    )

    return move, next_opponent
