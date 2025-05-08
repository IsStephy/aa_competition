def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]],
                     opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    current_opp_history = opponents_history.get(opponent_id, [])
    my_moves_with_current = my_history.get(opponent_id, [])

    if not current_opp_history:
        move = 1
    else:
        cooperation_rate = sum(current_opp_history) / len(current_opp_history)

        recent_window = min(5, len(current_opp_history))
        recent_cooperation = sum(current_opp_history[-recent_window:]) / recent_window if recent_window > 0 else 0

        end_game = len(my_moves_with_current) >= 195

        if cooperation_rate > 0.8:
            if len(my_moves_with_current) % 3 == 0:
                move = 0
            else:
                move = 1
        elif 0.5 <= cooperation_rate <= 0.8:
            if current_opp_history[-1] == 1:
                if recent_cooperation > 0.6:
                    move = 0
                else:
                    move = 1
            elif current_opp_history[-1] == 0:
                if cooperation_rate > 0.65 and len(my_moves_with_current) % 2 == 0:
                    move = 1
                else:
                    move = 0
            else:
                move = 0
        elif cooperation_rate < 0.5:
            if recent_cooperation > 0.6 and current_opp_history[-1] == 1:
                move = 1
            else:
                move = 0
        elif len(current_opp_history) >= 4:
            if (current_opp_history[-2] == 1 and current_opp_history[-1] == 0 and
                    current_opp_history[-4] == 1 and current_opp_history[-3] == 0):
                move = 0
            elif len(my_moves_with_current) >= 3:
                matches = 0
                for i in range(len(my_moves_with_current) - 3, len(my_moves_with_current)):
                    if current_opp_history[i] == my_moves_with_current[i - 1]:
                        matches += 1
                if matches >= 3:
                    move = 1
                else:
                    move = 0
            else:
                move = 0
        elif end_game:
            move = 0
        elif len(my_moves_with_current) % 5 < 2:
            move = 1
        else:
            move = 0

    max_rounds = 200
    best_score = -1
    best_opponent = None

    for opp_id in opponents_history.keys():
        if len(my_history.get(opp_id, [])) >= max_rounds:
            continue

        opp_moves = opponents_history.get(opp_id, [])
        my_moves = my_history.get(opp_id, [])

        if not opp_moves:
            return move, opp_id

        coop_rate = sum(opp_moves) / len(opp_moves) if opp_moves else 0

        total_rounds = len(my_moves)
        if total_rounds > 0:
            points = 0
            for i in range(total_rounds):
                if my_moves[i] == 1 and opp_moves[i] == 1:
                    points += 3
                elif my_moves[i] == 0 and opp_moves[i] == 1:
                    points += 5
                elif my_moves[i] == 0 and opp_moves[i] == 0:
                    points += 1

            avg_score = points / total_rounds

            score = (avg_score * 0.7) + (coop_rate * 0.3)

            rounds_left = max_rounds - len(my_moves)
            if rounds_left < 20:
                score *= 0.9

            if score > best_score:
                best_score = score
                best_opponent = opp_id

    if best_opponent is None:
        for opp_id in opponents_history.keys():
            if len(my_history.get(opp_id, [])) < max_rounds:
                return move, opp_id

    return move, best_opponent