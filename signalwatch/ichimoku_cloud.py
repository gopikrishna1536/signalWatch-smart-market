"""
Ichimoku Kinko Hyo (Ichimoku Cloud)
Calculates Tenkan-sen (Conversion Line), Kijun-sen (Base Line), and Senkou Span A & B.
"""
from typing import List, Dict, Any

class IchimokuCloud:
    @staticmethod
    def calculate(highs: List[float], lows: List[float], tenkan_period: int = 9, kijun_period: int = 26, senkou_b_period: int = 52) -> Dict[str, Any]:
        n = len(highs)
        if n < senkou_b_period:
            raise ValueError(f"Requires at least {senkou_b_period} candles for full Ichimoku")

        tenkan = (max(highs[-tenkan_period:]) + min(lows[-tenkan_period:])) / 2.0
        kijun = (max(highs[-kijun_period:]) + min(lows[-kijun_period:])) / 2.0
        senkou_a = (tenkan + kijun) / 2.0
        senkou_b = (max(highs[-senkou_b_period:]) + min(lows[-senkou_b_period:])) / 2.0

        is_bullish_cloud = senkou_a > senkou_b
        tk_cross = "BULLISH_CROSS" if tenkan > kijun else "BEARISH_CROSS"

        return {
            "tenkan_sen": round(tenkan, 4),
            "kijun_sen": round(kijun, 4),
            "senkou_span_a": round(senkou_a, 4),
            "senkou_span_b": round(senkou_b, 4),
            "is_bullish_cloud": is_bullish_cloud,
            "tk_cross": tk_cross
        }
