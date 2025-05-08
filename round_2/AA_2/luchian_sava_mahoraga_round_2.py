def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:

    def next_opponent(my_history, opponents_history, opponent_id):
        
        def count_algorithms_with_pattern(my_history, opponents_history):
            count = 0
            for opp_id, history in my_history.items():
                if len(history) >= 199:
                    if all(opponents_history[opp_id][-7 + i] == 1 for i in range(5)) and all(my_history[opp_id][-7 + i] == 0 for i in range(5)):
                        count += 1
            return count >= 5

        def has_three_consecutive_defections(history):
            for i in range(len(history) - 2):
                if history[i] == 0 and history[i+1] == 0 and history[i+2] == 0:
                    return True
            return False
        
        def cooperation_rate(opp_history):
            if not opp_history:
                return 0 
            return sum(opp_history) / len(opp_history)
        
        eligible_opponents = [
                opp_id for opp_id, history in my_history.items()
                if len(history) < 200 and (len(opponents_history[opp_id]) == 0 or opponents_history[opp_id][0] == 1) and not has_three_consecutive_defections(opponents_history[opp_id])
            ]

        if not eligible_opponents:
            eligible_opponents = [
                opp_id for opp_id, history in my_history.items()
                if len(history) < 200 
            ]

        if not count_algorithms_with_pattern(my_history, opponents_history):
            if len(opponents_history[opponent_id]) > 0 and opponents_history[opponent_id][-1] == 0 and opponents_history[opponent_id].count(0) == 1 and len(opponents_history[opponent_id]) < 200 and (len(opponents_history[opponent_id]) == 0 or opponents_history[opponent_id][0] == 1):
                return opponent_id

            if len(my_history[opponent_id]) > 0 and len(opponents_history[opponent_id]) > 0:
                if my_history[opponent_id][-1] == 0 and opponents_history[opponent_id][-1] == 1 and len(opponents_history[opponent_id]) < 200:
                    return opponent_id

            next_opponent = min(eligible_opponents, key=lambda opp_id: len(opponents_history[opp_id]))
            return next_opponent
        else:

            next_opponent = max(eligible_opponents, key=lambda opp_id: cooperation_rate(opponents_history[opp_id]))
            return next_opponent
        
        if not eligible_opponents:
            return opponent_id
        
    current_opponent_history = opponents_history.get(opponent_id, [])
    my_current_history = my_history.get(opponent_id, [])

    if len(my_current_history) == 0:
        return 1, next_opponent(my_history, opponents_history, opponent_id)  

    if len(my_current_history) >= 200:
        return 0, next_opponent(my_history, opponents_history, opponent_id)

    def is_tit_for_tat(my_hist, opp_hist):
        if len(opp_hist) == 0 or opp_hist[0] != 1:
            return False
        for i in range(1, len(my_hist)):
            if opp_hist[i] != my_hist[i - 1]:
                return False
        return True

    def is_random(opp_hist, my_hist):
        if len(opp_hist) < 15:
            return False

        ones = opp_hist.count(1)
        proportion = ones / len(opp_hist)

        if not (0.45 <= proportion <= 0.55):
            return False

        if is_tit_for_tat(my_hist, opp_hist):
            return False
        return True

    def check_coop_rate(my_history, opponent_history):
        count_aux = 0
        count = 0
        
        for i in range(min(len(my_history), 25) - 2):
            my_subarray = my_history[i:i+3]
            opp_subarray = opponent_history[i:i+3]
            
            coop_rate = my_subarray.count(1) / len(my_subarray)
            
            if coop_rate > 0.8 and opp_subarray[-1] == 0 and opp_subarray[-2]:
                count_aux += 1 
                
                if count_aux >= 2:
                    count += 1
                    count_aux = 0
                if count >= 1:
                    return True
                    
        return False
    
    if len(my_current_history) > 12 and len(my_current_history) < 15:
        return 0, next_opponent(my_history, opponents_history, opponent_id) 
    if is_tit_for_tat(my_current_history, current_opponent_history):
        return 1, next_opponent(my_history, opponents_history, opponent_id) 

    if is_random(current_opponent_history, my_current_history):
        return 0, next_opponent(my_history, opponents_history, opponent_id) 

    if check_coop_rate(my_current_history, current_opponent_history):
        if len(my_current_history) == 199: 
            return 0, next_opponent(my_history, opponents_history, opponent_id) 
        else:
            return 0, opponent_id  


    if len(my_current_history) > 6:
        for i in range(len(current_opponent_history) - 6):
            last_6_opponent = current_opponent_history[i:i+6]
            last_6_my = my_current_history[i:i+6]
            if all(move == 0 for move in last_6_opponent) and last_6_my.count(1) >= 2:
                return 0, next_opponent(my_history, opponents_history, opponent_id)

    my_last = my_current_history[-1]
    their_last = current_opponent_history[-1]

    if my_last == 0 and their_last == 0:
        return 1, next_opponent(my_history, opponents_history, opponent_id)
    elif my_last == their_last:
        return my_last, next_opponent(my_history, opponents_history, opponent_id)
    else:
        return 0, next_opponent(my_history, opponents_history, opponent_id)
    return 0, next_opponent(my_history, opponents_history, opponent_id)

