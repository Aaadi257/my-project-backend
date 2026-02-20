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
        self.assertEqual(calculate_google_rating_score(4.0, 4.0, 4.0), 10) # Avg 4.0
        self.assertEqual(calculate_google_rating_score(3.9, 3.9, 3.9), 9)  # Avg 3.9
        self.assertEqual(calculate_google_rating_score(3.85, 3.85, 3.85), 8) # Avg 3.85
        self.assertEqual(calculate_google_rating_score(3.0, 3.0, 3.0), 0)
        
    def test_food_cost(self):
        # Amritsari: 22(10), 23(9), 24(8), 25(7), 26(6), 27(5), >27(0)
        # Chennai:   18(10), 19(9), 20(8), 21(7), 22(5), >22(0)
        # CM:        24(10), 25(9), 26(8), 27(7), 28(6), 29(5), >=30(0)

        # Best case: A=10 + C=10 + CM=10 = 30
        self.assertEqual(calculate_food_cost_score(22, 18, 24), 30)
        # Middle case: A=7 + C=8 + CM=9 = 24
        self.assertEqual(calculate_food_cost_score(25, 20, 25), 24)
        # Edge case: A=5 + C=5 + CM=5 = 15
        self.assertEqual(calculate_food_cost_score(27, 22, 29), 15)
        # CM at 30 = 0 points
        self.assertEqual(calculate_food_cost_score(28, 23, 30), 0)

    def test_online_activity(self):
        # Avg of 6
        # 98(10), 97(8), 96(6), 95(4), <95(0)
        self.assertEqual(calculate_online_activity_score([98]*6), 10)
        self.assertEqual(calculate_online_activity_score([97]*6), 8)
        self.assertEqual(calculate_online_activity_score([95]*6), 4)
        self.assertEqual(calculate_online_activity_score([94.9]*6), 0)

    def test_kitchen_prep(self):
        # <10(12), 10-15(10), 16(9), 17(8), 18(7), 19(6), 20(5), >20(0)
        self.assertEqual(calculate_kitchen_prep_score([9]*6), 12)
        self.assertEqual(calculate_kitchen_prep_score([10]*6), 10)
        self.assertEqual(calculate_kitchen_prep_score([15]*6), 10)
        self.assertEqual(calculate_kitchen_prep_score([16]*6), 9)
        self.assertEqual(calculate_kitchen_prep_score([20]*6), 5)
        self.assertEqual(calculate_kitchen_prep_score([21]*6), 0)

    def test_bad_delay(self):
        # Bad: 3(5), 5(4), 7(3), 9(2), 11(1), >11(0) (Avg of 3)
        # Delay: 10(5), 12(4), 14(3), 16(2), 18(1), >18(0) (Avg of 3)
        
        # Best case: 5 + 5 = 10
        self.assertEqual(calculate_bad_delay_score([3]*3, [10]*3), 10)
        # Mid: 3 + 3 = 6
        self.assertEqual(calculate_bad_delay_score([7]*3, [14]*3), 6)
        # Worst: 0 + 0 = 0
        self.assertEqual(calculate_bad_delay_score([12]*3, [19]*3), 0)

    def test_outlet_audit(self):
        # 0 mistakes -> 20. 10 mistakes -> 0.
        # Avg of 3 scores.
        self.assertEqual(calculate_outlet_audit_score(0, 0, 0), 20)
        self.assertEqual(calculate_outlet_audit_score(10, 10, 10), 0)
        self.assertEqual(calculate_outlet_audit_score(5, 5, 5), 10)
        # 0, 10, 5 -> (20 + 0 + 10)/3 = 30/3 = 10
        self.assertEqual(calculate_outlet_audit_score(0, 10, 5), 10)

    def test_add_on_sale(self):
        # Rate = AOS/TS * 100
        # >=16(12), 15(10), 14(8), 13(6), 12(4), 11(2), <=10(0)
        # Avg of 3.
        
        # Case 1: All 16% (16/100) -> 12 pts
        self.assertEqual(calculate_add_on_sale_score(100, 16, 100, 16, 100, 16), 12)
        # Case 2: Mixed. A=16%(12), C=10%(0), CM=15%(10). Avg=(12+0+10)/3 = 22/3 = 7.333
        self.assertAlmostEqual(calculate_add_on_sale_score(100, 16, 100, 10, 100, 15), 22/3)

if __name__ == '__main__':
    unittest.main()
