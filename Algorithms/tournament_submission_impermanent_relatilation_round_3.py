
def strategy_round_3(opponent_id:int,my_history: dict[int,list[int]], opponents_history: dict[int,list[int]]) -> tuple[int,int]:

    func = lambda seed : (1664525*seed + 1013904223)%2**32
    curr_hist = my_history[opponent_id]
    opponent_history = opponents_history[opponent_id]

    response = 1

    lenl = len(curr_hist)-1
    if lenl >= 0:

        if curr_hist[lenl] == 0 or opponent_history[lenl] == 0:
            seed = 0
            for n in range(lenl):
                seed += (2**n) * curr_hist[n]
            forgive = func(seed) % 100 > 80

            response = int(forgive)

    # if it's the last possible game against this opponent, defect
    if lenl == 198 :
        respone = 0

    next_op = func(seed) % len(opponents_history.keys())

    min_def = lenl
    # find the most cooperative opponent
    for key in opponents_history:
        defections = sum(opponents_history[key])
        if min_def > defections and len(opponets_history[key]) < 200:
            next_op = key

    return tuple[next_op,response]

