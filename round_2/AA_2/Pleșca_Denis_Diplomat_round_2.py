def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    def select_next_opponent(opponents_history):
        cooperation_scores = {opponent: sum([1 for move in history if move == 1]) for opponent, history in opponents_history.items()}
        sorted_opponents = sorted(cooperation_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_opponents[0][0]

    if not opponents_history[opponent_id]:
        return 1, select_next_opponent(opponents_history)

    r = len(my_history[opponent_id])

    if r >= 200:
        return 0, select_next_opponent(opponents_history)

    if len(opponents_history[opponent_id]) >= 3 and opponents_history[opponent_id][-3:] == [0, 0, 0]:
        return 0, select_next_opponent(opponents_history)

    total = len(opponents_history[opponent_id])
    betrayal_rate = opponents_history[opponent_id].count(0) / total
    recent = opponents_history[opponent_id][-5:] if total >= 5 else opponents_history[opponent_id]
    recent_betrayal = recent.count(0) / len(recent)

    pattern_length = 4
    if total >= pattern_length * 2:
        recent_pattern = opponents_history[opponent_id][-pattern_length:]
        for i in range(total - pattern_length * 2):
            window = opponents_history[opponent_id][i:i+pattern_length]
            if window == recent_pattern:
                if my_history[opponent_id][i+pattern_length] == 1 and opponents_history[opponent_id][i+pattern_length] == 0:
                    return 0, select_next_opponent(opponents_history)

    def my_score():
        score = 0
        for my, op in zip(my_history[opponent_id], opponents_history[opponent_id]):
            if my == 1 and op == 1:
                score += 3
            elif my == 0 and op == 1:
                score += 5
            elif my == 1 and op == 0:
                score += 0
            else:
                score += 1
        return score / len(my_history[opponent_id])

    avg_score = my_score()

    if r >= 10 and opponents_history[opponent_id][-10:] == [0] * 10:
        return 0, select_next_opponent(opponents_history)

    if len(my_history[opponent_id]) >= 2 and my_history[opponent_id][-2:] == [0, 0] and opponents_history[opponent_id][-2:] == [0, 0]:
        return 1, select_next_opponent(opponents_history)

    if avg_score < 2.0 or (betrayal_rate > 0.6 and recent_betrayal > 0.4):
        return 0, select_next_opponent(opponents_history)

    if betrayal_rate > 0.4 and recent_betrayal <= 0.2:
        return 1, select_next_opponent(opponents_history)

    if opponents_history[opponent_id][-1] == 0:
        return 0, select_next_opponent(opponents_history)


    if betrayal_rate < 0.4:
        return 1, select_next_opponent(opponents_history)

    return 0, select_next_opponent(opponents_history)

