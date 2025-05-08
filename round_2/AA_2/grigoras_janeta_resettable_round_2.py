def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    def cooperation_rate(player_id: int) -> float:
        history = opponents_history.get(player_id, [])
        return sum(history) / len(history) if history else 1.0

    if my_history is None:
        my_history = {}
    if opponents_history is None:
        opponents_history = {}

    my_moves = my_history.get(opponent_id, [])
    opponent_moves = opponents_history.get(opponent_id, [])

    if len(my_moves) == 0:
        strategy_round_2.last_fresh_start = 0
    if len(my_moves) <= 5:
        move = opponent_moves[-1] if len(opponent_moves) != 0 else 1
    elif 200 - len(my_moves) <= 2:
        move = 0
    else:
        recent_opponent_moves = opponent_moves[-5:]
        cooperation = recent_opponent_moves.count(1)
        defection = recent_opponent_moves.count(0)
        youre_bad = defection > cooperation

        you_get_a_fresh_start = (
                (len(recent_opponent_moves) >= 2 and recent_opponent_moves[-1] != 0 and recent_opponent_moves[-2] != 1)
                and len(my_moves) - strategy_round_2.last_fresh_start >= 20
                and (200 - len(my_moves) > 10)
        )

        if you_get_a_fresh_start:
            strategy_round_2.last_fresh_start = len(my_moves)
            move = 1
        elif youre_bad:
            move = 0
        else:
            move = opponent_moves[-1]

    max_rounds = 200
    min_rounds_played = 10
    not_played = [player for player in opponents_history.keys() if len(my_history.get(player, [])) < min_rounds_played]

    if not_played:
        next_opponent = not_played[0]
    else:
        opponents_values = {}
        payoff = {(1, 1): 3, (1, 0): 0, (0, 1): 5, (0, 0): 1}

        for player in opponents_history.keys():
            my_strategy = my_history.get(player, [])
            if len(my_strategy) < max_rounds:
                player_strategy = opponents_history.get(player, [])
                if not my_strategy or not player_strategy:
                    score = 0
                else:
                    score = sum(payoff[(m, o)] for m, o in zip(my_strategy, player_strategy))
                opponents_values[player] = score + 5 * cooperation_rate(player)

        if opponents_values:
            sorted_opponents = sorted(opponents_values.keys(), key=lambda player_id: opponents_values[player_id], reverse=True)
            next_opponent = sorted_opponents[0]
        else:
            next_opponent = opponent_id

    return move, next_opponent
