def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> \
tuple[int, int]:

    MAX_ROUNDS = 200
    TARGET_ROUNDS = 80
    MIN_ROUNDS = 20
    EXPLORE_ROUNDS = 5
    HIGH_COOP_THRESHOLD = 0.65
    MID_COOP_THRESHOLD = 0.5
    LOW_COOP_THRESHOLD = 0.35

    def get_coop_rate(history):
        if not history:
            return 0.5
        return sum(history) / len(history)

    curr_opp_history = opponents_history.get(opponent_id, [])
    my_moves_against_curr = my_history.get(opponent_id, [])

    available_opponents = [
        opid for opid in opponents_history.keys()
        if len(my_history.get(opid, [])) < MAX_ROUNDS
    ]

    coop_rates = {}
    for opid in opponents_history:
        history = opponents_history.get(opid, [])
        if history:
            coop_rates[opid] = get_coop_rate(history)

    cooperative_opponents = [opid for opid, rate in coop_rates.items()
                             if rate >= HIGH_COOP_THRESHOLD and opid in available_opponents]

    mid_cooperative_opponents = [opid for opid, rate in coop_rates.items()
                                 if MID_COOP_THRESHOLD <= rate < HIGH_COOP_THRESHOLD and opid in available_opponents]

    defective_opponents = [opid for opid, rate in coop_rates.items()
                           if rate <= LOW_COOP_THRESHOLD and opid in available_opponents]

    neutral_opponents = [opid for opid in available_opponents
                         if opid not in cooperative_opponents
                         and opid not in defective_opponents
                         and opid not in mid_cooperative_opponents]

    unexplored = [opid for opid in available_opponents if len(opponents_history.get(opid, [])) < EXPLORE_ROUNDS]

    if not curr_opp_history or len(my_moves_against_curr) < 2:
        move = 1
    else:
        opp_coop_rate = get_coop_rate(curr_opp_history)

        if opp_coop_rate >= HIGH_COOP_THRESHOLD:
            move = 0 if len(my_moves_against_curr) % 4 == 3 else 1

        elif opp_coop_rate >= MID_COOP_THRESHOLD:
            move = 0 if len(my_moves_against_curr) % 5 == 4 else 1

        elif opp_coop_rate <= LOW_COOP_THRESHOLD:
            move = 1 if len(my_moves_against_curr) % 8 == 0 else 0

        else:
            if curr_opp_history[-1] == 0:
                move = 1 if len(my_moves_against_curr) % 3 == 0 else 0
            else:
                move = 1

    continue_with_current = False

    if len(my_moves_against_curr) < MIN_ROUNDS:
        continue_with_current = True
    elif opponent_id in cooperative_opponents and len(my_moves_against_curr) < TARGET_ROUNDS:
        continue_with_current = True
    elif opponent_id in mid_cooperative_opponents and len(my_moves_against_curr) < TARGET_ROUNDS * 0.75:
        continue_with_current = True
    elif len(my_moves_against_curr) < MIN_ROUNDS * 1.2:
        continue_with_current = True


    if unexplored:
        next_opponent = unexplored[0]
        return move, next_opponent

    if continue_with_current and opponent_id in available_opponents:
        return move, opponent_id


    cooperative_under_target = [opid for opid in cooperative_opponents
                                if len(my_history.get(opid, [])) < TARGET_ROUNDS]
    if cooperative_under_target:
        sorted_coop = sorted([(opid, coop_rates.get(opid, 0), len(my_history.get(opid, [])))
                              for opid in cooperative_under_target],
                             key=lambda x: (x[1], -x[2]), reverse=True)
        return move, sorted_coop[0][0]

    mid_coop_under_target = [opid for opid in mid_cooperative_opponents
                             if len(my_history.get(opid, [])) < int(TARGET_ROUNDS * 0.75)]
    if mid_coop_under_target:
        sorted_mid = sorted([(opid, coop_rates.get(opid, 0)) for opid in mid_coop_under_target],
                            key=lambda x: x[1], reverse=True)
        return move, sorted_mid[0][0]

    under_minimum = [opid for opid in available_opponents if len(my_history.get(opid, [])) < MIN_ROUNDS]
    if under_minimum:
        non_defective = [opid for opid in under_minimum if opid not in defective_opponents]
        if non_defective:
            return move, non_defective[0]
        return move, under_minimum[0]

    if neutral_opponents:
        sorted_neutrals = sorted([(opid, coop_rates.get(opid, 0)) for opid in neutral_opponents],
                                 key=lambda x: x[1], reverse=True)
        return move, sorted_neutrals[0][0]

    if cooperative_opponents:
        sorted_by_rounds = sorted([(opid, len(my_history.get(opid, []))) for opid in cooperative_opponents],
                                  key=lambda x: x[1])
        return move, sorted_by_rounds[0][0]

    if available_opponents:
        sorted_by_rounds = sorted([(opid, len(my_history.get(opid, []))) for opid in available_opponents],
                                  key=lambda x: x[1])
        return move, sorted_by_rounds[0][0]

    return move, opponent_id