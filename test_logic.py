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
        self.assertEqual(calculate_google_rating_score(3.9, None, 3.9), 9)  # Avg 3.9
        self.assertEqual(calculate_google_rating_score(None, None, 3.85), 8) # Avg 3.85
        self.assertEqual(calculate_google_rating_score(None, None, None), 0)
        
    def test_food_cost(self):
        self.assertEqual(calculate_food_cost_score(22, 18, 24), 10)
        self.assertEqual(calculate_food_cost_score(25, 20, 25), 8)
        self.assertEqual(calculate_food_cost_score(27, 22, 29), 5)
        self.assertEqual(calculate_food_cost_score(28, 23, 30), 0)
        self.assertEqual(calculate_food_cost_score(22, None, None), 10)
        self.assertEqual(calculate_food_cost_score(None, 20, 26), 8) # (8+8)/2

    def test_online_activity(self):
        self.assertEqual(calculate_online_activity_score([98]*6), 10)
        self.assertEqual(calculate_online_activity_score([97, None, 97, None, None, None]), 8)
        self.assertEqual(calculate_online_activity_score([95, None]), 4)
        self.assertEqual(calculate_online_activity_score([None]*6), 0)

    def test_kitchen_prep(self):
        self.assertEqual(calculate_kitchen_prep_score([9]*6), 12)
        self.assertEqual(calculate_kitchen_prep_score([10, None, 10]), 10)
        self.assertEqual(calculate_kitchen_prep_score([None]), 0)
        self.assertEqual(calculate_kitchen_prep_score([16, 16, None]), 9)

    def test_bad_delay(self):
        self.assertEqual(calculate_bad_delay_score([3, 3, 3], [10, 10, 10]), 10)
        self.assertEqual(calculate_bad_delay_score([7, None, None], [None, 14, None]), 6) # 3 + 3
        self.assertEqual(calculate_bad_delay_score([None]*3, [10]*3), 5)
        self.assertEqual(calculate_bad_delay_score([3]*3, [None]*3), 5)

    def test_outlet_audit(self):
        self.assertEqual(calculate_outlet_audit_score(0, 0, 0), 20)
        self.assertEqual(calculate_outlet_audit_score(10, None, None), 0)
        self.assertEqual(calculate_outlet_audit_score(5, 5, None), 10)
        self.assertEqual(calculate_outlet_audit_score(None, 10, 5), 5) # (0 + 10)/2

    def test_add_on_sale(self):
        self.assertEqual(calculate_add_on_sale_score(100, 16, 100, 16, 100, 16), 12)
        self.assertEqual(calculate_add_on_sale_score(100, 16, None, None, None, None), 12)
        self.assertAlmostEqual(calculate_add_on_sale_score(100, 16, 100, 10, None, None), 6.0) # (12 + 0)/2

if __name__ == '__main__':
    unittest.main()
