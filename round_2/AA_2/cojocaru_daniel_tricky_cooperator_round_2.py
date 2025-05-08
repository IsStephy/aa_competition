def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    current_opp_moves = opponents_history.get(opponent_id, [])

    if not current_opp_moves:
        move = 1
    elif current_opp_moves.count(0) > 3:
        move = 0
    else:
        move = current_opp_moves[-1]

    available_opponents = [id for id, moves in my_history.items() if len(moves) < 200]

    if available_opponents:
        best_opponent = max(
            available_opponents,
            key=lambda id: (opponents_history[id].count(1) / len(opponents_history[id])) if opponents_history[id] else 1
        )
    else:
        best_opponent = opponent_id

    return move, best_opponent
