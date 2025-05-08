def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> \
tuple[int, int]:
    opp_history = opponents_history[opponent_id]
    my_hist = my_history[opponent_id]

    # Using the same logic as in the original strategy
    if not opp_history:
        move = 1
    elif len(opp_history) < 20:
        if len(opp_history) >= 2 and opp_history[-1] == 0 and opp_history[-2] == 0:
            move = 0
        else:
            move = 1
    else:
        def detect_always_cooperate(history):
            return all(m == 1 for m in history)

        def detect_always_defect(history):
            return all(m == 0 for m in history)

        def detect_tit_for_tat(history, my_history):
            if len(history) < 2:
                return False
            return all(history[i] == my_history[i - 1] for i in range(1, len(history)))

        def detect_alternating(history):
            if len(history) < 2:
                return False
            return all(history[i] != history[i + 1] for i in range(len(history) - 1))

        def detect_grim_trigger(opp_history, my_hist):
            for i in range(len(my_hist)):
                if my_hist[i] == 0 and all(m == 0 for m in opp_history[i:]):
                    return True
            return False

        initial_opponent = opp_history[:20]
        initial_my = my_hist[:20]

        if detect_grim_trigger(opp_history, my_hist):
            move = 0
        elif detect_always_cooperate(initial_opponent):
            move = 1
        elif detect_always_defect(initial_opponent):
            move = 0
        elif detect_tit_for_tat(initial_opponent, initial_my):
            move = opp_history[-1]
        elif detect_alternating(initial_opponent):
            move = 1 - opp_history[-1]
        else:
            coop_rate = initial_opponent.count(1) / 20
            if coop_rate <= 0.5:
                move = 0
            else:
                move = opp_history[-1]

    round_counts = {opp: len(hist) for opp, hist in my_history.items()}

    win_rates = {}
    for opp in my_history:
        if my_history[opp]:
            total_score = 0
            for i in range(len(my_history[opp])):
                my_move = my_history[opp][i]
                opp_move = opponents_history[opp][i]

                if my_move == 1 and opp_move == 1:
                    total_score += 3
                elif my_move == 0 and opp_move == 1:
                    total_score += 5
                elif my_move == 1 and opp_move == 0:
                    total_score += 0
                else:
                    total_score += 1

            win_rates[opp] = total_score / len(my_history[opp])
        else:
            win_rates[opp] = 0

    empty_opponents = [opp for opp in my_history if not my_history[opp]]

    one_round_opponents = [opp for opp in my_history if len(my_history[opp]) == 1]
    good_one_round = [opp for opp in one_round_opponents if opponents_history[opp][0] == 1]

    two_round_opponents = [opp for opp in my_history if len(my_history[opp]) == 2]
    good_two_round = [opp for opp in two_round_opponents if opponents_history[opp].count(1) == 2]
    bad_two_round = [opp for opp in two_round_opponents if opp not in good_two_round]

    high_play_opponents = [opp for opp in my_history if 60 <= len(my_history[opp]) < 200]

    under_60_opponents = [opp for opp in my_history if 2 < len(my_history[opp]) < 60]

    mid_play_opponents = [opp for opp in my_history if 60 <= len(my_history[opp]) < 100]

    next_opponent = None

    if empty_opponents:
        next_opponent = empty_opponents[0]

    elif good_one_round:
        next_opponent = good_one_round[0]

    elif good_two_round:
        next_opponent = good_two_round[0]

    elif high_play_opponents:
        sorted_opponents = sorted(high_play_opponents, key=lambda opp: round_counts[opp], reverse=True)
        next_opponent = sorted_opponents[0]

    elif under_60_opponents:
        near_60 = [opp for opp in under_60_opponents if len(my_history[opp]) >= 50]

        if near_60:
            good_win_rate = [opp for opp in near_60 if win_rates[opp] > 0.5]
            if good_win_rate:
                next_opponent = max(good_win_rate, key=lambda opp: win_rates[opp])
            else:
                remaining = [opp for opp in under_60_opponents if opp not in near_60]
                if remaining:
                    next_opponent = min(remaining, key=lambda opp: round_counts[opp])
                else:
                    next_opponent = max(under_60_opponents, key=lambda opp: round_counts[opp])
        else:
            next_opponent = min(under_60_opponents, key=lambda opp: round_counts[opp])

    elif mid_play_opponents:
        good_win_rate = [opp for opp in mid_play_opponents if win_rates[opp] > 0.5]

        if good_win_rate:
            next_opponent = max(good_win_rate, key=lambda opp: win_rates[opp])
        else:
            next_opponent = max(mid_play_opponents, key=lambda opp: round_counts[opp])

    else:
        available = [opp for opp in my_history if round_counts[opp] < 200]

        if not available:
            next_opponent = opponent_id
        else:
            tier_1 = [opp for opp in available if win_rates.get(opp, 0) > 0.4]
            tier_2 = [opp for opp in available if 0.3 < win_rates.get(opp, 0) <= 0.4]
            tier_3 = [opp for opp in available if win_rates.get(opp, 0) <= 0.3]

            if tier_1:
                next_opponent = max(tier_1, key=lambda opp: win_rates[opp])
            elif tier_2:
                next_opponent = max(tier_2, key=lambda opp: win_rates[opp])
            elif tier_3:
                next_opponent = max(tier_3, key=lambda opp: win_rates.get(opp, 0))
            else:
                next_opponent = available[0]

    if next_opponent is not None and round_counts.get(next_opponent, 0) >= 200:
        alternatives = [opp for opp in my_history if round_counts[opp] < 200]
        next_opponent = alternatives[0] if alternatives else opponent_id

    return move, next_opponent