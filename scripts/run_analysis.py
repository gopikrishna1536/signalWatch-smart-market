#!/usr/bin/env python3
"""
CLI runner for SignalWatch market analysis.
"""
import json
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from signalwatch.indicators import TechnicalIndicators
from signalwatch.signals import MarketSignalEngine

def analyze_ticker(ticker: str, data: dict):
    prices = data["prices"]
    volumes = data["volumes"]

    print("=" * 60)
    print(f"  QUANTITATIVE TECHNICAL ANALYSIS: {ticker} ({data['name']})")
    print("=" * 60)
    print(f"Data Points: {len(prices)} candles")
    print(f"Latest Price: ${prices[-1]:,.2f}")

    sma_5 = TechnicalIndicators.simple_moving_average(prices, 5)[-1]
    sma_20 = TechnicalIndicators.simple_moving_average(prices, 20)[-1]
    print(f"SMA(5):  ${sma_5:,.2f}" if sma_5 else "SMA(5):  N/A")
    print(f"SMA(20): ${sma_20:,.2f}" if sma_20 else "SMA(20): N/A")

    rsi_eval = MarketSignalEngine.evaluate_rsi_conditions(prices, period=14)
    print(f"RSI(14): {rsi_eval['current_rsi']} [{rsi_eval['status']} -> {rsi_eval['recommendation']}]")

    vwap_val = TechnicalIndicators.vwap(prices, volumes)[-1]
    print(f"Cumulative VWAP: ${vwap_val:,.2f}")

    crossovers = MarketSignalEngine.detect_ma_crossover(prices, fast_window=5, slow_window=20)
    if crossovers:
        print(f"\nDetected Signals: {len(crossovers)}")
        for sig in crossovers:
            print(f"  • Candle #{sig['index']}: {sig['signal']} at price ${sig['price']:,.2f}")
    else:
        print("\nNo recent moving average crossovers detected.")
    print("=" * 60 + "\n")

def main():
    sample_file = PROJECT_ROOT / "data" / "market_samples.json"
    if not sample_file.exists():
        print("Market sample data not found.")
        return

    with open(sample_file, "r") as f:
        samples = json.load(f)

    for ticker, data in samples.items():
        analyze_ticker(ticker, data)

if __name__ == "__main__":
    main()
