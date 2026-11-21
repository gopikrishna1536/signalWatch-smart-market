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

    @staticmethod
    def average_true_range(
        highs: List[float],
        lows: List[float],
        closes: List[float],
        period: int = 14
    ) -> List[Optional[float]]:
        """
        Calculates Average True Range (ATR) using Wilder's smoothing method.
        TR = max(High - Low, |High - PrevClose|, |Low - PrevClose|)
        """
        n = len(closes)
        if len(highs) != n or len(lows) != n:
            raise ValueError("Highs, lows, and closes lists must have identical lengths.")
        if period <= 0:
            raise ValueError("Period must be greater than zero.")
        if n < period:
            return [None] * n

        # Calculate True Range (TR)
        tr_list: List[float] = []
        for i in range(n):
            if i == 0:
                tr = highs[i] - lows[i]
            else:
                prev_close = closes[i - 1]
                tr = max(
                    highs[i] - lows[i],
                    abs(highs[i] - prev_close),
                    abs(lows[i] - prev_close)
                )
            tr_list.append(tr)

        atr: List[Optional[float]] = [None] * (period - 1)
        # Initial ATR is simple average of first period TRs
        initial_atr = sum(tr_list[:period]) / period
        atr.append(round(initial_atr, 4))

        current_atr = initial_atr
        for i in range(period, n):
            current_atr = (current_atr * (period - 1) + tr_list[i]) / period
            atr.append(round(current_atr, 4))

        return atr

    @staticmethod
    def supertrend(
        highs: List[float],
        lows: List[float],
        closes: List[float],
        period: int = 10,
        multiplier: float = 3.0
    ) -> Dict[str, List[Optional[float]]]:
        """
        Calculates the SuperTrend indicator.
        Returns dictionary containing:
        - 'supertrend': the active dynamic trailing stop level
        - 'direction': 1 for bullish (uptrend), -1 for bearish (downtrend)
        """
        atr = TechnicalIndicators.average_true_range(highs, lows, closes, period)
        n = len(closes)

        supertrend: List[Optional[float]] = [None] * n
        direction: List[Optional[int]] = [None] * n

        upper_band: List[float] = [0.0] * n
        lower_band: List[float] = [0.0] * n

        first_valid = period - 1
        for i in range(first_valid, n):
            hl2 = (highs[i] + lows[i]) / 2.0
            basic_upper = hl2 + (multiplier * atr[i])
            basic_lower = hl2 - (multiplier * atr[i])

            if i == first_valid:
                upper_band[i] = basic_upper
                lower_band[i] = basic_lower
                direction[i] = 1 if closes[i] >= lower_band[i] else -1
                supertrend[i] = round(lower_band[i] if direction[i] == 1 else upper_band[i], 4)
                continue

            # Upper Band logic
            if basic_upper < upper_band[i - 1] or closes[i - 1] > upper_band[i - 1]:
                upper_band[i] = basic_upper
            else:
                upper_band[i] = upper_band[i - 1]

            # Lower Band logic
            if basic_lower > lower_band[i - 1] or closes[i - 1] < lower_band[i - 1]:
                lower_band[i] = basic_lower
            else:
                lower_band[i] = lower_band[i - 1]

            # Direction logic
            if supertrend[i - 1] == upper_band[i - 1]:
                direction[i] = 1 if closes[i] > upper_band[i] else -1
            else:
                direction[i] = -1 if closes[i] < lower_band[i] else 1

            supertrend[i] = round(lower_band[i] if direction[i] == 1 else upper_band[i], 4)

        return {
            "supertrend": supertrend,
            "direction": direction
        }

    @staticmethod
    def commodity_channel_index(
        highs: List[float],
        lows: List[float],
        closes: List[float],
        period: int = 20
    ) -> List[Optional[float]]:
        """
        Calculates Commodity Channel Index (CCI).
        CCI = (Typical Price - SMA(TP)) / (0.015 * Mean Deviation)
        """
        n = len(closes)
        if len(highs) != n or len(lows) != n:
            raise ValueError("Highs, lows, and closes lists must have identical lengths.")
        if period <= 0:
            raise ValueError("Period must be greater than zero.")
        if n < period:
            return [None] * n

        typical_prices = [(highs[i] + lows[i] + closes[i]) / 3.0 for i in range(n)]
        cci_series: List[Optional[float]] = [None] * (period - 1)

        for i in range(period - 1, n):
            window = typical_prices[i - period + 1 : i + 1]
            sma_tp = sum(window) / period
            mean_dev = sum(abs(tp - sma_tp) for tp in window) / period

            if mean_dev == 0:
                cci_series.append(0.0)
            else:
                cci = (typical_prices[i] - sma_tp) / (0.015 * mean_dev)
                cci_series.append(round(cci, 4))

        return cci_series

    @staticmethod
    def williams_r(
        highs: List[float],
        lows: List[float],
        closes: List[float],
        period: int = 14
    ) -> List[Optional[float]]:
        """
        Calculates Williams %R oscillator (-100 to 0).
        %R = (Highest High - Close) / (Highest High - Lowest Low) * -100
        """
        n = len(closes)
        if len(highs) != n or len(lows) != n:
            raise ValueError("Highs, lows, and closes lists must have identical lengths.")
        if period <= 0:
            raise ValueError("Period must be greater than zero.")
        if n < period:
            return [None] * n

        wr_series: List[Optional[float]] = [None] * (period - 1)

        for i in range(period - 1, n):
            highest_high = max(highs[i - period + 1 : i + 1])
            lowest_low = min(lows[i - period + 1 : i + 1])
            denom = highest_high - lowest_low

            if denom == 0:
                wr_series.append(-50.0)
            else:
                wr = ((highest_high - closes[i]) / denom) * -100.0
                wr_series.append(round(wr, 4))

        return wr_series
