def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    opponent_history = opponents_history.get(opponent_id, [])
    my_moves = my_history.get(opponent_id, [])
    
    if not opponent_history:
        move = 0
    else:
        opp_coop = sum(opponent_history)

        if opp_coop > 15:
            move = 0
        elif len(opponent_history) >= 15 and sum(opponent_history[-15:]) == 0:
            move = 0
        else:
            move = len(my_moves) % 2

    possible_opponents = [pid for pid, history in my_history.items() if len(history) < 200]
    
    if not possible_opponents:
        next_opponent = opponent_id
    else:
        next_opponent = possible_opponents[0]

    return move, next_opponent
