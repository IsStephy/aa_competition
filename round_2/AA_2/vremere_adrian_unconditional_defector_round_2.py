def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]],opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    if len(my_history[opponent_id]) == 0:
        return 0, opponent_id

    if opponents_history[opponent_id][len(my_history[opponent_id])-1] == 1 and len(my_history[opponent_id]) < 200:
        return 0, opponent_id

    for i in my_history.keys():
        if len(my_history[i]) == 0:
            return 0, i

    percentage_threshold = 20
    games_threshold = 5

    highest_percentage_id = opponent_id
    highest_percentage = -1

    for i in my_history.keys():
        if len(my_history[i]) >= 200:
            continue

        if len(opponents_history[i]) > 0:
            ones_count = sum(1 for move in opponents_history[i] if move == 1)
            percentage = ones_count / len(opponents_history[i]) * 100

            if percentage > highest_percentage:
                highest_percentage = percentage
                highest_percentage_id = i

    if highest_percentage > percentage_threshold:
        return 0, highest_percentage_id

    min_games_id = opponent_id
    min_games = float('inf')

    for i in my_history.keys():
        if len(my_history[i]) < min_games and len(my_history[i]) < 200:
            min_games = len(my_history[i])
            min_games_id = i

    if min_games < games_threshold:
        return 0, min_games_id

    return 0, highest_percentage_id
