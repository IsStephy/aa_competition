
def strategy_round_2(
    opponent_id: int,
    my_history: dict[int, list[int]],
    opponents_history: dict[int, list[int]]
) -> tuple[int, int]:
    def calculate_cooperation_rate(history: list[int]) -> float:
        if not history:
            return 0.5
        return sum(history) / len(history)

    def detect_alternating_pattern(history: list[int]) -> bool:
        if len(history) < 3:
            return False
        return history[-3:] in ([1, 0, 1], [0, 1, 0])

    def select_next_opponent(current: int) -> int:
        max_rounds = 200
        # all IDs are in my_history, with [] if never played
        candidates = [
            oid for oid, hist in my_history.items()
            if oid != current and len(hist) < max_rounds
        ]
        if not candidates:
            return current
        # as before, pick the one you’ve played the fewest rounds with
        return min(candidates, key=lambda oid: len(my_history[oid]))

    my_moves = my_history.get(opponent_id, [])
    opp_moves = opponents_history.get(opponent_id, [])

    # first move ever → cooperate
    if not my_moves:
        return (1, select_next_opponent(opponent_id))

    # if you’re at round 200 with this opponent, defect and move on
    if len(my_moves) >= 199:
        return (0, select_next_opponent(opponent_id))

    coop_rate = calculate_cooperation_rate(opp_moves)

    # exploit too-nice or punish too-nasty
    if coop_rate > 0.7 or coop_rate < 0.3:
        return (0, select_next_opponent(opponent_id))

    # punish obvious alternators
    if detect_alternating_pattern(opp_moves):
        return (0, select_next_opponent(opponent_id))

    # every 10th round, try a cooperative test
    if len(my_moves) % 10 == 0:
        return (1, select_next_opponent(opponent_id))

    # otherwise mirror their last move (or start with cooperate)
    return (
        opp_moves[-1] if opp_moves else 1,
        select_next_opponent(opponent_id)
    )
