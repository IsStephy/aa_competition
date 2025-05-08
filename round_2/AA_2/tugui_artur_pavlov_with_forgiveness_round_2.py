def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:

    move = 1

    if my_history[opponent_id] and opponents_history[opponent_id]:
        my_last = my_history[opponent_id][-1]
        opp_last = opponents_history[opponent_id][-1]

        my_last_moves = my_history[opponent_id][-30:]
        opp_last_moves = opponents_history[opponent_id][-30:]

        if my_last == opp_last:
            move = my_last
        elif my_last == 1 and opp_last == 0:
            history_hash = hash(str(my_last_moves) + str(opp_last_moves))
            if history_hash % 5 == 0:
                move = 1
            else:
                move = 0
        else:
            move = 1

    total_rounds_played = sum(len(history) for history in my_history.values())
    available_opponents = [opid for opid in my_history.keys() if len(my_history[opid]) < 200]

    if not available_opponents:
        return move, opponent_id

    if total_rounds_played < 375:
        for opid in available_opponents:
            if 0 < len(my_history[opid]) < 15:
                return move, opid

        unexplored = [opid for opid in available_opponents if len(my_history[opid]) == 0]

        if unexplored:
            index = abs(hash(str(my_history) + str(opponents_history))) % len(unexplored)
            return move, unexplored[index]
        else:
            index = abs(hash(str(my_history) + str(opponents_history))) % len(available_opponents)
            return move, available_opponents[index]

    opponent_scores = {}
    for opid in available_opponents:
        if not my_history[opid] or not opponents_history[opid]:
            continue

        my_moves = my_history[opid]
        opp_moves = opponents_history[opid]
        score = 0

        for i in range(len(my_moves)):
            my_move = my_moves[i]
            opp_move = opp_moves[i]

            if my_move == 1 and opp_move == 1:
                score += 3
            elif my_move == 0 and opp_move == 1:
                score += 5
            elif my_move == 1 and opp_move == 0:
                score += 0
            else:
                score += 1

        opponent_scores[opid] = score / len(my_moves)

    best_opponent = opponent_id
    best_score = -1

    for opid, score in opponent_scores.items():
        if score > best_score:
            best_score = score
            best_opponent = opid

    if best_score == -1 and available_opponents:
        best_opponent = min(available_opponents)

    return move, best_opponent