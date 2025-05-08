def strategy_round_2(opponent_id:int,my_history: dict[int,list[int]], opponents_history: dict[int,list[int]]) -> tuple[int,int]:

    func = lambda seed : (1664525*seed + 1013904223)%2**32
    curr_hist = my_history[opponent_id]
    opponent_history = opponents_history[opponent_id]
    seed = 0
    response = 1

    lenl = len(curr_hist)-1
    if lenl >= 0:

        if curr_hist[lenl] == 0 or opponent_history[lenl] == 0:
           
            for n in range(lenl):
                seed += (2**n) * curr_hist[n]
            forgive = func(seed) % 100 > 80

            response = int(forgive)

    # if it's the last possible game against this opponent, defect
    if lenl == 198 :
        response = 0

    # Find valid opponents who haven't reached 200 interactions
    valid_opponents = []
    for key in opponents_history.keys():
        if len(opponents_history[key]) < 200:
            valid_opponents.append(key)
    
    # Default to a random next opponent if we can't find a cooperative one
    next_op = valid_opponents[func(seed) % len(valid_opponents)] if valid_opponents else opponent_id
    
    # Find the most cooperative opponent (lowest number of defections)
    min_defections = float('inf')  # Start with "infinity"
    
    for key in valid_opponents:
        # Count defections (where history entry is 0)
        defections = sum(1 - val for val in opponents_history[key])
        
        # If we found a more cooperative opponent with room for more interactions
        if defections < min_defections and len(opponents_history[key]) < 200:
            min_defections = defections
            next_op = key

    return (response,next_op)
