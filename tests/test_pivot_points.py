import unittest
from signalwatch.pivot_points import PivotPoints

class TestPivotPoints(unittest.TestCase):
    def test_standard_pivots(self):
        res = PivotPoints.calculate_standard(110.0, 90.0, 100.0)
        self.assertEqual(res["pivot_point"], 100.0)
        self.assertEqual(res["resistance_1"], 110.0)
        self.assertEqual(res["support_1"], 90.0)
        self.assertEqual(res["resistance_2"], 120.0)
        self.assertEqual(res["support_2"], 80.0)

if __name__ == "__main__":
    unittest.main()
