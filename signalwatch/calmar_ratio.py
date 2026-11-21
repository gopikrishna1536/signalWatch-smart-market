"""
Calmar Ratio Evaluator
Calmar Ratio = Annualized Compound Return / Maximum Drawdown
Used primarily in hedge fund and CTA performance assessment.
"""
from typing import Dict, Any

class CalmarRatio:
    @staticmethod
    def calculate(annualized_return_percent: float, max_drawdown_percent: float) -> Dict[str, Any]:
        abs_mdd = abs(max_drawdown_percent)
        if abs_mdd == 0:
            ratio = 99.0
        else:
            ratio = round(annualized_return_percent / abs_mdd, 2)

        tier = "Excellent" if ratio >= 3.0 else ("Good" if ratio >= 1.5 else "Suboptimal")
        return {
            "annualized_return_percent": annualized_return_percent,
            "max_drawdown_percent": abs_mdd,
            "calmar_ratio": ratio,
            "performance_tier": tier
        }
