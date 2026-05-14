from typing import Optional, List

def calculate_google_rating_score(r1: Optional[float], r2: Optional[float], r3: Optional[float]) -> int:
    valid = [v for v in (r1, r2, r3) if v is not None]
    if not valid: return 0
    avg = sum(valid) / len(valid)
    if avg >= 4.0: return 10
    if avg >= 3.9: return 9
    if avg >= 3.8: return 8
    if avg >= 3.7: return 7
    if avg >= 3.6: return 6
    if avg >= 3.5: return 5
    return 0

def calculate_zomato_swiggy_score(ratings: List[Optional[float]]) -> int:
    valid = [r for r in ratings if r is not None]
    if not valid: return 0
    avg = sum(valid) / len(valid)
    if avg >= 4.0: return 10
    if avg >= 3.9: return 9
    if avg >= 3.8: return 8
    if avg >= 3.7: return 7
    if avg >= 3.6: return 6
    if avg >= 3.5: return 5
    return 0

def calculate_food_cost_score(amritsari_pct: Optional[float], chennai_pct: Optional[float], chaat_masala_pct: Optional[float]) -> float:
    def score_amritsari(pct):
        if pct <= 22: return 10
        if pct <= 23: return 9
        if pct <= 24: return 8
        if pct <= 25: return 7
        if pct <= 26: return 6
        if pct <= 27: return 5
        return 0

    def score_chennai(pct):
        if pct <= 18: return 10
        if pct <= 19: return 9
        if pct <= 20: return 8
        if pct <= 21: return 7
        if pct <= 22: return 5
        return 0

    def score_chaat_masala(pct):
        if pct <= 24: return 10
        if pct <= 25: return 9
        if pct <= 26: return 8
        if pct <= 27: return 7
        if pct <= 28: return 6
        if pct <= 29: return 5
        return 0

    scores = []
    if amritsari_pct is not None: scores.append(score_amritsari(amritsari_pct))
    if chennai_pct is not None: scores.append(score_chennai(chennai_pct))
    if chaat_masala_pct is not None: scores.append(score_chaat_masala(chaat_masala_pct))
    
    return sum(scores) / len(scores) if scores else 0

def calculate_online_activity_score(percentages: List[Optional[float]]) -> int:
    valid = [p for p in percentages if p is not None]
    if not valid: return 0
    avg = sum(valid) / len(valid)
    
    if avg >= 98: return 10
    if avg >= 97: return 8
    if avg >= 96: return 6
    if avg >= 95: return 4
    return 0

def calculate_kitchen_prep_score(times: List[Optional[float]]) -> int:
    valid = [t for t in times if t is not None]
    if not valid: return 0
    avg = sum(valid) / len(valid)
    
    if avg < 10: return 12
    if avg <= 15: return 10
    if avg <= 16: return 9
    if avg <= 17: return 8
    if avg <= 18: return 7
    if avg <= 19: return 6
    if avg <= 20: return 5
    return 0

def calculate_bad_delay_score(bad_pcts: List[Optional[float]], delay_pcts: List[Optional[float]]) -> int:
    bad_score = 0
    valid_bad = [p for p in bad_pcts if p is not None]
    if valid_bad:
        avg_bad = sum(valid_bad) / len(valid_bad)
        if avg_bad <= 3: bad_score = 5
        elif avg_bad <= 5: bad_score = 4
        elif avg_bad <= 7: bad_score = 3
        elif avg_bad <= 9: bad_score = 2
        elif avg_bad <= 11: bad_score = 1
        else: bad_score = 0
        
    delay_score = 0
    valid_delay = [p for p in delay_pcts if p is not None]
    if valid_delay:
        avg_delay = sum(valid_delay) / len(valid_delay)
        if avg_delay <= 10: delay_score = 5
        elif avg_delay <= 12: delay_score = 4
        elif avg_delay <= 14: delay_score = 3
        elif avg_delay <= 16: delay_score = 2
        elif avg_delay <= 18: delay_score = 1
        else: delay_score = 0
        
    return bad_score + delay_score

def calculate_outlet_audit_score(mistakes_a: Optional[int], mistakes_c: Optional[int], mistakes_cm: Optional[int]) -> float:
    def score_mistakes(m):
        raw = 20 - (2 * m)
        return max(0, min(20, raw))
        
    scores = []
    if mistakes_a is not None: scores.append(score_mistakes(mistakes_a))
    if mistakes_c is not None: scores.append(score_mistakes(mistakes_c))
    if mistakes_cm is not None: scores.append(score_mistakes(mistakes_cm))
    
    return sum(scores) / len(scores) if scores else 0

def calculate_negative_review_score(neg_a: Optional[int], neg_c: Optional[int], neg_cm: Optional[int]) -> float:
    """Each negative review deducts 0.25 points. Total deduction = sum of (input * -0.25) per restaurant."""
    total = 0.0
    if neg_a is not None: total += neg_a * (-0.25)
    if neg_c is not None: total += neg_c * (-0.25)
    if neg_cm is not None: total += neg_cm * (-0.25)
    return total

def calculate_add_on_sale_score(ts_a: Optional[float], aos_a: Optional[float], ts_c: Optional[float], aos_c: Optional[float], ts_cm: Optional[float], aos_cm: Optional[float]) -> float:
    def score_aos(ts, aos):
        if ts <= 0: return 0
        pct = (aos / ts) * 100
        if pct >= 16: return 12
        if pct >= 15: return 10
        if pct >= 14: return 8
        if pct >= 13: return 6
        if pct >= 12: return 4
        if pct >= 11: return 2
        return 0

    scores = []
    # Only score if we have both total sales and add-on sales for the restaurant
    if ts_a is not None and aos_a is not None: scores.append(score_aos(ts_a, aos_a))
    if ts_c is not None and aos_c is not None: scores.append(score_aos(ts_c, aos_c))
    if ts_cm is not None and aos_cm is not None: scores.append(score_aos(ts_cm, aos_cm))
    
    return sum(scores) / len(scores) if scores else 0
