import unittest
from signalwatch.parabolic_sar import ParabolicSAR

class TestParabolicSAR(unittest.TestCase):
    def test_sar_uptrend(self):
        highs = [10.0, 11.0, 12.0, 13.5, 15.0, 16.0]
        lows = [9.0, 9.8, 10.5, 11.8, 13.0, 14.5]
        sar = ParabolicSAR.calculate(highs, lows)
        self.assertEqual(len(sar), 6)
        # In consistent uptrend, SAR trails below lows
        for i in range(1, 6):
            self.assertLessEqual(sar[i], highs[i])

if __name__ == "__main__":
    unittest.main()
