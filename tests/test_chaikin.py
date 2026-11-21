import unittest
from signalwatch.chaikin_oscillator import ChaikinOscillator

class TestChaikinOscillator(unittest.TestCase):
    def test_chaikin(self):
        highs = [10.0 + i * 0.2 for i in range(15)]
        lows = [9.0 + i * 0.2 for i in range(15)]
        closes = [9.8 + i * 0.2 for i in range(15)]
        volumes = [1000.0 for _ in range(15)]

        res = ChaikinOscillator.calculate(highs, lows, closes, volumes)
        self.assertEqual(len(res), 6)

if __name__ == "__main__":
    unittest.main()
