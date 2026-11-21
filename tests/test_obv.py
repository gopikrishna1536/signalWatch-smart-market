import unittest
from signalwatch.obv_indicator import OnBalanceVolume

class TestOnBalanceVolume(unittest.TestCase):
    def test_obv_accumulation(self):
        closes = [10.0, 11.0, 10.5, 12.0]
        vols = [100.0, 200.0, 50.0, 300.0]
        # Day 0: 100
        # Day 1: up -> 100 + 200 = 300
        # Day 2: down -> 300 - 50 = 250
        # Day 3: up -> 250 + 300 = 550
        res = OnBalanceVolume.calculate(closes, vols)
        self.assertEqual(res, [100.0, 300.0, 250.0, 550.0])

if __name__ == "__main__":
    unittest.main()
