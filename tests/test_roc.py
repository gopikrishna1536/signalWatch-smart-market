import unittest
from signalwatch.rate_of_change import RateOfChange

class TestRateOfChange(unittest.TestCase):
    def test_roc_calculation(self):
        closes = [100.0, 102.0, 105.0, 110.0, 115.0]
        res = RateOfChange.calculate(closes, period=2)
        # Period 2:
        # idx 2: (105-100)/100 = 5.0%
        # idx 3: (110-102)/102 = 7.84%
        # idx 4: (115-105)/105 = 9.52%
        self.assertEqual(res, [5.0, 7.84, 9.52])

if __name__ == "__main__":
    unittest.main()
