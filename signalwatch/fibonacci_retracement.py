"""
Fibonacci Retracement & Extension Generator
Computes critical support/resistance ratios (23.6%, 38.2%, 50%, 61.8%, 78.6%, 161.8%).
"""
from typing import Dict, Any

class FibonacciRetracement:
    @staticmethod
    def calculate_levels(swing_high: float, swing_low: float, is_uptrend: bool = True) -> Dict[str, float]:
        if swing_high <= swing_low:
            raise ValueError("Swing high must be strictly greater than swing low")

        diff = swing_high - swing_low
        if is_uptrend:
            return {
                "level_0.0": round(swing_high, 4),
                "level_23.6": round(swing_high - 0.236 * diff, 4),
                "level_38.2": round(swing_high - 0.382 * diff, 4),
                "level_50.0": round(swing_high - 0.500 * diff, 4),
                "level_61.8": round(swing_high - 0.618 * diff, 4),
                "level_78.6": round(swing_high - 0.786 * diff, 4),
                "level_100.0": round(swing_low, 4),
                "extension_161.8": round(swing_high + 0.618 * diff, 4)
            }
        else:
            return {
                "level_0.0": round(swing_low, 4),
                "level_23.6": round(swing_low + 0.236 * diff, 4),
                "level_38.2": round(swing_low + 0.382 * diff, 4),
                "level_50.0": round(swing_low + 0.500 * diff, 4),
                "level_61.8": round(swing_low + 0.618 * diff, 4),
                "level_78.6": round(swing_low + 0.786 * diff, 4),
                "level_100.0": round(swing_high, 4),
                "extension_161.8": round(swing_low - 0.618 * diff, 4)
            }
