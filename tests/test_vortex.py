import unittest
from signalwatch.vortex_indicator import VortexIndicator

class TestVortexIndicator(unittest.TestCase):
    def test_vortex_calculation(self):
        highs = [10.0 + i for i in range(25)]
        lows = [8.0 + i for i in range(25)]
        closes = [9.5 + i for i in range(25)]

        res = VortexIndicator.calculate(highs, lows, closes, period=14)
        self.assertEqual(len(res["vi_plus"]), 11)
        # Consistent uptrend -> VI+ should exceed VI-
        self.assertGreater(res["vi_plus"][-1], res["vi_minus"][-1])

if __name__ == "__main__":
    unittest.main()
