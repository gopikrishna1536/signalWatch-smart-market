"""
Money Flow Index (MFI)
Volume-weighted momentum oscillator measuring buying and selling pressure.
"""
from typing import List

class MoneyFlowIndex:
    @staticmethod
    def calculate(highs: List[float], lows: List[float], closes: List[float], volumes: List[float], period: int = 14) -> List[float]:
        n = len(closes)
        if n <= period:
            raise ValueError("Insufficient data points for MFI")

        typical_prices = [(h + l + c) / 3.0 for h, l, c in zip(highs, lows, closes)]
        raw_money_flows = [tp * v for tp, v in zip(typical_prices, volumes)]

        mfi_values = []
        for i in range(period, n):
            pos_flow = 0.0
            neg_flow = 0.0
            for j in range(i - period + 1, i + 1):
                if typical_prices[j] > typical_prices[j - 1]:
                    pos_flow += raw_money_flows[j]
                elif typical_prices[j] < typical_prices[j - 1]:
                    neg_flow += raw_money_flows[j]

            if neg_flow == 0:
                mfi = 100.0
            else:
                money_ratio = pos_flow / neg_flow
                mfi = 100.0 - (100.0 / (1.0 + money_ratio))
            mfi_values.append(round(mfi, 2))

        return mfi_values
