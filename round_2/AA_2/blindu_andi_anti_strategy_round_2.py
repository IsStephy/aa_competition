def strategy_round_2(
    opponent_id: int,
    my_history: dict[int, list[int]],
    opponents_history: dict[int, list[int]],
) -> tuple[int, int]:
    MAX_ROUNDS = 200

    my_moves   = my_history.get(opponent_id, [])
    opp_moves  = opponents_history.get(opponent_id, [])
    round_num  = len(my_moves)

    if round_num == 0:
        move = 1                         # start cooperant
    elif round_num + 1 == MAX_ROUNDS:
        move = 0                         # ultima rundă cu acest adversar → defect
    else:
        total = round_num
        coop_r = opp_moves.count(1) / total if total else 1
        def_r  = opp_moves.count(0) / total if total else 0

        # detectori (aceiași ca în prima etapă, dar interni)
        def is_all_c()      : return def_r < 0.05
        def is_all_d()      : return coop_r < 0.05
        def is_tft()        : return all(opp_moves[i] == my_moves[i-1] for i in range(1, total))
        def is_gt()         : return 0 in my_moves and opp_moves[my_moves.index(0):] == [0]*(total-my_moves.index(0))
        def is_pavlov()     : return total > 2 and all((my_moves[i]==opp_moves[i])==(my_moves[i+1]==my_moves[i]) for i in range(total-2))
        def is_tft2()       : return total > 2 and any(my_moves[i-1]==my_moves[i-2]==0 and opp_moves[i]==0 for i in range(2,total))
        def is_randlike()   : return 0.35 < coop_r < 0.65
        def is_generous()   : return coop_r > 0.7 and opp_moves[-1] == 1
        def is_spiteful()   : return 0 in my_moves and 0 in opp_moves[my_moves.index(0):] and 1 not in opp_moves[my_moves.index(0):]
        def is_copykitten() : return is_tft() and opp_moves.count(0) < 3
        def is_probe()      : return opp_moves[:3] == [0,1,1] and coop_r > 0.7
        def is_inv_tft()    : return all(opp_moves[i] != my_moves[i-1] for i in range(1,total))
        def is_lookback()   : return total >= 5 and opp_moves[-1] == opp_moves[-5]
        def is_switcher()   : return total >= 4 and len(set(opp_moves[-4:])) > 1
        def is_trigger()    : return total > 4 and opp_moves[-3:] == [0,0,0]
        def is_cycle_cdd()  : return total > 3 and opp_moves[-3:] == [1,0,0]
        def is_cycle_dcc()  : return total > 3 and opp_moves[-3:] == [0,1,1]
        def is_alt_pat()    : return total > 5 and all(opp_moves[i] != opp_moves[i-1] for i in range(1, min(total,6)))
        def is_repeater()   : return total > 3 and len(set(opp_moves[-3:])) == 1
        def is_noisy_tft()  : return total >= 5 and sum(abs(opp_moves[i]-my_moves[i-1]) for i in range(1,5)) == 1
        def is_soft_mafia() : return opp_moves[:3] == [1,1,0] and coop_r > 0.5
        def is_alt_abuser(): return total >= 6 and opp_moves[-6:] == [1,0,1,0,1,0]
        def is_defect10()  : return total >= 10 and opp_moves[9] == 0
        def is_rand_grim() : return total >= 10 and opp_moves[:5].count(0) >= 2 and all(x == 0 for x in opp_moves[5:])

        if is_all_c() or is_all_d():               move = 0
        elif is_tft() or is_copykitten():          move = opp_moves[-1]
        elif is_gt():                              move = 1 if 0 not in my_moves else 0
        elif is_pavlov():                          move = my_moves[-1] if my_moves[-1] == opp_moves[-1] else 1 - my_moves[-1]
        elif is_tft2():                            move = opp_moves[-1] if opp_moves[-2:] != [0,0] else 0
        elif is_generous() or is_probe():          move = 0
        elif is_spiteful():                        move = 1
        elif is_randlike() or is_switcher():       move = 0
        elif is_inv_tft():                         move = 1
        elif is_lookback():                        move = opp_moves[-1]
        elif is_trigger():                         move = 1
        elif is_cycle_cdd():                       move = 1
        elif is_cycle_dcc():                       move = 0
        elif is_alt_pat():                         move = 0
        elif is_repeater() or is_noisy_tft():      move = opp_moves[-1]
        elif is_soft_mafia() or is_alt_abuser():   move = 0
        elif is_defect10() or is_rand_grim():      move = 0
        elif opp_moves and opp_moves[-1] == 0:     move = 0
        elif total >=2 and my_moves[-1]==0 and opp_moves[-2:]==[0,1]:
                                                   move = 1
        else:                                      move = 1

    def coop_rate(pid: int) -> float:
        hist = opponents_history.get(pid, [])
        return sum(hist) / len(hist) if hist else 1.0

    eligible = [
        pid for pid in set(my_history) | set(opponents_history)
        if len(my_history.get(pid, [])) < MAX_ROUNDS
    ]

    if opponent_id in eligible and coop_rate(opponent_id) > 0.6:
        next_opponent = opponent_id
    elif eligible:
        best_rate = max(coop_rate(pid) for pid in eligible)
        best_ids  = [pid for pid in eligible if coop_rate(pid) == best_rate]
        next_opponent = min(best_ids)
    else:
        next_opponent = opponent_id  # toate listele au 200 runde

    return move, next_opponent
