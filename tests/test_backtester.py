import unittest
from signalwatch.backtester import StrategyBacktester

class TestStrategyBacktester(unittest.TestCase):
    def test_profitable_trade_execution(self):
        backtester = StrategyBacktester(initial_capital=10000.0, commission_rate=0.0)
        prices = [100.0, 105.0, 110.0, 120.0, 115.0]
        signals = ["BUY", "HOLD", "HOLD", "SELL", "HOLD"]

        report = backtester.run_backtest(prices, signals)
        self.assertEqual(report["total_trades"], 1)
        self.assertEqual(report["winning_trades"], 1)
        self.assertEqual(report["win_rate_pct"], 100.0)
        self.assertEqual(report["final_equity"], 12000.0)
        self.assertEqual(report["total_return_pct"], 20.0)
        self.assertEqual(report["max_drawdown_pct"], 0.0)

    def test_losing_trade_execution_and_drawdown(self):
        backtester = StrategyBacktester(initial_capital=10000.0, commission_rate=0.0)
        prices = [100.0, 90.0, 80.0, 70.0]
        signals = ["BUY", "HOLD", "HOLD", "SELL"]

        report = backtester.run_backtest(prices, signals)
        self.assertEqual(report["total_trades"], 1)
        self.assertEqual(report["losing_trades"], 1)
        self.assertEqual(report["win_rate_pct"], 0.0)
        self.assertEqual(report["final_equity"], 7000.0)
        self.assertEqual(report["total_return_pct"], -30.0)
        self.assertEqual(report["max_drawdown_pct"], 30.0)

    def test_no_signals_preserves_capital(self):
        backtester = StrategyBacktester(initial_capital=5000.0)
        prices = [10.0, 12.0, 15.0]
        signals = [None, None, None]

        report = backtester.run_backtest(prices, signals)
        self.assertEqual(report["total_trades"], 0)
        self.assertEqual(report["final_equity"], 5000.0)
        self.assertEqual(report["total_return_pct"], 0.0)

    def test_mismatched_lengths_raises_error(self):
        backtester = StrategyBacktester()
        with self.assertRaises(ValueError):
            backtester.run_backtest([100.0, 105.0], ["BUY"])

if __name__ == "__main__":
    unittest.main()
