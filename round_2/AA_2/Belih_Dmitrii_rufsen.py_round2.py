def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    my_moves = my_history.get(opponent_id, [])
    opponent_moves = opponents_history.get(opponent_id, [])
    current_round = len(my_moves)

    # Step 1: Determine valid opponent IDs
    # Find all available opponents who haven't reached 200 rounds
    valid_opponents = [oid for oid in opponents_history if len(my_history.get(oid, [])) < 200]
    next_opponent = opponent_id if opponent_id in valid_opponents else (valid_opponents[0] if valid_opponents else opponent_id)


    # Step 2: Strategy logic
    if current_round < 2:
        return 1, next_opponent

    if opponent_moves.count(0) >= 3:
        return 0, next_opponent

    total_rounds = max(len(v) for v in my_history.values()) if my_history else None
    if total_rounds is not None and current_round > 0.8 * total_rounds:
        return 0, next_opponent

    recent_opponent_moves = opponent_moves[-5:]
    if 0 in recent_opponent_moves:
        return 0, next_opponent
        
    move = opponent_moves[-1] if opponent_moves else 1
    return move, next_opponent
