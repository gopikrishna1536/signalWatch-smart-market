"""
Quantitative Risk & Portfolio Performance Metrics for SignalWatch.
Implements annualized Sharpe Ratio, Sortino Ratio, Downside Deviation, and Calmar Ratio.
"""
from typing import List, Dict, Any
import math

class RiskMetricsCalculator:
    @staticmethod
    def calculate_returns_from_prices(prices: List[float]) -> List[float]:
        """
        Converts a price series into percentage periodic returns.
        """
        if len(prices) < 2:
            return []
        returns = []
        for i in range(1, len(prices)):
            if prices[i - 1] <= 0:
                raise ValueError("Asset prices must be strictly positive.")
            ret = (prices[i] - prices[i - 1]) / prices[i - 1]
            returns.append(ret)
        return returns

    @staticmethod
    def mean_return(returns: List[float]) -> float:
        if not returns:
            return 0.0
        return sum(returns) / len(returns)

    @staticmethod
    def volatility(returns: List[float], annualized: bool = True, trading_days: int = 252) -> float:
        """
        Calculates standard deviation of returns, optionally annualized by sqrt(trading_days).
        """
        if len(returns) < 2:
            return 0.0
        mean = sum(returns) / len(returns)
        variance = sum((r - mean) ** 2 for r in returns) / (len(returns) - 1)
        std_dev = math.sqrt(variance)
        return round(std_dev * math.sqrt(trading_days) if annualized else std_dev, 4)

    @staticmethod
    def downside_deviation(returns: List[float], target_return: float = 0.0, annualized: bool = True, trading_days: int = 252) -> float:
        """
        Calculates downside deviation (semi-variance) considering only returns below the target return.
        """
        downside_diffs = [min(0.0, r - target_return) ** 2 for r in returns]
        if not downside_diffs or len(returns) < 2:
            return 0.0
        downside_variance = sum(downside_diffs) / (len(returns) - 1)
        downside_std = math.sqrt(downside_variance)
        return round(downside_std * math.sqrt(trading_days) if annualized else downside_std, 4)

    @staticmethod
    def sharpe_ratio(returns: List[float], risk_free_rate: float = 0.04, trading_days: int = 252) -> float:
        """
        Calculates the annualized Sharpe Ratio.
        Sharpe = (Annualized Return - Risk Free Rate) / Annualized Volatility
        """
        if len(returns) < 2:
            return 0.0
        mean_ret = sum(returns) / len(returns)
        annualized_ret = mean_ret * trading_days
        ann_vol = RiskMetricsCalculator.volatility(returns, annualized=True, trading_days=trading_days)
        if ann_vol <= 0:
            return 0.0
        return round((annualized_ret - risk_free_rate) / ann_vol, 4)

    @staticmethod
    def sortino_ratio(returns: List[float], risk_free_rate: float = 0.04, target_return: float = 0.0, trading_days: int = 252) -> float:
        """
        Calculates the annualized Sortino Ratio.
        Sortino = (Annualized Return - Risk Free Rate) / Annualized Downside Deviation
        """
        if len(returns) < 2:
            return 0.0
        mean_ret = sum(returns) / len(returns)
        annualized_ret = mean_ret * trading_days
        downside_dev = RiskMetricsCalculator.downside_deviation(returns, target_return, annualized=True, trading_days=trading_days)
        if downside_dev <= 0:
            return 99.0 if (annualized_ret - risk_free_rate) > 0 else 0.0
        return round((annualized_ret - risk_free_rate) / downside_dev, 4)

    @staticmethod
    def analyze_portfolio_risk(prices: List[float], risk_free_rate: float = 0.04) -> Dict[str, Any]:
        """
        Comprehensive risk analysis summary for a price series.
        """
        returns = RiskMetricsCalculator.calculate_returns_from_prices(prices)
        if not returns:
            return {"error": "Insufficient price data for risk analysis."}

        ann_vol = RiskMetricsCalculator.volatility(returns, annualized=True)
        downside_dev = RiskMetricsCalculator.downside_deviation(returns, annualized=True)
        sharpe = RiskMetricsCalculator.sharpe_ratio(returns, risk_free_rate=risk_free_rate)
        sortino = RiskMetricsCalculator.sortino_ratio(returns, risk_free_rate=risk_free_rate)

        mean_daily = round(RiskMetricsCalculator.mean_return(returns), 6)
        annualized_return = round(mean_daily * 252 * 100, 2)

        return {
            "periods_analyzed": len(returns),
            "mean_daily_return": mean_daily,
            "annualized_return_pct": annualized_return,
            "annualized_volatility": ann_vol,
            "downside_deviation": downside_dev,
            "sharpe_ratio": sharpe,
            "sortino_ratio": sortino,
            "risk_profile": "AGGRESSIVE" if ann_vol > 0.25 else ("MODERATE" if ann_vol > 0.15 else "CONSERVATIVE")
        }
