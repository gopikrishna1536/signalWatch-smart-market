import unittest
from signalwatch.portfolio_rebalancer import PortfolioRebalancer

class TestPortfolioRebalancer(unittest.TestCase):
    def test_rebalancing(self):
        current = {"AAPL": 8000.0, "GOOGL": 2000.0}
        target = {"AAPL": 0.50, "GOOGL": 0.50}
        res = PortfolioRebalancer.generate_rebalance_orders(current, target, drift_threshold=0.05)
        self.assertTrue(res["rebalance_required"])
        self.assertEqual(len(res["orders"]), 2)
        sell_order = next(o for o in res["orders"] if o["asset"] == "AAPL")
        self.assertEqual(sell_order["action"], "SELL")
        self.assertEqual(sell_order["amount"], 3000.0)

if __name__ == "__main__":
    unittest.main()
