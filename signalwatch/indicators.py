"""
Technical Analysis Indicators Engine for SignalWatch.
Implements mathematically rigorous financial indicators in pure Python.
"""
from typing import List, Optional, Tuple, Dict
import math

class TechnicalIndicators:
    @staticmethod
    def simple_moving_average(prices: List[float], window: int) -> List[Optional[float]]:
        """
        Calculates the Simple Moving Average (SMA) over a rolling window.
        Returns None for indices before the window is satisfied.
        """
        if window <= 0:
            raise ValueError("Window size must be greater than zero.")
        if not prices:
            return []

        sma: List[Optional[float]] = []
        running_sum = 0.0

        for i, price in enumerate(prices):
            running_sum += price
            if i >= window:
                running_sum -= prices[i - window]

            if i >= window - 1:
                sma.append(round(running_sum / window, 4))
            else:
                sma.append(None)

        return sma

    @staticmethod
    def exponential_moving_average(prices: List[float], window: int) -> List[Optional[float]]:
        """
        Calculates the Exponential Moving Average (EMA).
        Multiplier = 2 / (window + 1)
        """
        if window <= 0:
            raise ValueError("Window size must be greater than zero.")
        if len(prices) < window:
            return [None] * len(prices)

        multiplier = 2.0 / (window + 1)
        ema: List[Optional[float]] = [None] * (window - 1)

        # Initial EMA is simple average of first window
        initial_sma = sum(prices[:window]) / window
        ema.append(round(initial_sma, 4))

        for i in range(window, len(prices)):
            current_ema = (prices[i] - ema[-1]) * multiplier + ema[-1]
            ema.append(round(current_ema, 4))

        return ema

    @staticmethod
    def relative_strength_index(prices: List[float], period: int = 14) -> List[Optional[float]]:
        """
        Calculates the Relative Strength Index (RSI) using Wilder's smoothing technique.
        RSI = 100 - (100 / (1 + RS))
        RS = Average Gain / Average Loss
        """
        if period <= 0:
            raise ValueError("Period must be greater than zero.")
        if len(prices) <= period:
            return [None] * len(prices)

        rsi: List[Optional[float]] = [None] * period

        gains = []
        losses = []
        for i in range(1, period + 1):
            change = prices[i] - prices[i - 1]
            gains.append(max(0.0, change))
            losses.append(max(0.0, -change))

        avg_gain = sum(gains) / period
        avg_loss = sum(losses) / period

        if avg_loss == 0.0:
            rsi.append(100.0)
        else:
            rs = avg_gain / avg_loss
            rsi.append(round(100.0 - (100.0 / (1.0 + rs)), 2))

        for i in range(period + 1, len(prices)):
            change = prices[i] - prices[i - 1]
            current_gain = max(0.0, change)
            current_loss = max(0.0, -change)

            avg_gain = (avg_gain * (period - 1) + current_gain) / period
            avg_loss = (avg_loss * (period - 1) + current_loss) / period

            if avg_loss == 0.0:
                rsi.append(100.0)
            else:
                rs = avg_gain / avg_loss
                rsi.append(round(100.0 - (100.0 / (1.0 + rs)), 2))

        return rsi

    @staticmethod
    def bollinger_bands(prices: List[float], window: int = 20, num_std: float = 2.0) -> List[Optional[Tuple[float, float, float]]]:
        """
        Calculates Bollinger Bands: (Upper Band, Middle Band, Lower Band).
        Middle = SMA(window)
        Upper = SMA + (num_std * standard_deviation)
        Lower = SMA - (num_std * standard_deviation)
        """
        if window <= 1:
            raise ValueError("Window must be greater than 1.")
        if len(prices) < window:
            return [None] * len(prices)

        bands: List[Optional[Tuple[float, float, float]]] = [None] * (window - 1)

        for i in range(window - 1, len(prices)):
            slice_window = prices[i - window + 1 : i + 1]
            mean = sum(slice_window) / window
            variance = sum((x - mean) ** 2 for x in slice_window) / (window - 1)
            std_dev = math.sqrt(variance)

            upper = round(mean + (num_std * std_dev), 4)
            middle = round(mean, 4)
            lower = round(mean - (num_std * std_dev), 4)
            bands.append((upper, middle, lower))

        return bands

    @staticmethod
    def macd(prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, List[Optional[float]]]:
        """
        Calculates Moving Average Convergence Divergence (MACD).
        MACD Line = EMA(fast) - EMA(slow)
        Signal Line = EMA(MACD Line, signal)
        Histogram = MACD Line - Signal Line
        """
        if fast >= slow:
            raise ValueError("Fast period must be strictly less than slow period.")

        fast_ema = TechnicalIndicators.exponential_moving_average(prices, fast)
        slow_ema = TechnicalIndicators.exponential_moving_average(prices, slow)

        macd_line: List[Optional[float]] = []
        valid_macd_values: List[float] = []

        for f, s in zip(fast_ema, slow_ema):
            if f is not None and s is not None:
                diff = round(f - s, 4)
                macd_line.append(diff)
                valid_macd_values.append(diff)
            else:
                macd_line.append(None)

        # Compute signal line over MACD line
        signal_line: List[Optional[float]] = [None] * (len(prices) - len(valid_macd_values))
        if len(valid_macd_values) >= signal:
            raw_signal = TechnicalIndicators.exponential_moving_average(valid_macd_values, signal)
            signal_line.extend(raw_signal)
        else:
            signal_line.extend([None] * len(valid_macd_values))

        histogram: List[Optional[float]] = []
        for m, sig in zip(macd_line, signal_line):
            if m is not None and sig is not None:
                histogram.append(round(m - sig, 4))
            else:
                histogram.append(None)

        return {
            "macd_line": macd_line,
            "signal_line": signal_line,
            "histogram": histogram
        }

    @staticmethod
    def vwap(prices: List[float], volumes: List[float]) -> List[Optional[float]]:
        """
        Calculates Cumulative Volume-Weighted Average Price (VWAP).
        VWAP = Cumulative(Price * Volume) / Cumulative(Volume)
        """
        if len(prices) != len(volumes):
            raise ValueError("Prices and volumes lists must have identical lengths.")
        if not prices:
            return []

        cum_pv = 0.0
        cum_v = 0.0
        vwap_series: List[Optional[float]] = []

        for p, v in zip(prices, volumes):
            if v < 0:
                raise ValueError("Volume must be non-negative.")
            cum_pv += p * v
            cum_v += v
            if cum_v > 0:
                vwap_series.append(round(cum_pv / cum_v, 4))
            else:
                vwap_series.append(None)

        return vwap_series
