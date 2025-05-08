def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    ZODIAC_SIGNS = [
        'ARIES', 'TAURUS', 'GEMINI', 'CANCER', 'LEO', 'VIRGO', 
        'LIBRA', 'SCORPIO', 'SAGITTARIUS', 'CAPRICORN', 'AQUARIUS', 'PISCES'
    ]
    
    RULES_OF_DESTINY = ['ELEMENT', 'DAY_AND_NIGHT_RULERSHIP', 'HEMISPHERE']
    
    ELEMENT_RULE = {
        'FIRE': ['ARIES', 'LEO', 'SAGITTARIUS'],
        'EARTH': ['TAURUS', 'VIRGO', 'CAPRICORN'],
        'AIR': ['GEMINI', 'LIBRA', 'AQUARIUS'],
        'WATER': ['CANCER', 'SCORPIO', 'PISCES']
    }
    
    DAY_AND_NIGHT_RULERSHIP = {
        'DAY': ['LEO', 'SAGITTARIUS', 'AQUARIUS', 'ARIES', 'LIBRA', 'GEMINI'],
        'NIGHT': ['CANCER', 'PISCES', 'CAPRICORN', 'SCORPIO', 'TAURUS', 'VIRGO']
    }
    
    HEMISPHERE_RULE = {
        'SPRING': ['ARIES', 'TAURUS', 'GEMINI'],
        'SUMMER': ['CANCER', 'LEO', 'VIRGO'],
        'FALL': ['LIBRA', 'SCORPIO', 'SAGITTARIUS'],
        'WINTER': ['CAPRICORN', 'AQUARIUS', 'PISCES']
    }
    
    PREDICTION_RESULT = 1
    
    my_moves = my_history.get(opponent_id, [])
    opponent_moves = opponents_history.get(opponent_id, [])
    
    player_destiny = sum(my_moves) + len(my_moves)
    player_rule_of_destiny = RULES_OF_DESTINY[player_destiny % 3]
    
    opponent_destiny = sum(opponent_moves) + len(my_moves)
    opponent_sign = ZODIAC_SIGNS[opponent_destiny % 12]
    
    if player_rule_of_destiny == 'ELEMENT':
        opponent_element = 'FIRE'
        for element in ELEMENT_RULE:
            if opponent_sign in ELEMENT_RULE[element]:
                opponent_element = element
        if opponent_element in ['FIRE', 'AIR']:
            PREDICTION_RESULT = 1
        else:
            PREDICTION_RESULT = 0
            
    elif player_rule_of_destiny == 'DAY_AND_NIGHT_RULERSHIP':
        opponent_time = 'DAY'
        for time in DAY_AND_NIGHT_RULERSHIP:
            if opponent_sign in DAY_AND_NIGHT_RULERSHIP[time]:
                opponent_time = time
        if opponent_time == 'DAY':
            PREDICTION_RESULT = 1
        else:
            PREDICTION_RESULT = 0
            
    elif player_rule_of_destiny == 'HEMISPHERE':
        opponent_season = 'SPRING'
        for season in HEMISPHERE_RULE:
            if opponent_sign in HEMISPHERE_RULE[season]:
                opponent_season = season
        if opponent_season in ['SPRING', 'SUMMER']:
            PREDICTION_RESULT = 1
        else:
            PREDICTION_RESULT = 0

    possible_opponents = [
        pid for pid in opponents_history 
        if len(my_history.get(pid, [])) < 200
    ]
    
    if not possible_opponents:
        next_opponent = opponent_id
    else:
        best_opponent = opponent_id
        best_prediction = -1
        
        for pid in possible_opponents:
            my_moves_other = my_history.get(pid, [])
            opponent_moves_other = opponents_history.get(pid, [])
            player_destiny_other = sum(my_moves_other) + len(my_moves_other)
            rule_of_destiny_other = RULES_OF_DESTINY[player_destiny_other % 3]
            opponent_destiny_other = sum(opponent_moves_other) + len(my_moves_other)
            opponent_sign_other = ZODIAC_SIGNS[opponent_destiny_other % 12]
            
            prediction = 1
            
            if rule_of_destiny_other == 'ELEMENT':
                opponent_element = 'FIRE'
                for element in ELEMENT_RULE:
                    if opponent_sign_other in ELEMENT_RULE[element]:
                        opponent_element = element
                if opponent_element not in ['FIRE', 'AIR']:
                    prediction = 0
                    
            elif rule_of_destiny_other == 'DAY_AND_NIGHT_RULERSHIP':
                opponent_time = 'DAY'
                for time in DAY_AND_NIGHT_RULERSHIP:
                    if opponent_sign_other in DAY_AND_NIGHT_RULERSHIP[time]:
                        opponent_time = time
                if opponent_time != 'DAY':
                    prediction = 0
                    
            elif rule_of_destiny_other == 'HEMISPHERE':
                opponent_season = 'SPRING'
                for season in HEMISPHERE_RULE:
                    if opponent_sign_other in HEMISPHERE_RULE[season]:
                        opponent_season = season
                if opponent_season not in ['SPRING', 'SUMMER']:
                    prediction = 0

            if prediction > best_prediction:
                best_prediction = prediction
                best_opponent = pid
        
        next_opponent = best_opponent

    return (PREDICTION_RESULT, next_opponent)
