"""
Chaikin Oscillator
Measures momentum of the Accumulation/Distribution line using 3-day and 10-day EMAs.
"""
from typing import List

class ChaikinOscillator:
    @staticmethod
    def calculate(highs: List[float], lows: List[float], closes: List[float], volumes: List[float]) -> List[float]:
        n = len(closes)
        if n < 10:
            raise ValueError("Insufficient data points for Chaikin Oscillator")

        # Money Flow Multiplier & Volume
        adl = [0.0] * n
        running_ad = 0.0
        for i in range(n):
            h, l, c, v = highs[i], lows[i], closes[i], volumes[i]
            hl_range = h - l
            mfm = ((c - l) - (h - c)) / hl_range if hl_range > 0 else 0.0
            running_ad += mfm * v
            adl[i] = running_ad

        # 3-day and 10-day EMA of ADL
        ema3 = [0.0] * n
        ema10 = [0.0] * n
        k3 = 2.0 / (3 + 1)
        k10 = 2.0 / (10 + 1)

        ema3[2] = sum(adl[:3]) / 3
        for i in range(3, n):
            ema3[i] = adl[i] * k3 + ema3[i - 1] * (1 - k3)

        ema10[9] = sum(adl[:10]) / 10
        for i in range(10, n):
            ema10[i] = adl[i] * k10 + ema10[i - 1] * (1 - k10)

        chaikin = []
        for i in range(9, n):
            chaikin.append(round(ema3[i] - ema10[i], 2))

        return chaikin
