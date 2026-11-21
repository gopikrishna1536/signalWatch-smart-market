"""
Vortex Indicator (VI+ and VI-)
Identifies start of a new trend or confirms existing trend direction.
"""
from typing import List, Dict, Any

class VortexIndicator:
    @staticmethod
    def calculate(highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> Dict[str, List[float]]:
        n = len(closes)
        if n <= period:
            raise ValueError("Insufficient data points for Vortex Indicator")

        vm_plus = [abs(highs[i] - lows[i - 1]) for i in range(1, n)]
        vm_minus = [abs(lows[i] - highs[i - 1]) for i in range(1, n)]
        tr = [max(highs[i] - lows[i], abs(highs[i] - closes[i - 1]), abs(lows[i] - closes[i - 1])) for i in range(1, n)]

        vi_plus_list = []
        vi_minus_list = []

        for i in range(period - 1, len(vm_plus)):
            sum_tr = sum(tr[i - period + 1:i + 1])
            sum_vmp = sum(vm_plus[i - period + 1:i + 1])
            sum_vmm = sum(vm_minus[i - period + 1:i + 1])

            vi_plus = round(sum_vmp / sum_tr, 4) if sum_tr > 0 else 1.0
            vi_minus = round(sum_vmm / sum_tr, 4) if sum_tr > 0 else 1.0

            vi_plus_list.append(vi_plus)
            vi_minus_list.append(vi_minus)

        return {
            "vi_plus": vi_plus_list,
            "vi_minus": vi_minus_list
        }
