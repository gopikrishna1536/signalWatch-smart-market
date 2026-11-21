import unittest
from signalwatch.indicators import TechnicalIndicators
from signalwatch.signals import MarketSignalEngine

class TestTechnicalIndicators(unittest.TestCase):
    def setUp(self):
        self.prices = [10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0]

    def test_sma_calculation(self):
        sma = TechnicalIndicators.simple_moving_average(self.prices, window=3)
        self.assertIsNone(sma[0])
        self.assertIsNone(sma[1])
        # (10 + 11 + 12) / 3 = 11.0
        self.assertEqual(sma[2], 11.0)
        # (11 + 12 + 13) / 3 = 12.0
        self.assertEqual(sma[3], 12.0)
        # (14 + 15 + 16) / 3 = 15.0
        self.assertEqual(sma[6], 15.0)

    def test_ema_calculation(self):
        ema = TechnicalIndicators.exponential_moving_average(self.prices, window=3)
        self.assertIsNone(ema[0])
        self.assertIsNone(ema[1])
        self.assertEqual(ema[2], 11.0)
        # Next value should be weighted towards prices[3] = 13.0
        self.assertAlmostEqual(ema[3], 12.0, places=2)

    def test_rsi_bounds(self):
        uptrend = [float(x) for x in range(100, 130)]
        rsi = TechnicalIndicators.relative_strength_index(uptrend, period=14)
        valid_rsi = [x for x in rsi if x is not None]
        for val in valid_rsi:
            self.assertGreaterEqual(val, 0.0)
            self.assertLessEqual(val, 100.0)

        # Sustained uptrend should have high RSI
        self.assertGreater(valid_rsi[-1], 70.0)

    def test_bollinger_bands_ordering(self):
        prices = [100.0 + (i % 5) for i in range(25)]
        bands = TechnicalIndicators.bollinger_bands(prices, window=20)
        valid_bands = [b for b in bands if b is not None]
        self.assertTrue(len(valid_bands) > 0)

        for upper, middle, lower in valid_bands:
            self.assertGreater(upper, middle)
            self.assertGreater(middle, lower)


class TestMarketSignalEngine(unittest.TestCase):
    def test_golden_cross_detection(self):
        # Create a series where fast MA crosses above slow MA
        prices = [10.0] * 15 + [12.0, 15.0, 20.0, 25.0, 30.0]
        signals = MarketSignalEngine.detect_ma_crossover(prices, fast_window=3, slow_window=10)
        self.assertTrue(any(s["signal"] == "BULLISH_GOLDEN_CROSS" for s in signals))

    def test_rsi_overbought_condition(self):
        steep_uptrend = [100.0 + (i * 2.5) for i in range(20)]
        eval_result = MarketSignalEngine.evaluate_rsi_conditions(steep_uptrend, period=14)
        self.assertEqual(eval_result["status"], "OVERBOUGHT")
        self.assertEqual(eval_result["recommendation"], "SELL_OR_TAKE_PROFIT")


if __name__ == "__main__":
    unittest.main()
