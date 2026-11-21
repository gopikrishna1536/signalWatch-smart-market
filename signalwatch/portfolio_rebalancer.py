"""
Portfolio Target Allocation Drift & Rebalancer
Detects portfolio weights deviating beyond tolerance bands and generates corrective orders.
"""
from typing import Dict, List, Any

class PortfolioRebalancer:
    @staticmethod
    def generate_rebalance_orders(current_holdings: Dict[str, float], target_weights: Dict[str, float], drift_threshold: float = 0.05) -> Dict[str, Any]:
        total_value = sum(current_holdings.values())
        if total_value <= 0:
            raise ValueError("Portfolio must have positive total value")

        orders = []
        drifts = {}

        for asset, target_w in target_weights.items():
            curr_val = current_holdings.get(asset, 0.0)
            curr_w = curr_val / total_value
            drift = curr_w - target_w
            drifts[asset] = round(drift, 4)

            if abs(drift) >= drift_threshold:
                target_val = total_value * target_w
                order_amount = round(target_val - curr_val, 2)
                action = "BUY" if order_amount > 0 else "SELL"
                orders.append({
                    "asset": asset,
                    "action": action,
                    "amount": abs(order_amount),
                    "current_weight": round(curr_w * 100, 2),
                    "target_weight": round(target_w * 100, 2)
                })

        return {
            "total_portfolio_value": total_value,
            "rebalance_required": len(orders) > 0,
            "drifts": drifts,
            "orders": orders
        }
