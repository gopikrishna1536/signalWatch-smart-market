import unittest
from signalwatch.money_flow_index import MoneyFlowIndex

class TestMoneyFlowIndex(unittest.TestCase):
    def test_mfi_uptrend(self):
        highs = [10.0 + i for i in range(20)]
        lows = [9.0 + i for i in range(20)]
        closes = [9.5 + i for i in range(20)]
        volumes = [1000.0 for _ in range(20)]

        mfi = MoneyFlowIndex.calculate(highs, lows, closes, volumes, period=14)
        self.assertEqual(len(mfi), 6)
        # Consistent uptrend should yield MFI of 100.0
        self.assertEqual(mfi[-1], 100.0)

if __name__ == "__main__":
    unittest.main()
