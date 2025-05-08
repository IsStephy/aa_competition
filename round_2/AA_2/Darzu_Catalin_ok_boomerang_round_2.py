def strategy_round_2(
    opponent_id: int,
    my_history: dict[int, list[int]],
    opponents_history: dict[int, list[int]]
) -> tuple[int, int]:
    """
    OK Boomerang Stage 2:
    - Same sliding-window regret + forgiveness as in Stage 1.
    - Chooses next opponent as the one with highest cooperation rate,
      excluding any with whom we've already played ≥200 rounds.
    """
    # --- Parameters from Stage 1 ---
    COOP_THRESHOLD    = 0.30
    DEFECT_THRESHOLD  = 0.70
    FORGIVE_THRESHOLD = 0.50
    WINDOW_MIN, WINDOW_MAX = 1, 20

    # --- Extract histories for current opponent ---
    mine = my_history.get(opponent_id, [])
    theirs = opponents_history.get(opponent_id, [])

    # --- 1) Decide this round's move ---
    if not mine:
        move = 1
    else:
        # window ~10% of #rounds played so far, capped
        window = len(mine) // 10
        if window < WINDOW_MIN:
            window = WINDOW_MIN
        elif window > WINDOW_MAX:
            window = WINDOW_MAX

        recent = theirs[-window:] if len(theirs) >= window else theirs
        defect_ratio = (recent.count(0) / len(recent)) if recent else 0.0

        if defect_ratio <= COOP_THRESHOLD:
            move = 1
        elif defect_ratio >= DEFECT_THRESHOLD:
            move = 0
        else:
            last = theirs[-1]
            # forgive a mutual defection if overall regret is still low
            if (
                mine[-1] == 0
                and last == 0
                and defect_ratio < FORGIVE_THRESHOLD
            ):
                move = 1
            else:
                move = last

    # --- 2) Pick next opponent ---
    candidates = [
        pid
        for pid, hist in opponents_history.items()
        if len(my_history.get(pid, [])) < 200
    ]
    if not candidates:
        # no one left → stay with current
        return move, opponent_id

    best_pid = None
    best_rate = -1.0
    for pid in candidates:
        h = opponents_history.get(pid, [])
        rate = (h.count(1) / len(h)) if h else 1.0
        if rate > best_rate or (rate == best_rate and (best_pid is None or pid < best_pid)):
            best_rate, best_pid = rate, pid

    return move, best_pid
