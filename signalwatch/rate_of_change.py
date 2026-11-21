"""
Price Rate of Change (ROC)
Momentum oscillator measuring percentage change between current price and n periods ago.
"""
from typing import List

class RateOfChange:
    @staticmethod
    def calculate(closes: List[float], period: int = 12) -> List[float]:
        n = len(closes)
        if n <= period:
            raise ValueError(f"Insufficient data points: requires > {period}")

        roc_values = []
        for i in range(period, n):
            prev = closes[i - period]
            if prev == 0:
                roc_values.append(0.0)
            else:
                pct = ((closes[i] - prev) / prev) * 100.0
                roc_values.append(round(pct, 2))

        return roc_values
