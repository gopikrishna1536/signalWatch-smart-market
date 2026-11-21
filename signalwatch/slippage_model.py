"""
Order Execution Slippage & Market Impact Model
Estimates price slippage based on trade size relative to average daily volume (ADV).
"""
import math
from typing import Dict, Any

class SlippageModel:
    @staticmethod
    def estimate_slippage(trade_value: float, adv: float, volatility: float = 0.02) -> Dict[str, Any]:
        if adv <= 0 or trade_value <= 0:
            raise ValueError("Trade value and ADV must be positive non-zero")

        participation_rate = trade_value / adv
        market_impact_bps = round(0.5 * volatility * math.sqrt(participation_rate) * 10000, 2)
        slippage_cost = round(trade_value * (market_impact_bps / 10000.0), 2)

        return {
            "trade_value": trade_value,
            "participation_rate_percent": round(participation_rate * 100, 3),
            "estimated_impact_bps": market_impact_bps,
            "estimated_slippage_cost": slippage_cost
        }
