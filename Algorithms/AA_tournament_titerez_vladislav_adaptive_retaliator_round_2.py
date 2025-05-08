def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    my_moves = my_history.get(opponent_id, [])
    opponent_moves = opponents_history.get(opponent_id, [])
    
    if not opponent_moves:
        move = 1
    else:
        total_rounds = len(opponent_moves)
        opponent_defects = opponent_moves.count(0)
        my_defects = my_moves.count(0)

        if total_rounds >= 2 and opponent_moves[-1] == 0 and opponent_moves[-2] == 0:
            move = 0
        elif opponent_defects / total_rounds > 0.5:
            move = 0
        elif my_defects >= 10 and my_moves[-2:].count(0) < 2:
            move = 1
        elif total_rounds == 199:
            move = 0
        else:
            move = 1

    available_opponents = [pid for pid in opponents_history if len(my_history.get(pid, [])) < 200]
    
    def cooperation_score(pid):
        opp = opponents_history[pid]
        return opp.count(1) / len(opp) if opp else 1.0

    available_opponents.sort(key=cooperation_score, reverse=True)

    next_opponent = available_opponents[0] if available_opponents else opponent_id

    return move, next_opponent
