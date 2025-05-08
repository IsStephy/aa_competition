def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    opponent_moves = opponents_history[opponent_id]

    if len(opponent_moves) < 3:
        if len(opponent_moves) < 2:
            move = 1
        else:
            if opponent_moves[0] == opponent_moves[1]:
                move = opponent_moves[0]
            else:
                move = 1
    else:
        if opponent_moves[-1] == opponent_moves[-2]:
            move = opponent_moves[-1]
        else:
            move = opponent_moves[-3]

    eligible_opponents = [pid for pid, history in my_history.items() if len(history) < 200]

    if not eligible_opponents:
        next_opponent = opponent_id
    else:
        next_opponent = opponent_id if opponent_id in eligible_opponents else eligible_opponents[0]

    return move, next_opponent