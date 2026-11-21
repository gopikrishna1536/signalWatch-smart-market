"""
Donchian Channels
Computes n-period highest high and lowest low bands for breakout trend following.
"""
from typing import List, Dict, Any

class DonchianChannels:
    @staticmethod
    def calculate(highs: List[float], lows: List[float], period: int = 20) -> Dict[str, List[float]]:
        n = len(highs)
        if n < period:
            raise ValueError("Insufficient data points for Donchian Channels")

        upper = []
        lower = []
        middle = []

        for i in range(period - 1, n):
            h_max = max(highs[i - period + 1:i + 1])
            l_min = min(lows[i - period + 1:i + 1])
            mid = (h_max + l_min) / 2.0
            upper.append(round(h_max, 4))
            lower.append(round(l_min, 4))
            middle.append(round(mid, 4))

        return {
            "upper": upper,
            "middle": middle,
            "lower": lower
        }
