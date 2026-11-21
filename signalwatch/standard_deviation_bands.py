"""
Rolling Standard Deviation Volatility Bands
Computes running dispersion around moving average to gauge regime shifts.
"""
import math
from typing import List, Dict, Any

class StandardDeviationBands:
    @staticmethod
    def calculate(closes: List[float], period: int = 20) -> List[float]:
        n = len(closes)
        if n < period:
            raise ValueError("Insufficient data points for standard deviation")

        stdevs = []
        for i in range(period - 1, n):
            window = closes[i - period + 1:i + 1]
            mean = sum(window) / period
            variance = sum((x - mean) ** 2 for x in window) / period
            stdevs.append(round(math.sqrt(variance), 4))

        return stdevs
