def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]],
                     opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    if not hasattr(strategy_round_2, "defection_count"):
        strategy_round_2.defection_count = {}
        strategy_round_2.defection_mode = {}
        strategy_round_2.defection_streak = {}

    if opponent_id not in strategy_round_2.defection_count:
        strategy_round_2.defection_count[opponent_id] = 0
        strategy_round_2.defection_mode[opponent_id] = False
        strategy_round_2.defection_streak[opponent_id] = 0

    opp_moves = opponents_history.get(opponent_id, [])

    if len(opp_moves) > 0 and opp_moves[-1] == 0:
        strategy_round_2.defection_count[opponent_id] += 1

    if not strategy_round_2.defection_mode[opponent_id] and strategy_round_2.defection_count[opponent_id] >= 2:
        strategy_round_2.defection_mode[opponent_id] = True
        strategy_round_2.defection_streak[opponent_id] = 0

    if strategy_round_2.defection_mode[opponent_id]:
        strategy_round_2.defection_streak[opponent_id] += 1
        if strategy_round_2.defection_streak[opponent_id] <= 10:
            move = 0
        else:
            if len(opp_moves) > 0 and opp_moves[-1] == 1:
                strategy_round_2.defection_mode[opponent_id] = False
                strategy_round_2.defection_streak[opponent_id] = 0
                strategy_round_2.defection_count[opponent_id] = 0
                move = 1
            else:
                move = 0
    else:
        move = 1

    all_opponents = list(my_history.keys())
    if not all_opponents:
        all_opponents = [0]

    eligible = [opp for opp in all_opponents if len(my_history.get(opp, [])) < 200]

    if not eligible:
        new_opp = max(my_history.keys()) + 1 if my_history else 0
        eligible = [new_opp]

    best_coop_rate = -1
    next_opp = eligible[0]

    for opp in eligible:
        opp_hist = opponents_history.get(opp, [])
        if not opp_hist:
            coop_rate = 1.0
        else:
            coop_rate = opp_hist.count(1) / len(opp_hist)

        if coop_rate > best_coop_rate:
            best_coop_rate = coop_rate
            next_opp = opp

    return move, next_opp
