def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    def is_toxic(history):
        return history[:5].count(0) >= 3

    def is_fibonacci(n):
        a, b = 0, 1
        while b < n:
            a, b = b, a + b
        return b == n

    def looks_random(history):
        if len(history) < 5:
            return False
        return 0 in history[:5] and 1 in history[:5]

    current_round = len(my_history.get(opponent_id, []))
    opp_hist = opponents_history.get(opponent_id, [])
    toxic = is_toxic(opp_hist)

    if current_round == 0:
        move = 1
    elif toxic:
        if current_round >= 51:
            move = 0
        elif is_fibonacci(current_round):
            move = 0
        elif current_round % 6 == 0:
            move = 1
        elif opp_hist[-1] == 0:
            move = 0
        else:
            move = 1
    else:
        if opp_hist[-1] == 0:
            if current_round % 7 == 0:
                move = 1
            else:
                move = 0
        else:
            move = 1

    # selection criteria
    best_score = -1
    next_opponent = opponent_id  # default
    for pid, history in opponents_history.items():
        if len(my_history.get(pid, [])) >= 200:
            continue
        score = 0
        if is_toxic(history):
            score += 3
        if looks_random(history):
            score += 2
        if len(my_history.get(pid, [])) == 0:
            score += 1  # curiosity bonus point

        if score > best_score:
            best_score = score
            next_opponent = pid

    return move, next_opponent
