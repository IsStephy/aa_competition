def strategy_round_2(opponent_id: int, my_history: dict[int, list[int]], 
                     opponents_history: dict[int, list[int]]) -> tuple[int, int]:
    """
    Enhanced strategy for Iterated Prisoner's Dilemma with opponent selection.
    This builds on the successful core algorithm by adding opponent reputation tracking
    and strategic opponent selection.
    
    Args:
        opponent_id: ID of the current opponent
        my_history: Dictionary of my past moves against all opponents
        opponents_history: Dictionary of all opponents' past moves against me
        
    Returns:
        tuple: (move, next_opponent)
            move: 0 for defect, 1 for cooperate
            next_opponent: ID of the next opponent to play with
    """
    # Get current histories with opponent
    my_moves = my_history.get(opponent_id, [])
    opp_moves = opponents_history.get(opponent_id, [])
    
    # Use the core strategy logic to decide the current move
    current_move = core_strategy(my_moves, opp_moves)
    
    # Build reputation system for all opponents
    opponent_reputations = build_opponent_reputations(my_history, opponents_history)
    
    # Choose next opponent based on reputation
    next_opponent = select_next_opponent(opponent_id, opponent_reputations, my_history)
    
    return current_move, next_opponent


def core_strategy(my_history: list[int], opponent_history: list[int]) -> int:
    """
    Core decision-making algorithm for choosing cooperation or defection.
    This preserves the original successful strategy logic.
    """
    # First move cooperation
    if len(my_history) == 0:
        return 1
    
    # Last round defection (we handle this differently since rounds param is not available)
    if len(my_history) == 199:  # 0-indexed, so 199 is the 200th round
        return 0
    
    def is_tit_for_tat(my_hist, opp_hist):
        if len(opp_hist) < 3 or opp_hist[0] != 1:
            return False
        matches = 0
        for i in range(1, len(my_hist)):
            if opp_hist[i] == my_hist[i - 1]:
                matches += 1
        return matches >= (len(my_hist) - 1) * 0.9
    
    def is_random_strategy(opp_hist):
        if len(opp_hist) < 20: 
            return False
        ones = opp_hist.count(1)
        proportion = ones / len(opp_hist)
        return 0.4 <= proportion <= 0.6
    
    def detect_exploitation_pattern(my_hist, opp_hist):
        """Detect if opponent exploits cooperation"""
        if len(my_hist) < 10:
            return False
            
        defect_after_coop = 0
        coop_count = 0
        
        for i in range(len(my_hist) - 1):
            if my_hist[i] == 1:
                coop_count += 1
                if opp_hist[i+1] == 0:
                    defect_after_coop += 1
        return coop_count > 0 and defect_after_coop / coop_count > 0.6
    
    def detect_pattern(hist, length=3):
        """Check if there's a repeating pattern of given length"""
        if len(hist) < length * 2:
            return False, None
            
        for i in range(len(hist) - length * 2 + 1):
            pattern = hist[i:i+length]
            next_seq = hist[i+length:i+length*2]
            if pattern == next_seq:
                return True, pattern
        return False, None
    
    if is_tit_for_tat(my_history, opponent_history):
        return 1
    
    if is_random_strategy(opponent_history):
        return 0
    
    if detect_exploitation_pattern(my_history, opponent_history):
        return 0
    
    has_pattern, pattern = detect_pattern(opponent_history, 3)
    if has_pattern and pattern:
        next_predicted = pattern[len(my_history) % len(pattern)]
        return 1 if next_predicted == 1 else 0
    
    if len(my_history) >= 2:
        if all(move == 0 for move in my_history[-2:]) and all(move == 0 for move in opponent_history[-2:]):
            return 1
    
    recent_window = min(10, len(opponent_history))
    recent_coop_rate = sum(opponent_history[-recent_window:]) / recent_window
    
    if recent_coop_rate > 0.7:
        return 1
    
    if recent_coop_rate < 0.3:
        return 0
    
    if opponent_history[-1] == 1:
        return 1
    else:
        # Replace random with deterministic decision based on game state
        # This removes the random dependency which isn't allowed
        return 1 if (len(my_history) % 5 == 0) else 0


