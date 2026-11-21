"""
Parabolic Stop and Reverse (SAR)
Trend-following indicator setting trailing price stop levels based on acceleration factor.
"""
from typing import List

class ParabolicSAR:
    @staticmethod
    def calculate(highs: List[float], lows: List[float], af_step: float = 0.02, af_max: float = 0.2) -> List[float]:
        n = len(highs)
        if n < 3:
            raise ValueError("Insufficient data points for Parabolic SAR")

        sar = [0.0] * n
        is_bullish = True
        ep = highs[0] # Extreme point
        af = af_step
        sar[0] = lows[0]

        for i in range(1, n):
            prev_sar = sar[i - 1]
            if is_bullish:
                curr_sar = prev_sar + af * (ep - prev_sar)
                curr_sar = min(curr_sar, lows[i - 1], lows[max(0, i - 2)])

                if lows[i] < curr_sar:
                    is_bullish = False
                    sar[i] = ep
                    ep = lows[i]
                    af = af_step
                else:
                    sar[i] = curr_sar
                    if highs[i] > ep:
                        ep = highs[i]
                        af = min(af + af_step, af_max)
            else:
                curr_sar = prev_sar - af * (prev_sar - ep)
                curr_sar = max(curr_sar, highs[i - 1], highs[max(0, i - 2)])

                if highs[i] > curr_sar:
                    is_bullish = True
                    sar[i] = ep
                    ep = highs[i]
                    af = af_step
                else:
                    sar[i] = curr_sar
                    if lows[i] < ep:
                        ep = lows[i]
                        af = min(af + af_step, af_max)

        return [round(s, 4) for s in sar]
