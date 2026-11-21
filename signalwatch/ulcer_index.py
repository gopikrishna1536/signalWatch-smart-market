"""
Ulcer Index (UI) & Martin Ratio
Downside volatility metric that only penalizes drawdowns from historical peak, unlike standard deviation.
"""
import math
from typing import List, Dict, Any

class UlcerIndex:
    @staticmethod
    def calculate(closes: List[float], period: int = 14) -> List[float]:
        n = len(closes)
        if n < period:
            raise ValueError("Insufficient data points for Ulcer Index")

        ui_values = []
        for i in range(period - 1, n):
            window = closes[i - period + 1:i + 1]
            max_seen = window[0]
            drawdowns_sq = []
            for p in window:
                if p > max_seen:
                    max_seen = p
                pct_dd = ((p - max_seen) / max_seen * 100.0) if max_seen > 0 else 0.0
                drawdowns_sq.append(pct_dd ** 2)

            ui = math.sqrt(sum(drawdowns_sq) / period)
            ui_values.append(round(ui, 3))

        return ui_values
