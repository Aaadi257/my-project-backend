import unittest
from logic import (
    calculate_google_rating_score,
    calculate_zomato_swiggy_score,
    calculate_food_cost_score,
    calculate_online_activity_score,
    calculate_kitchen_prep_score,
    calculate_bad_delay_score,
    calculate_outlet_audit_score,
    calculate_add_on_sale_score
)

class TestScoringLogic(unittest.TestCase):
    
    def test_google_rating(self):
        self.assertEqual(calculate_google_rating_score(4.0, 4.0), 10) # Avg 4.0
        self.assertEqual(calculate_google_rating_score(3.9, 3.9), 9)  # Avg 3.9
        self.assertEqual(calculate_google_rating_score(3.85, 3.85), 8) # Avg 3.85 -> 3.8 bucket? No, logic is >= 3.8
        # Logic: if avg >= 3.9 return 9. 3.85 !>= 3.9. 3.85 >= 3.8. So 8.
        self.assertEqual(calculate_google_rating_score(3.0, 3.0), 0)
        
    def test_food_cost(self):
        # Amritsari: 22(10), 23(9), 24(8), 25(7), 26(6), 27(5), >27(0)
        # Chennai: 18(10), 19(9), 20(8), 21(7), 22(5), >22(0)
        
        # Best case
        self.assertEqual(calculate_food_cost_score(22, 18), 10 + 10)
        # Middle case
        self.assertEqual(calculate_food_cost_score(25, 20), 7 + 8)
        # Edge case
        self.assertEqual(calculate_food_cost_score(27, 22), 5 + 5)
        # Fail case
        self.assertEqual(calculate_food_cost_score(28, 23), 0 + 0)

    def test_online_activity(self):
        # Avg of 4
        # 98(10), 97(8), 96(6), 95(4), <95(0)
        self.assertEqual(calculate_online_activity_score([98, 98, 98, 98]), 10)
        self.assertEqual(calculate_online_activity_score([97, 97, 97, 97]), 8)
        self.assertEqual(calculate_online_activity_score([95, 95, 95, 95]), 4)
        self.assertEqual(calculate_online_activity_score([94.9, 94.9, 94.9, 94.9]), 0)

    def test_kitchen_prep(self):
        # <10(12), 10-15(10), 16(9), 17(8), 18(7), 19(6), 20(5), >20(0)
        self.assertEqual(calculate_kitchen_prep_score([9, 9, 9, 9]), 12)
        self.assertEqual(calculate_kitchen_prep_score([10, 10, 10, 10]), 10)
        self.assertEqual(calculate_kitchen_prep_score([15, 15, 15, 15]), 10)
        self.assertEqual(calculate_kitchen_prep_score([16, 16, 16, 16]), 9)
        self.assertEqual(calculate_kitchen_prep_score([20, 20, 20, 20]), 5)
        self.assertEqual(calculate_kitchen_prep_score([21, 21, 21, 21]), 0)

    def test_bad_delay(self):
        # Bad: 3(5), 5(4), 7(3), 9(2), 11(1), >11(0)
        # Delay: 10(5), 12(4), 14(3), 16(2), 18(1), >18(0)
        
        # Best case
        self.assertEqual(calculate_bad_delay_score([3]*4, [10]*4), 5 + 5)
        # Mid
        self.assertEqual(calculate_bad_delay_score([7]*4, [14]*4), 3 + 3)
        # Worst
        self.assertEqual(calculate_bad_delay_score([12]*4, [19]*4), 0 + 0)

    def test_outlet_audit(self):
        # 0 mistakes -> 20. 10 mistakes -> 0.
        # Avg of 2 scores.
        self.assertEqual(calculate_outlet_audit_score(0, 0), 20)
        self.assertEqual(calculate_outlet_audit_score(10, 10), 0)
        self.assertEqual(calculate_outlet_audit_score(5, 5), (10+10)/2)
        self.assertEqual(calculate_outlet_audit_score(0, 10), (20+0)/2) # 10

    def test_add_on_sale(self):
        # Rate = AOS/TS * 100
        # >=16(12), 15(10), 14(8), 13(6), 12(4), 11(2), <=10(0)
        # Avg of 2.
        
        # Case 1: Both 16% (16/100)
        self.assertEqual(calculate_add_on_sale_score(100, 16, 100, 16), 12)
        # Case 2: 15% (15/100) -> 10 pts
        self.assertEqual(calculate_add_on_sale_score(100, 15, 100, 15), 10)
        # Case 3: Mixed. A=16%(12), C=10%(0). Avg=6.
        self.assertEqual(calculate_add_on_sale_score(100, 16, 100, 10), 6)

if __name__ == '__main__':
    unittest.main()
