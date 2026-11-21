import unittest
from signalwatch.slippage_model import SlippageModel

class TestSlippageModel(unittest.TestCase):
    def test_slippage_scaling(self):
        small_trade = SlippageModel.estimate_slippage(10000, 10000000)
        large_trade = SlippageModel.estimate_slippage(1000000, 10000000)
        self.assertGreater(large_trade["estimated_impact_bps"], small_trade["estimated_impact_bps"])

if __name__ == "__main__":
    unittest.main()
