def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    current_round = len(my_history.get(opponent_id, []))
    if current_round == 0:
        move = 1
    else:
        cycle_position = current_round % 10
        if cycle_position == 0:
            cycle_position = 10
        recent_window = opponents_history[opponent_id][-cycle_position:]
        betrayals = recent_window.count(0)
        move = 0 if betrayals >= 2 else 1

    available_opponents = [op for op in my_history if len(my_history[op]) < 200]


    if not available_opponents:
        return move, opponent_id


    if opponents_history[opponent_id] and (opponents_history[opponent_id][-1] == 0 or len(my_history[opponent_id]) >= 200):

        available_opponents.sort(key=lambda x: (len(my_history[x]), x))
        next_opponent = available_opponents[0]
        return move, next_opponent


    return move, opponent_id
