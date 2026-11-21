import unittest
from signalwatch.calmar_ratio import CalmarRatio

class TestCalmarRatio(unittest.TestCase):
    def test_calmar_evaluation(self):
        res = CalmarRatio.calculate(25.0, 8.0)
        self.assertEqual(res["calmar_ratio"], 3.12)
        self.assertEqual(res["performance_tier"], "Excellent")

if __name__ == "__main__":
    unittest.main()
