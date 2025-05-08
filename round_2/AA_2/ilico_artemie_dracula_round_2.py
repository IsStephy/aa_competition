def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> \
tuple[int, int]:
    if not my_history[opponent_id]:
        move = 1
    else:
        current_round = len(my_history[opponent_id])
        if current_round <= 50:
            move = opponents_history[opponent_id][-1]
        else:
            first_50_cooperation_rate = sum(opponents_history[opponent_id][:50]) / 50
            if first_50_cooperation_rate > 0.7:
                forgiveness_frequency = 5
            elif first_50_cooperation_rate > 0.5:
                forgiveness_frequency = 7
            else:
                forgiveness_frequency = 10

            rounds_after_50 = current_round - 50
            if rounds_after_50 % forgiveness_frequency == 0:
                move = 1
            else:
                move = opponents_history[opponent_id][-1]
    cooperation_rates = {}
    for player_id in opponents_history:
        if len(opponents_history[player_id]) > 0:
            cooperation_rates[player_id] = sum(opponents_history[player_id]) / len(opponents_history[player_id])
        else:
            cooperation_rates[player_id] = 0.5

    expected_values = {}
    for player_id, rate in cooperation_rates.items():
        if len(my_history[player_id]) >= 200:
            continue

        expected_values[player_id] = rate * 3 + (1 - rate) * 1

        if rate > 0.8 and len(my_history[player_id]) > 10:
            expected_values[player_id] = rate * 5

        if len(my_history[player_id]) < 5:
            expected_values[player_id] += 0.5

    if not expected_values:
        return move, opponent_id

    next_opponent = max(expected_values, key=expected_values.get)

    return move, next_opponent
