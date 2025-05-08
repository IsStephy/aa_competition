def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]],
                    opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    best_score = -1
    best_opponent = opponent_id
    payoff = {(1, 1): 3, (1, 0): 0, (0, 1): 5, (0, 0): 1}

    defect_values = {1, 6, 7, 17, 22, 23, 26, 29, 30, 31,
                     33, 38, 39, 45, 49, 54, 55, 58, 61}

    n = len(my_history[opponent_id])
    empty = False

    if n == 0:
        return 1, best_opponent

    if n == 1:
        return opponents_history[opponent_id][0], best_opponent

    if n == 2:
        if my_history[opponent_id][0] > opponents_history[opponent_id][0] and my_history[opponent_id][1] < opponents_history[opponent_id][1]:
            result = 0
        else:
            result = opponents_history[opponent_id][1]

        for opp in opponents_history.keys():
            if len(opponents_history[opp]) == 0:
                best_opponent = opp
                empty = True
                break
        if not empty:
            for opp_id, opp_hist in opponents_history.items():
                if len(my_history[opp_id]) == 0 or len(opponents_history[opp_id]) == 0:
                    continue
                score = sum(payoff[(m, o)] for m, o in zip(my_history[opp_id], opponents_history[opp_id])) / len(my_history[opp_id])

                coop_rate = opponents_history[opp_id].count(1) / len(opponents_history[opp_id])
                score += 10 * coop_rate

                if score > best_score:
                    best_score = score
                    best_opponent = opp_id
        return result, best_opponent

    weights = [1, 4, 16]
    A = 0
    for i in range(3):
        points = 0
        if my_history[opponent_id][n - 3 + i] == 0:
            points += 1
        if opponents_history[opponent_id][n - 3 + i] == 0:
            points += 2
        A += weights[i] * points

    for opp_id, opp_hist in opponents_history.items():
        if len(my_history[opp_id]) == 0 or len(opponents_history[opp_id]) == 0:
            continue
        score = sum(payoff[(m, o)] for m, o in zip(my_history[opp_id], opponents_history[opp_id])) / len(my_history[opp_id])
        coop_rate = opponents_history[opp_id].count(1) / len(opponents_history[opp_id])
        score += 10 * coop_rate
        if score > best_score and len(my_history[opp_id]) < 200:
            best_score = score
            best_opponent = opp_id

    if A in defect_values:
        return 0, best_opponent
    else:
        return 1, best_opponent