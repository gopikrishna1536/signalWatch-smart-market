import unittest
from signalwatch.fibonacci_retracement import FibonacciRetracement

class TestFibonacciRetracement(unittest.TestCase):
    def test_uptrend_levels(self):
        res = FibonacciRetracement.calculate_levels(200.0, 100.0, is_uptrend=True)
        self.assertEqual(res["level_0.0"], 200.0)
        self.assertEqual(res["level_50.0"], 150.0)
        self.assertEqual(res["level_61.8"], 138.2)
        self.assertEqual(res["level_100.0"], 100.0)
        self.assertEqual(res["extension_161.8"], 261.8)

if __name__ == "__main__":
    unittest.main()
