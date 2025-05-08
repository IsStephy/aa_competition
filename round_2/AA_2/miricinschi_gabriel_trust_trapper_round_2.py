def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    round_number = len(my_history.get(opponent_id, []))
    opponent_history = opponents_history.get(opponent_id, [])
    my_own_history = my_history.get(opponent_id, [])

    if round_number < 3:
        move = 1
    elif round_number >= 190:
        move = 0
    else:
        try:
            last_defect = len(opponent_history) - 1 - opponent_history[::-1].index(0)
        except ValueError:
            last_defect = -1

        if 0 <= last_defect < round_number - 2 and round_number - last_defect == 3:
            move = 0
        elif 0 <= last_defect < round_number - 3 and round_number - last_defect == 4:
            move = 0
        else:
            coop_streak = 0
            for m in reversed(opponent_history):
                if m == 1:
                    coop_streak += 1
                else:
                    break
            if coop_streak >= 4:
                move = 0
            else:
                coop_ratio = opponent_history.count(1) / round_number if round_number > 0 else 1
                if my_own_history[-2:] == [1, 1] and coop_ratio > 0.7:
                    move = 0
                else:
                    move = 1

    candidates = [opp for opp, hist in my_history.items() if len(hist) < 200 and opp != opponent_id]
    if candidates:
        best_opponent = candidates[0]
        best_rate = -1
        for cand in candidates:
            hist = opponents_history.get(cand, [])
            rate = sum(hist) / len(hist) if hist else 1
            if rate > best_rate:
                best_rate = rate
                best_opponent = cand
        next_opponent = best_opponent
    else:
        next_opponent = opponent_id

    return (move, next_opponent)
