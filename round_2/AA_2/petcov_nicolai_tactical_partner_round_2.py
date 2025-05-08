
def strategy_round_2(opponent_id: int,
                     my_history: dict[int, list[int]],
                     opponents_history: dict[int, list[int]]) -> tuple[int, int]:

    current_opponent_moves = opponents_history[opponent_id]
    my_moves_with_current = my_history.get(opponent_id, [])

    if not current_opponent_moves:
        move = 1
    else:
        recent_moves = current_opponent_moves[-3:] if len(current_opponent_moves) >= 3 else current_opponent_moves

        if sum(recent_moves) == 0:
            move = 0
        elif sum(recent_moves) == len(recent_moves):
            if len(my_moves_with_current) > 5 and hash(tuple(my_moves_with_current[-3:] + current_opponent_moves[-3:])) % 4 == 0:
                move = 0
            else:
                move = 1
        else:
            if hash(tuple(my_moves_with_current[-2:] + current_opponent_moves[-2:])) % 7 == 0:
                move = 1 - current_opponent_moves[-1]
            else:
                move = current_opponent_moves[-1]

    available_opponents = [oid for oid in opponents_history if len(my_history.get(oid, [])) < 200]

    if not available_opponents:
        return (move, opponent_id)

    def evaluate_opponent(oid):
        opp_moves = opponents_history[oid]
        if not opp_moves:
            return 0.7

        total_rounds = len(opp_moves)
        coop_rate = sum(opp_moves) / total_rounds
        last_5 = opp_moves[-5:] if total_rounds >= 5 else opp_moves
        trend = sum(last_5) / len(last_5)
        penalty = 0.2 if 0 in last_5 else 0
        bonus = 0.15 if trend == 1 else 0
        return (coop_rate * 0.6) + (trend * 0.3) - penalty + bonus

    if len(available_opponents) > 1:
        if hash(tuple(my_moves_with_current)) % 10 < 7:
            next_opponent = max(available_opponents, key=evaluate_opponent)
        else:
            next_opponent = min(available_opponents, key=lambda oid: len(my_history.get(oid, [])))
    else:
        next_opponent = available_opponents[0]

    return (move, next_opponent)