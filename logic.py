
def calculate_google_rating_score(r1: float, r2: float) -> int:
    """
    Avg of 2 ratings -> Score.
    4 and above 10pt
    3.9 9pt
    3.8 8pt
    3.7 7pt
    3.6 6pt
    3.5 5pt
    Below 0pt (Assumed < 3.5 is 0)
    """
    avg = (r1 + r2) / 2
    if avg >= 4.0: return 10
    if avg >= 3.9: return 9
    if avg >= 3.8: return 8
    if avg >= 3.7: return 7
    if avg >= 3.6: return 6
    if avg >= 3.5: return 5
    return 0

def calculate_zomato_swiggy_score(ratings: list[float]) -> int:
    """
    Avg of 4 ratings -> Score.
    Same scale as Google.
    """
    if not ratings: return 0
    avg = sum(ratings) / len(ratings)
    # Rounding? Prompt doesn't specify, but tables are specific (3.9, 3.8). 
    # Validating against exact thresholds.
    if avg >= 4.0: return 10
    if avg >= 3.9: return 9
    if avg >= 3.8: return 8
    if avg >= 3.7: return 7
    if avg >= 3.6: return 6
    if avg >= 3.5: return 5
    return 0

def calculate_food_cost_score(amritsari_pct: float, chennai_pct: float) -> int:
    """
    Amritsari: 22% & below(10), 23(9), 24(8), 25(7), 26(6), 27(5), >27(0)
    Chennai: 18% & below(10), 19(9), 20(8), 21(7), 22(5), >22(0)
    Total = Sum of scores.
    """
    # Amritsari
    s1 = 0
    if amritsari_pct <= 22: s1 = 10
    elif amritsari_pct <= 23: s1 = 9
    elif amritsari_pct <= 24: s1 = 8
    elif amritsari_pct <= 25: s1 = 7
    elif amritsari_pct <= 26: s1 = 6
    elif amritsari_pct <= 27: s1 = 5
    else: s1 = 0

    # Chennai
    s2 = 0
    if chennai_pct <= 18: s2 = 10
    elif chennai_pct <= 19: s2 = 9
    elif chennai_pct <= 20: s2 = 8
    elif chennai_pct <= 21: s2 = 7
    elif chennai_pct <= 22: s2 = 5
    else: s2 = 0
    
    return s1 + s2

def calculate_online_activity_score(percentages: list[float]) -> int:
    """
    Avg of 4 percentages.
    98% & above 10pt
    97% 8pt
    96% 6pt
    95% 4pt
    Below 95% 0pt
    """
    if not percentages: return 0
    avg = sum(percentages) / len(percentages)
    
    if avg >= 98: return 10
    if avg >= 97: return 8
    if avg >= 96: return 6
    if avg >= 95: return 4
    return 0

def calculate_kitchen_prep_score(times: list[float]) -> int:
    """
    Avg of 4 times.
    Less than 10 mins 12pt (Assuming <10)
    10-15 mins 10pt
    16 9pt
    17 8pt
    18 7pt
    19 6pt
    20 5pt
    Above 20 0pt
    """
    if not times: return 0
    avg = sum(times) / len(times)
    
    if avg < 10: return 12
    if avg <= 15: return 10
    if avg <= 16: return 9
    if avg <= 17: return 8
    if avg <= 18: return 7
    if avg <= 19: return 6
    if avg <= 20: return 5
    return 0

def calculate_bad_delay_score(bad_pcts: list[float], delay_pcts: list[float]) -> int:
    """
    Bad Score: Avg of 4 bad pcts.
    3%(5), 5%(4), 7%(3), 9%(2), 11%(1), >11(0)
    
    Delay Score: Avg of 4 delay pcts.
    10%(5), 12%(4), 14%(3), 16%(2), 18%(1), >18(0)

    Total = Bad Score + Delay Score
    """
    # Bad
    bad_score = 0
    if bad_pcts:
        avg_bad = sum(bad_pcts) / len(bad_pcts)
        if avg_bad <= 3: bad_score = 5
        elif avg_bad <= 5: bad_score = 4
        elif avg_bad <= 7: bad_score = 3
        elif avg_bad <= 9: bad_score = 2
        elif avg_bad <= 11: bad_score = 1
        else: bad_score = 0
        
    # Delay
    delay_score = 0
    if delay_pcts:
        avg_delay = sum(delay_pcts) / len(delay_pcts)
        if avg_delay <= 10: delay_score = 5
        elif avg_delay <= 12: delay_score = 4
        elif avg_delay <= 14: delay_score = 3
        elif avg_delay <= 16: delay_score = 2
        elif avg_delay <= 18: delay_score = 1
        else: delay_score = 0
        
    return bad_score + delay_score

def calculate_outlet_audit_score(mistakes_amritsari: int, mistakes_chennai: int) -> float:
    """
    Score each separately out of 20. Then Avg.
    10(0)...0(20). Formula: 20 - 2*mistakes, bounded 0-20.
    """
    def score_mistakes(m):
        raw = 20 - (2 * m)
        return max(0, min(20, raw))
        
    s1 = score_mistakes(mistakes_amritsari)
    s2 = score_mistakes(mistakes_chennai)
    return (s1 + s2) / 2

def calculate_add_on_sale_score(ts_a: float, aos_a: float, ts_c: float, aos_c: float) -> float:
    """
    Rating(%) = AOS/TS * 100
    16 & Above% 10+2 (12)
    15% 10
    14% 8
    13% 6
    12% 4
    11% 2
    10% & Below 0
    
    Avg of the 2 scores.
    """
    def score_aos(ts, aos):
        if ts == 0: return 0
        pct = (aos / ts) * 100
        if pct >= 16: return 12
        if pct >= 15: return 10
        if pct >= 14: return 8
        if pct >= 13: return 6
        if pct >= 12: return 4
        if pct >= 11: return 2
        return 0

    s1 = score_aos(ts_a, aos_a)
    s2 = score_aos(ts_c, aos_c)
    return (s1 + s2) / 2

