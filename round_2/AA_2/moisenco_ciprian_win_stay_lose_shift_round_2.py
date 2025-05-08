def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    if len(my_history[opponent_id]) == 0:
        move = 1
    else:
        my_last_move = my_history[opponent_id][-1]
        opp_last_move = opponents_history[opponent_id][-1]
        if my_last_move == 0 and opp_last_move == 0:
            my_payoff = 1
        elif my_last_move == 0 and opp_last_move == 1:
            my_payoff = 5
        elif my_last_move == 1 and opp_last_move == 0:
            my_payoff = 0
        else:
            my_payoff = 3
        if my_payoff in (3, 5):
            move = my_last_move
        else:
            move = 1 - my_last_move

    recent_defections = opponents_history[opponent_id][-3:].count(0) if len(opponents_history[opponent_id]) >= 3 else 0
    avoid_current = recent_defections >= 2

    best_opponent = None
    best_coop_ratio = -1.0

    for player_id, history in opponents_history.items():
        if len(history) >= 200:
            continue
        if len(history) == 0:
            coop_ratio = 1.0
        else:
            coop_ratio = sum(history) / len(history)
        if coop_ratio > best_coop_ratio or (coop_ratio == best_coop_ratio and (best_opponent is None or player_id < best_opponent)):
            best_coop_ratio = coop_ratio
            best_opponent = player_id

    if best_opponent is None or (not avoid_current and len(opponents_history[opponent_id]) < 200):
        next_opponent = opponent_id
    else:
        next_opponent = best_opponent

    return move, next_opponent
