import unittest
from signalwatch.standard_deviation_bands import StandardDeviationBands

class TestStandardDeviationBands(unittest.TestCase):
    def test_constant_series(self):
        closes = [50.0] * 25
        res = StandardDeviationBands.calculate(closes, period=20)
        self.assertEqual(len(res), 6)
        self.assertTrue(all(s == 0.0 for s in res))

    def test_volatile_series(self):
        closes = [10.0 if i % 2 == 0 else 20.0 for i in range(25)]
        res = StandardDeviationBands.calculate(closes, period=20)
        self.assertGreater(res[-1], 4.0)

if __name__ == "__main__":
    unittest.main()
