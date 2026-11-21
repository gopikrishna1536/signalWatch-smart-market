"""
TRIX Oscillator
Triple exponentially smoothed moving average percentage rate-of-change filter.
"""
from typing import List

class TRIXIndicator:
    @staticmethod
    def _ema(series: List[float], period: int) -> List[float]:
        n = len(series)
        ema = [0.0] * n
        k = 2.0 / (period + 1)
        ema[period - 1] = sum(series[:period]) / period
        for i in range(period, n):
            ema[i] = series[i] * k + ema[i - 1] * (1 - k)
        return ema

    @classmethod
    def calculate(cls, closes: List[float], period: int = 15) -> List[float]:
        n = len(closes)
        if n < period * 3:
            raise ValueError(f"Requires at least {period * 3} candles for TRIX")

        e1 = cls._ema(closes, period)
        e2 = cls._ema(e1, period)
        e3 = cls._ema(e2, period)

        start = period * 3 - 2
        trix = []
        for i in range(start, n):
            prev = e3[i - 1]
            val = ((e3[i] - prev) / prev * 10000.0) if prev != 0 else 0.0
            trix.append(round(val, 3))

        return trix