def build_opponent_reputations(my_history: dict[int, list[int]], 
                             opponents_history: dict[int, list[int]]) -> dict:
    """
    Builds a comprehensive reputation system for all opponents.
    
    Returns a dictionary with opponent_id as key and reputation metrics as values.
    """
    reputations = {}
    
    for opp_id in opponents_history:
        my_moves = my_history.get(opp_id, [])
        opp_moves = opponents_history.get(opp_id, [])
        
        # Calculate metrics only if we have history with this opponent
        if not opp_moves:
            reputations[opp_id] = {
                'score_potential': 3.0,  # Expected score from mutual cooperation
                'cooperativeness': 1.0,  # Initially assume cooperative
                'exploitability': 0.5,   # Unknown exploitability
                'stability': 0.5,        # Unknown stability
                'rounds_played': 0,
                'pattern': 'unknown'
            }
            continue
        
        # Calculate cooperation rate
        coop_rate = sum(opp_moves) / len(opp_moves)
        
        # Calculate my average score per round against this opponent
        my_score = 0
        for i in range(len(my_moves)):
            if my_moves[i] == 1 and opp_moves[i] == 1:  # Both cooperate
                my_score += 3
            elif my_moves[i] == 0 and opp_moves[i] == 1:  # I defect, they cooperate
                my_score += 5
            elif my_moves[i] == 0 and opp_moves[i] == 0:  # Both defect
                my_score += 1
            # If I cooperate and they defect, I get 0 points
        
        avg_score = my_score / len(my_moves) if my_moves else 0
        
        # Detect if opponent is tit-for-tat
        is_tft = False
        if len(my_moves) > 1:
            tft_matches = sum(1 for i in range(1, len(opp_moves)) if opp_moves[i] == my_moves[i-1])
            is_tft = tft_matches >= (len(my_moves) - 1) * 0.9
        
        # Detect if opponent always cooperates
        always_coop = all(move == 1 for move in opp_moves)
        
        # Detect if opponent always defects
        always_defect = all(move == 0 for move in opp_moves)
        
        # Calculate stability (consistency of behavior)
        if len(opp_moves) < 3:
            stability = 0.5
        else:
            # Look at how often they change their strategy
            changes = sum(1 for i in range(len(opp_moves)-1) if opp_moves[i] != opp_moves[i+1])
            stability = 1.0 - (changes / (len(opp_moves) - 1))
        
        # Determine pattern
        if always_coop:
            pattern = 'always_cooperate'
            exploitability = 1.0  # Highly exploitable
        elif always_defect:
            pattern = 'always_defect'
            exploitability = 0.0  # Not exploitable
        elif is_tft:
            pattern = 'tit_for_tat'
            exploitability = 0.3  # Somewhat exploitable
        elif coop_rate > 0.8:
            pattern = 'mostly_cooperate'
            exploitability = 0.8  # Quite exploitable
        elif coop_rate < 0.2:
            pattern = 'mostly_defect'
            exploitability = 0.1  # Not very exploitable
        else:
            pattern = 'mixed'
            exploitability = 0.5  # Moderately exploitable
        
        # Calculate score potential (expected points we can get)
        # For always cooperate: we can get 5 points consistently by defecting
        # For tit-for-tat: we can get 3 points consistently by cooperating
        if pattern == 'always_cooperate':
            score_potential = 5.0
        elif pattern == 'always_defect':
            score_potential = 1.0
        elif pattern == 'tit_for_tat':
            score_potential = 3.0
        else:
            # Use our average score so far as prediction
            score_potential = avg_score
            
            # Adjust based on exploitability
            score_potential = min(5.0, score_potential * (1 + exploitability * 0.5))
        
        reputations[opp_id] = {
            'score_potential': score_potential,
            'cooperativeness': coop_rate,
            'exploitability': exploitability,
            'stability': stability,
            'rounds_played': len(my_moves),
            'pattern': pattern,
            'avg_score': avg_score
        }
    
    return reputations


def select_next_opponent(current_id: int, reputations: dict, my_history: dict[int, list[int]]) -> int:
    """
    Select the next opponent based on their reputation and our strategy.
    
    This function implements a sophisticated selection strategy that balances:
    1. Exploitation - play against opponents we can score well against
    2. Exploration - try new or less-played opponents
    3. Strategic timing - avoid exhausting rounds with highly profitable opponents too early
    """
    # Filter out opponents we've already played maximum rounds with
    available_opponents = [opp_id for opp_id in reputations 
                          if opp_id in my_history and len(my_history[opp_id]) < 200]
    
    if not available_opponents:
        return current_id  # Fallback to current if no options
    
    # Calculate selection scores for each opponent
    selection_scores = {}
    for opp_id in available_opponents:
        rep = reputations[opp_id]
        rounds_played = rep['rounds_played']
        
        # Base score is the expected points per round
        score = rep['score_potential']
        
        # Add exploration bonus for opponents we haven't played much with
        # This decreases as we play more rounds with them
        exploration_bonus = max(0, 1.0 - (rounds_played / 20))
        
        # Add stability bonus - prefer predictable opponents
        stability_bonus = rep['stability'] * 0.5
        
        # Special handling for different patterns
        if rep['pattern'] == 'always_cooperate':
            # Highly valuable but don't exhaust too early
            pattern_bonus = 2.0 - (rounds_played / 100)
        elif rep['pattern'] == 'tit_for_tat':
            # Good stable relationship, value increases as game progresses
            pattern_bonus = 1.0 + (rounds_played / 200)
        elif rep['pattern'] == 'always_defect':
            # Avoid unless we have few options
            pattern_bonus = -1.0
        else:
            pattern_bonus = 0.0
            
        # Calculate final score
        final_score = score + exploration_bonus + stability_bonus + pattern_bonus
        
        # Slightly prefer sticking with current opponent if they're good
        if opp_id == current_id and rep['score_potential'] > 2.5:
            final_score += 0.2
            
        selection_scores[opp_id] = final_score
    
    # Special case: if we haven't explored many opponents yet, prioritize exploration
    if len([opp for opp in reputations if reputations[opp]['rounds_played'] > 0]) < 5:
        # Find least played opponents
        min_rounds = min(reputations[opp]['rounds_played'] for opp in available_opponents)
        candidates = [opp for opp in available_opponents 
                     if reputations[opp]['rounds_played'] == min_rounds]
        return candidates[0]  # Choose first of the least played opponents
    
    # Select opponent with highest score
    return max(selection_scores.items(), key=lambda x: x[1])[0]