"""
On-Balance Volume (OBV)
Cumulative momentum indicator linking price change to total volume flow.
"""
from typing import List

class OnBalanceVolume:
    @staticmethod
    def calculate(closes: List[float], volumes: List[float]) -> List[float]:
        if len(closes) != len(volumes):
            raise ValueError("Closes and volumes lists must have matching lengths")
        if not closes:
            return []

        obv = [volumes[0]]
        for i in range(1, len(closes)):
            if closes[i] > closes[i - 1]:
                obv.append(obv[-1] + volumes[i])
            elif closes[i] < closes[i - 1]:
                obv.append(obv[-1] - volumes[i])
            else:
                obv.append(obv[-1])

        return obv
