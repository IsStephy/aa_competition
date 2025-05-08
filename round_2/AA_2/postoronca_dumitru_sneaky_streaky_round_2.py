def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    my_moves = my_history.get(opponent_id, [])
    opp_moves = opponents_history.get(opponent_id, [])
    round_number = len(my_moves)

    if round_number < 3:
        move = 1
    else:
        coop_rate = opp_moves.count(1) / round_number
        fake_random = (sum(my_moves) + sum(opp_moves) + round_number) % 10
        if coop_rate > 0.7:
            move = 0 if fake_random < 7 else 1
        elif coop_rate < 0.4:
            move = 0
        else:
            move = 0 if fake_random < 6 else 1

    def calculate_score(my, opp):
        score = 0
        for m, o in zip(my, opp):
            if m == 1 and o == 1:
                score += 3
            elif m == 0 and o == 0:
                score += 1
            elif m == 0 and o == 1:
                score += 5
            elif m == 1 and o == 0:
                score += 0
        return score / len(my) if my else 2.5

    best_opponent = None
    best_score = -1

    all_known_opponents = set(my_history.keys()) | set(
        opponents_history.keys())

    for opp_id in range(1, 100):
        my = my_history.get(opp_id, [])
        if len(my) >= 200:
            continue
        opp = opponents_history.get(opp_id, [])
        avg_score = calculate_score(my, opp)
        if avg_score > best_score:
            best_score = avg_score
            best_opponent = opp_id

    if best_opponent is None:
        best_opponent = opponent_id

    return (move, best_opponent)
