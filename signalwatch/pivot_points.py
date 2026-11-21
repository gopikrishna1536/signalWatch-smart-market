"""
Pivot Points Calculator
Computes Standard floor pivot points and Fibonacci support/resistance levels.
"""
from typing import Dict, Any

class PivotPoints:
    @staticmethod
    def calculate_standard(high: float, low: float, close: float) -> Dict[str, float]:
        pp = (high + low + close) / 3.0
        r1 = (2.0 * pp) - low
        s1 = (2.0 * pp) - high
        r2 = pp + (high - low)
        s2 = pp - (high - low)
        r3 = high + 2.0 * (pp - low)
        s3 = low - 2.0 * (high - pp)

        return {
            "pivot_point": round(pp, 2),
            "resistance_1": round(r1, 2),
            "support_1": round(s1, 2),
            "resistance_2": round(r2, 2),
            "support_2": round(s2, 2),
            "resistance_3": round(r3, 2),
            "support_3": round(s3, 2)
        }

    @staticmethod
    def calculate_fibonacci(high: float, low: float, close: float) -> Dict[str, float]:
        pp = (high + low + close) / 3.0
        rng = high - low
        return {
            "pivot_point": round(pp, 2),
            "r1": round(pp + 0.382 * rng, 2),
            "r2": round(pp + 0.618 * rng, 2),
            "r3": round(pp + 1.000 * rng, 2),
            "s1": round(pp - 0.382 * rng, 2),
            "s2": round(pp - 0.618 * rng, 2),
            "s3": round(pp - 1.000 * rng, 2)
        }
