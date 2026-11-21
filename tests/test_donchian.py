import unittest
from signalwatch.donchian_channels import DonchianChannels

class TestDonchianChannels(unittest.TestCase):
    def test_donchian_bands(self):
        highs = [10.0 + i for i in range(25)]
        lows = [8.0 + i for i in range(25)]
        res = DonchianChannels.calculate(highs, lows, period=10)
        self.assertEqual(len(res["upper"]), 16)
        for u, m, l in zip(res["upper"], res["middle"], res["lower"]):
            self.assertGreater(u, m)
            self.assertGreater(m, l)

if __name__ == "__main__":
    unittest.main()
