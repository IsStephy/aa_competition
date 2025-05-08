def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    round_num = len(my_history.get(opponent_id, []))
    
    if round_num == 0:
        move = 1
    elif round_num == 199:
        move = 0
    elif round_num >= 16 and ((round_num - 16) % 24 == 0 or (round_num - 17) % 24 == 0):
        move = 1
    else:
        opponent_last_move = opponents_history[opponent_id][-1] if opponents_history[opponent_id] else 1
        move = opponent_last_move

    coop_rates = {}
    for opp_id in opponents_history.keys():
        if opp_id == opponent_id or len(my_history.get(opp_id, [])) >= 200:
            continue
        opp_moves = opponents_history.get(opp_id, [])
        if not opp_moves:
            coop_rates[opp_id] = 1.0
        else:
            coop_rate = sum(opp_moves) / len(opp_moves)
            coop_rates[opp_id] = coop_rate

    if coop_rates:
        next_opponent = max(coop_rates, key=coop_rates.get)
    else:
        next_opponent = opponent_id if len(my_history.get(opponent_id, [])) < 199 else list(opponents_history.keys())[0]

    return (move, next_opponent)