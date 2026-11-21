"""
Keltner Channels Indicator
Constructed using an exponential moving average (EMA) centerline and average true range (ATR) bands.
"""
from typing import List, Dict, Any

class KeltnerChannels:
    @staticmethod
    def calculate(highs: List[float], lows: List[float], closes: List[float], ema_period: int = 20, atr_period: int = 10, multiplier: float = 2.0) -> Dict[str, List[float]]:
        n = len(closes)
        if n < max(ema_period, atr_period):
            raise ValueError("Insufficient data points for Keltner Channels")

        # Compute EMA of close
        ema = [0.0] * n
        k = 2.0 / (ema_period + 1)
        ema[ema_period - 1] = sum(closes[:ema_period]) / ema_period
        for i in range(ema_period, n):
            ema[i] = closes[i] * k + ema[i - 1] * (1 - k)

        # Compute True Range
        tr = [0.0] * n
        tr[0] = highs[0] - lows[0]
        for i in range(1, n):
            tr[i] = max(highs[i] - lows[i], abs(highs[i] - closes[i - 1]), abs(lows[i] - closes[i - 1]))

        # Compute ATR via SMA of TR
        atr = [0.0] * n
        for i in range(atr_period - 1, n):
            atr[i] = sum(tr[i - atr_period + 1:i + 1]) / atr_period

        upper = [0.0] * n
        lower = [0.0] * n
        start_idx = max(ema_period, atr_period) - 1
        for i in range(start_idx, n):
            upper[i] = round(ema[i] + multiplier * atr[i], 4)
            lower[i] = round(ema[i] - multiplier * atr[i], 4)
            ema[i] = round(ema[i], 4)

        return {
            "middle": ema[start_idx:],
            "upper": upper[start_idx:],
            "lower": lower[start_idx:]
        }
