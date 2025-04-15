def strategy_round_3(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    opponent_moves = opponents_history.get(opponent_id, [])
    my_moves = my_history.get(opponent_id, [])

    if 0 in opponent_moves:
        i = len(my_moves)
        move = (sum(my_moves) + sum(opponent_moves) + i + opponent_id) % 2
    else:
        move = 1

    available = [oid for oid, moves in my_history.items() if len(moves) < 200]
    if not available:
        next_opponent = opponent_id
    else:
        best = max(available, key=lambda oid: opponents_history[oid].count(1) if opponents_history[oid] else 0)
        next_opponent = best

    return move, next_opponent