def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    if not my_history:
        if rounds is not None and rounds > 50:
            return 1
        else:
            return 0

    current_round = len(my_history)

    trust_score = 0.5

    recent_history = opponent_history[-20:] if len(opponent_history) > 20 else opponent_history
    for i, move in enumerate(recent_history):
        weight = 0.7 * (i + 1) / len(recent_history)
        if move == 1:
            trust_score += weight * 0.1
        else:  
            trust_score -= weight * 0.2

    trust_score = max(0.0, min(1.0, trust_score))

    pattern_prediction = None
    if len(opponent_history) >= 4:
        latest_pattern = opponent_history[-3:]
        for i in range(len(opponent_history) - 6):
            if opponent_history[i:i+3] == latest_pattern:
                prediction_index = i + 3
                if prediction_index < len(opponent_history):
                    pattern_prediction = opponent_history[prediction_index]
                    break

    recent_my_history = my_history[-10:] if len(my_history) > 10 else my_history
    recent_opp_history = opponent_history[-10:] if len(opponent_history) > 10 else opponent_history
    
    always_cooperates_after_cooperation = False
    always_defects_after_cooperation = False
    always_cooperates_after_defection = False
    always_defects_after_defection = False

    if len(recent_my_history) >= 3:
        cooperation_followed_by_cooperation = 0
        cooperation_followed_by_defection = 0
        defection_followed_by_cooperation = 0
        defection_followed_by_defection = 0

        for i in range(len(recent_my_history) - 1):
            if recent_my_history[i] == 1:
                if recent_opp_history[i+1] == 1:
                    cooperation_followed_by_cooperation += 1
                else:
                    cooperation_followed_by_defection += 1
            else:
                if recent_opp_history[i+1] == 1:
                    defection_followed_by_cooperation += 1
                else:
                    defection_followed_by_defection += 1

        # check if any pattern is consistent
        total_after_cooperation = cooperation_followed_by_cooperation + cooperation_followed_by_defection
        if total_after_cooperation >= 3:
            if cooperation_followed_by_cooperation == total_after_cooperation:
                always_cooperates_after_cooperation = True
            elif cooperation_followed_by_defection == total_after_cooperation:
                always_defects_after_cooperation = True

        total_after_defection = defection_followed_by_cooperation + defection_followed_by_defection
        if total_after_defection >= 3:
            if defection_followed_by_cooperation == total_after_defection:
                always_cooperates_after_defection = True
            elif defection_followed_by_defection == total_after_defection:
                always_defects_after_defection = True

    if rounds is not None:
        remaining_rounds = rounds - current_round
        if remaining_rounds <= 3:
 
            return 0

    # check if opponent is overly aggressive
    defection_rate = opponent_history.count(0) / len(opponent_history) if opponent_history else 0

    if defection_rate > 0.7 and len(opponent_history) >= 5:
        return 0

    # exploit predictable patterns
    if pattern_prediction is not None:
        if pattern_prediction == 1:
            return 0
        else:
            return 0

    if my_history[-1] == 1:
        if always_defects_after_cooperation:
            return 0
        elif always_cooperates_after_cooperation:
            if trust_score < 0.7:
                return 0
    else:
        if always_cooperates_after_defection:
            return 0
        elif always_defects_after_defection:
            if trust_score > 0.3:
                return 1
            else:
                return 0

    if opponent_history[-1] == 0:
        if trust_score > 0.6:
            return 1
        else:
            return 0

    if trust_score > 0.4:
        return 1
    else:
        return 0 