import unittest
from signalwatch.ichimoku_cloud import IchimokuCloud

class TestIchimokuCloud(unittest.TestCase):
    def test_ichimoku(self):
        highs = [100.0 + i for i in range(60)]
        lows = [90.0 + i for i in range(60)]
        res = IchimokuCloud.calculate(highs, lows)
        self.assertGreater(res["tenkan_sen"], 0)
        self.assertGreater(res["kijun_sen"], 0)
        self.assertTrue(res["is_bullish_cloud"])
        self.assertEqual(res["tk_cross"], "BULLISH_CROSS")

if __name__ == "__main__":
    unittest.main()
