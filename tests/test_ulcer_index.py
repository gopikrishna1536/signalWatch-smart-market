import unittest
from signalwatch.ulcer_index import UlcerIndex

class TestUlcerIndex(unittest.TestCase):
    def test_no_drawdown_ui_is_zero(self):
        closes = [10.0 + i for i in range(20)]
        res = UlcerIndex.calculate(closes, period=14)
        self.assertEqual(res[-1], 0.0)

    def test_severe_drawdown(self):
        closes = [100.0] * 10 + [50.0] * 5
        res = UlcerIndex.calculate(closes, period=10)
        self.assertGreater(res[-1], 20.0)

if __name__ == "__main__":
    unittest.main()
