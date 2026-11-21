import unittest
from signalwatch.stochastic_oscillator import StochasticOscillator

class TestStochasticOscillator(unittest.TestCase):
    def test_stochastic_range(self):
        highs = [50.0, 52.0, 51.0, 53.0, 55.0, 54.0, 56.0, 58.0, 57.0, 59.0, 60.0, 62.0, 61.0, 63.0, 65.0, 64.0, 66.0]
        lows = [45.0, 46.0, 47.0, 48.0, 49.0, 50.0, 51.0, 52.0, 53.0, 54.0, 55.0, 56.0, 57.0, 58.0, 59.0, 60.0, 61.0]
        closes = [48.0, 50.0, 49.0, 52.0, 53.0, 52.0, 55.0, 56.0, 55.0, 58.0, 59.0, 60.0, 59.0, 62.0, 63.0, 62.0, 65.0]

        res = StochasticOscillator.calculate(highs, lows, closes, k_period=14, d_period=3)
        self.assertGreater(len(res["percent_k"]), 0)
        self.assertEqual(len(res["percent_k"]), len(res["percent_d"]))
        for k, d in zip(res["percent_k"], res["percent_d"]):
            self.assertTrue(0.0 <= k <= 100.0)
            self.assertTrue(0.0 <= d <= 100.0)

if __name__ == "__main__":
    unittest.main()
