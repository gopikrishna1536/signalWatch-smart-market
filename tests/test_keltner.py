import unittest
from signalwatch.keltner_channels import KeltnerChannels

class TestKeltnerChannels(unittest.TestCase):
    def test_keltner_calculation(self):
        highs = [10.0 + i * 0.5 for i in range(25)]
        lows = [9.0 + i * 0.5 for i in range(25)]
        closes = [9.5 + i * 0.5 for i in range(25)]

        res = KeltnerChannels.calculate(highs, lows, closes, ema_period=10, atr_period=5, multiplier=2.0)
        self.assertGreater(len(res["middle"]), 0)
        for u, m, l in zip(res["upper"], res["middle"], res["lower"]):
            self.assertGreater(u, m)
            self.assertGreater(m, l)

if __name__ == "__main__":
    unittest.main()
