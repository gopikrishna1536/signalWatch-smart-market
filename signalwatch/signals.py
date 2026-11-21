"""
Signal Detection Engine for SignalWatch.
Evaluates technical indicators to generate quantitative trading signals.
"""
from typing import List, Dict, Any, Optional
from .indicators import TechnicalIndicators

class MarketSignalEngine:
    @staticmethod
    def detect_ma_crossover(prices: List[float], fast_window: int = 5, slow_window: int = 20) -> List[Dict[str, Any]]:
        """
        Detects Golden Cross (Fast MA crosses above Slow MA) and
        Death Cross (Fast MA crosses below Slow MA).
        """
        if fast_window >= slow_window:
            raise ValueError("Fast window must be strictly less than slow window.")

        fast_sma = TechnicalIndicators.simple_moving_average(prices, fast_window)
        slow_sma = TechnicalIndicators.simple_moving_average(prices, slow_window)

        signals = []
        for i in range(1, len(prices)):
            f_prev, f_curr = fast_sma[i - 1], fast_sma[i]
            s_prev, s_curr = slow_sma[i - 1], slow_sma[i]

            if None in (f_prev, f_curr, s_prev, s_curr):
                continue

            # Bullish Golden Cross
            if f_prev <= s_prev and f_curr > s_curr:
                signals.append({
                    "index": i,
                    "price": prices[i],
                    "signal": "BULLISH_GOLDEN_CROSS",
                    "fast_sma": f_curr,
                    "slow_sma": s_curr,
                    "strength": "HIGH"
                })
            # Bearish Death Cross
            elif f_prev >= s_prev and f_curr < s_curr:
                signals.append({
                    "index": i,
                    "price": prices[i],
                    "signal": "BEARISH_DEATH_CROSS",
                    "fast_sma": f_curr,
                    "slow_sma": s_curr,
                    "strength": "HIGH"
                })

        return signals

    @staticmethod
    def evaluate_rsi_conditions(prices: List[float], period: int = 14) -> Dict[str, Any]:
        """
        Evaluates current RSI state for overbought (>70) and oversold (<30) market conditions.
        """
        rsi_series = TechnicalIndicators.relative_strength_index(prices, period)
        if not rsi_series or rsi_series[-1] is None:
            return {"status": "INSUFFICIENT_DATA", "current_rsi": None}

        current_rsi = rsi_series[-1]

        if current_rsi >= 70.0:
            status = "OVERBOUGHT"
            recommendation = "SELL_OR_TAKE_PROFIT"
        elif current_rsi <= 30.0:
            status = "OVERSOLD"
            recommendation = "BUY_OPPORTUNITY"
        else:
            status = "NEUTRAL"
            recommendation = "HOLD"

        return {
            "status": status,
            "current_rsi": current_rsi,
            "recommendation": recommendation,
            "sample_size": len(prices)
        }
