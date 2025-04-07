def strategy(my_history, opponent_history, rounds):
    return 1 if not opponent_history else (0 if opponent_history.count(0) > 1 or (rounds and len(my_history) == rounds - 1) else opponent_history[-1])
