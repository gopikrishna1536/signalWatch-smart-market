import unittest
from signalwatch.indicators import TechnicalIndicators

class TestOscillatorIndicators(unittest.TestCase):
    def setUp(self):
        self.highs = [10.0 + (i * 0.5) for i in range(25)]
        self.lows = [8.0 + (i * 0.5) for i in range(25)]
        self.closes = [9.5 + (i * 0.5) for i in range(25)]

    def test_commodity_channel_index_calculation(self):
        cci = TechnicalIndicators.commodity_channel_index(self.highs, self.lows, self.closes, period=20)
        self.assertEqual(len(cci), 25)
        # First 19 entries should be None
        self.assertIsNone(cci[0])
        self.assertIsNone(cci[18])
        # From index 19 onwards, CCI should be a valid float
        self.assertIsNotNone(cci[19])
        self.assertIsNotNone(cci[24])

    def test_williams_r_range_bounds(self):
        wr = TechnicalIndicators.williams_r(self.highs, self.lows, self.closes, period=14)
        self.assertEqual(len(wr), 25)
        self.assertIsNone(wr[0])
        self.assertIsNotNone(wr[13])

        for val in wr[13:]:
            self.assertGreaterEqual(val, -100.0)
            self.assertLessEqual(val, 0.0)

    def test_mismatched_length_exception(self):
        with self.assertRaises(ValueError):
            TechnicalIndicators.commodity_channel_index([10.0], [5.0, 6.0], [8.0])

if __name__ == "__main__":
    unittest.main()
