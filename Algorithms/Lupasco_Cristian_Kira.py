def strategy(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    def calculate_cooperation_rate(history: list[int]) -> float:
        if not history:
            return 0.5
        return sum(history) / len(history)

    def detect_alternating_pattern(history: list[int]) -> bool:
        if len(history) < 3:
            return False
        return history[-3:] == [1, 0, 1] or history[-3:] == [0, 1, 0]

    def select_next_opponent(current_opponent: int, my_history: dict[int, list[int]]) -> int:
        max_rounds = 200
        valid_opponents = [opponent for opponent, history in my_history.items() if len(history) < max_rounds]
        valid_opponents = [opponent for opponent in valid_opponents if opponent != current_opponent]
        if not valid_opponents:
            return current_opponent
        return min(valid_opponents, key=lambda x: len(my_history[x]))

    my_moves = my_history.get(opponent_id, [])
    opponent_moves = opponents_history.get(opponent_id, [])

    if not my_moves:
        return (1, select_next_opponent(opponent_id, my_history))

    if len(my_moves) >= 199:
        return (0, select_next_opponent(opponent_id, my_history))

    opponent_cooperation_rate = calculate_cooperation_rate(opponent_moves)
    if opponent_cooperation_rate > 0.7:
        return (0, select_next_opponent(opponent_id, my_history))

    if opponent_cooperation_rate < 0.3:
        return (0, select_next_opponent(opponent_id, my_history))

    if detect_alternating_pattern(opponent_moves):
        return (0, select_next_opponent(opponent_id, my_history))

    if len(my_moves) % 10 == 0:
        return (1, select_next_opponent(opponent_id, my_history))

    move = opponent_moves[-1] if opponent_moves else 1
    return (move, select_next_opponent(opponent_id, my_history))