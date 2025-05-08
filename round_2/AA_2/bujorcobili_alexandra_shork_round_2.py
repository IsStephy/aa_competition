def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    if not opponents_history[opponent_id]: return 1, opponent_id
    
    current_history = my_history[opponent_id]
    current_opponent_history = opponents_history[opponent_id]
    debt = current_history.count(1) - current_opponent_history.count(1)
    
    next_opponent = opponent_id
    for pid in opponents_history:
        if pid not in my_history: 
            next_opponent = pid
            break
        if pid in my_history and len(my_history[pid]) < 200:
            if pid in opponents_history and opponents_history[pid] and sum(opponents_history[pid])/len(opponents_history[pid]) > 0.6:
                next_opponent = pid
                break
    
    if debt > 0 and debt*1.5 > sum(current_history)-sum(current_opponent_history): return 0, next_opponent
    if len(current_history) >= 198: return 0, next_opponent
    if current_opponent_history[-1] == 1: return 1, next_opponent
    if len(current_history) % 7 == 0: return 1, next_opponent
    
    return 0, next_opponent