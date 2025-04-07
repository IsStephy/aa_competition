def strategy_round_3(opponent_id, my_history, opponents_history):
    interaction_count = len(my_history.get(opponent_id, []))
    seed = opponent_id * 12345 + interaction_count
    move = (seed * 5144013 + 22310311) % 2

    all_opponents = list(my_history.keys()) + [max(my_history.keys()) + 1 if my_history else 0]
    eligible = [opp for opp in all_opponents if len(my_history.get(opp, [])) < 200]
    
    if not eligible:
        new_opp = max(my_history.keys()) + 1 if my_history else 0
        eligible = [new_opp]
    
    selector = sum(len(v) for v in my_history.values()) % len(eligible)
    next_opp = eligible[selector]

    return (move, next_opp)