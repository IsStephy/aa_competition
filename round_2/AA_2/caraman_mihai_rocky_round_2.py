def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    my_hist = my_history.get(opponent_id, [])
    opp_hist = opponents_history.get(opponent_id, [])
    total_moves = len(opp_hist)

    coop_rate = sum(opp_hist) / total_moves if total_moves > 0 else 1.0
    recent = opp_hist[-5:] if total_moves >= 5 else opp_hist
    recent_rate = (sum(recent) / len(recent)) if recent else 1.0
    move = 0
    if total_moves == 0:
        move = 1

    elif total_moves >= 10 and sum(opp_hist) == 0:
        move = 0

    elif total_moves >= 10 and sum(opp_hist) == total_moves:
        move = 1

    elif total_moves >= 3:
        mimic = True
        for i in range(1, total_moves):
            if i < len(my_hist) and opp_hist[i] != my_hist[i - 1]:
                mimic = False
                break
        move = 1 if mimic else None
        if move is None:
            move = None

    if 'move' not in locals() or move is None:
        if total_moves >= 4 and opp_hist[-4:] == [1, 0, 1, 0]:
            move = 0

    if move is None:
        if total_moves >= 2 and opp_hist[-2:] == [0, 0]:
            move = 0

    if move is None:
        if recent and recent_rate < coop_rate - 0.3:
            move = 0

    if move is None:
        if coop_rate > 0.8:
            move = 1

    if move is None:
        if coop_rate < 0.2:
            move = 0

    if move is None:
        if 0.4 < coop_rate < 0.6:
            move = 0 if my_hist and my_hist[-1] == 1 else 1

    if move is None:
        move = opp_hist[-1]

    MAX_ROUNDS = 200

    candidates = []
    for pid, hist in opponents_history.items():
        if len(my_history.get(pid, [])) >= MAX_ROUNDS:
            continue
        if 0 in hist:
            continue
        candidates.append((pid, len(hist)))

    if not candidates:
        best_rate = -1.0
        best_id = opponent_id
        for pid, hist in opponents_history.items():
            if len(my_history.get(pid, [])) >= MAX_ROUNDS:
                continue
            rate = sum(hist) / len(hist) if hist else 1.0
            if rate > best_rate:
                best_rate = rate
                best_id = pid
        next_opponent = best_id
    else:
        candidates.sort(key=lambda x: x[1])
        next_opponent = candidates[0][0]

    return move, next_opponent
