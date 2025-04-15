def strategy(my_history, opponent_history, rounds):
    if not my_history:
        return 1
    return opponent_history[-1]
