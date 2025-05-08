def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    def classify_opponent(oid):
        opp_moves = opponents_history.get(oid, [])
        if not opp_moves:
            return 'unknown'
        coop_rate = sum(opp_moves) / len(opp_moves)
        if coop_rate >= 0.8:
            return 'naive'
        elif coop_rate >= 0.5:
            return 'cooperative'
        else:
            return 'hostile'

    def choose_opponent():
        best_score = -1
        chosen = None
        for oid in opponents_history.keys():
            if len(my_history.get(oid, [])) >= 200:
                continue
            category = classify_opponent(oid)
            if category == 'unknown':
                return oid
            elif category == 'naive':
                score = 3
            elif category == 'cooperative':
                score = 2
            else:
                score = 1
            if score > best_score:
                best_score = score
                chosen = oid
        for oid in range(1000):
            if len(my_history.get(oid, [])) < 200:
                return oid
        return opponent_id

    my_moves = my_history.get(opponent_id, [])
    opp_moves = opponents_history.get(opponent_id, [])
    round_num = len(my_moves)

    if round_num < 3:
        move = 1
    elif round_num == 5:
        if all(m == 0 for m in opp_moves[:5]):
            move = 0
        elif all(m == 1 for m in opp_moves[:5]):
            move = 1
        else:
            move = 1
    else:
        if opp_moves and opp_moves[-1] == 0:
            move = 1
        elif round_num % 6 == 0:
            move = 0
        else:
            move = 1

    if classify_opponent(opponent_id) == 'naive' and round_num >= 15:
        move = 0

    next_opponent = choose_opponent()
    return (move, next_opponent)
