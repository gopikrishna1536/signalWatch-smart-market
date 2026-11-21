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

    def test_macd_calculation(self):
        prices = [float(x) for x in range(1, 40)]
        res = TechnicalIndicators.macd(prices, fast=5, slow=10, signal=3)
        self.assertIn("macd_line", res)
        self.assertIn("signal_line", res)
        self.assertIn("histogram", res)
        valid_macd = [x for x in res["macd_line"] if x is not None]
        self.assertTrue(len(valid_macd) > 0)
        # Uptrend should have positive MACD line (Fast EMA > Slow EMA)
        self.assertGreater(valid_macd[-1], 0)

    def test_vwap_calculation(self):
        prices = [100.0, 105.0, 110.0]
        volumes = [10.0, 20.0, 30.0]
        # Cum PV: (100*10) + (105*20) + (110*30) = 1000 + 2100 + 3300 = 6400
        # Cum V: 10 + 20 + 30 = 60
        # VWAP = 6400 / 60 = 106.6667
        vwap_series = TechnicalIndicators.vwap(prices, volumes)
        self.assertEqual(len(vwap_series), 3)
        self.assertEqual(vwap_series[0], 100.0)
        self.assertAlmostEqual(vwap_series[-1], 106.6667, places=4)

    def test_vwap_length_mismatch(self):
        with self.assertRaises(ValueError):
            TechnicalIndicators.vwap([10.0, 20.0], [5.0])

    def test_average_true_range(self):
        highs = [48.70, 48.72, 48.90, 48.87, 48.82, 49.05, 49.20, 49.35, 49.92, 50.19, 50.12, 49.66, 50.46, 50.65, 50.96]
        lows = [47.79, 48.14, 48.39, 48.37, 48.24, 48.64, 48.94, 48.86, 49.50, 49.87, 49.20, 48.98, 49.70, 49.85, 50.40]
        closes = [48.16, 48.61, 48.75, 48.63, 48.74, 49.03, 49.07, 49.32, 49.91, 50.13, 49.53, 49.50, 50.23, 50.41, 50.81]

        atr = TechnicalIndicators.average_true_range(highs, lows, closes, period=14)
        self.assertEqual(len(atr), 15)
        self.assertIsNone(atr[0])
        self.assertIsNotNone(atr[13])
        self.assertIsNotNone(atr[14])
        self.assertGreater(atr[14], 0.0)

    def test_supertrend_calculation(self):
        highs = [10.0 + i for i in range(20)]
        lows = [8.0 + i for i in range(20)]
        closes = [9.5 + i for i in range(20)]

        st_res = TechnicalIndicators.supertrend(highs, lows, closes, period=5, multiplier=2.0)
        self.assertIn("supertrend", st_res)
        self.assertIn("direction", st_res)
        # In a steady uptrend, direction should be bullish (+1)
        self.assertEqual(st_res["direction"][-1], 1)


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
