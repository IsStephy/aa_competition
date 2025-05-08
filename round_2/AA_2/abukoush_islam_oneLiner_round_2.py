def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    return ((1 if len(list(my_history.keys())) > 60 else 0), len(list(my_history.keys()))%60)
