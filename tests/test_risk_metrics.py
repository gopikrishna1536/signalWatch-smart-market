import unittest
from signalwatch.risk_metrics import RiskMetricsCalculator

class TestRiskMetricsCalculator(unittest.TestCase):
    def test_returns_calculation_from_prices(self):
        prices = [100.0, 110.0, 121.0]
        returns = RiskMetricsCalculator.calculate_returns_from_prices(prices)
        self.assertEqual(len(returns), 2)
        self.assertAlmostEqual(returns[0], 0.10, places=4)
        self.assertAlmostEqual(returns[1], 0.10, places=4)

    def test_volatility_and_downside_deviation(self):
        # Series with positive and negative swings
        returns = [0.01, -0.02, 0.03, -0.01, 0.02, -0.005]
        vol = RiskMetricsCalculator.volatility(returns, annualized=False)
        downside = RiskMetricsCalculator.downside_deviation(returns, annualized=False)

        self.assertGreater(vol, 0.0)
        self.assertGreater(downside, 0.0)
        # Total volatility must be greater than or equal to downside deviation
        self.assertGreaterEqual(vol, downside)

    def test_sharpe_and_sortino_ratio(self):
        # Steady uptrend returns
        returns = [0.002] * 252 # ~50% annualized return
        sharpe = RiskMetricsCalculator.sharpe_ratio(returns, risk_free_rate=0.04)
        sortino = RiskMetricsCalculator.sortino_ratio(returns, risk_free_rate=0.04)

        # In steady upward drift with no downside, Sortino should be high
        self.assertGreater(sortino, 0.0)

    def test_portfolio_risk_summary(self):
        prices = [100.0 + (i * 0.5) for i in range(50)]
        analysis = RiskMetricsCalculator.analyze_portfolio_risk(prices)

        self.assertEqual(analysis["periods_analyzed"], 49)
        self.assertIn("annualized_return_pct", analysis)
        self.assertIn("sharpe_ratio", analysis)
        self.assertIn("sortino_ratio", analysis)
        self.assertIn("risk_profile", analysis)

if __name__ == "__main__":
    unittest.main()
