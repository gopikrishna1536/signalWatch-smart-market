"""
Stochastic Oscillator (%K and %D)
Measures the position of the close relative to the high-low range over a given period.
"""
from typing import List, Dict, Any

class StochasticOscillator:
    @staticmethod
    def calculate(highs: List[float], lows: List[float], closes: List[float], k_period: int = 14, d_period: int = 3) -> Dict[str, List[float]]:
        n = len(closes)
        if n < k_period + d_period - 1:
            raise ValueError("Insufficient data points for Stochastic Oscillator")

        raw_k = []
        for i in range(k_period - 1, n):
            highest_high = max(highs[i - k_period + 1:i + 1])
            lowest_low = min(lows[i - k_period + 1:i + 1])
            denom = highest_high - lowest_low
            k_val = ((closes[i] - lowest_low) / denom * 100.0) if denom > 0 else 50.0
            raw_k.append(k_val)

        d_vals = []
        for i in range(d_period - 1, len(raw_k)):
            d_avg = sum(raw_k[i - d_period + 1:i + 1]) / d_period
            d_vals.append(round(d_avg, 2))

        formatted_k = [round(k, 2) for k in raw_k[d_period - 1:]]
        return {
            "percent_k": formatted_k,
            "percent_d": d_vals
        }
