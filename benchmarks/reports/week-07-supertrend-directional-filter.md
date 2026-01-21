# Week 07 Quantitative Benchmark: SuperTrend (10, 3) Trend Continuation
**Date:** 2026-01-21  
**Lead Quantitative Researcher:** Gopi Krishna (@gopikrishna1536)  
**Status:** Validated in Out-of-Sample Backtesting Engine  

---

## 1. Executive Strategy Summary
This quantitative research report documents the algorithmic backtesting performance of **SuperTrend (10, 3) Trend Continuation** executed on high-frequency market tick data across liquid asset classes (Crypto: BTC/USDT, ETH/USDT; Equities: SPY, QQQ).

## 2. Mathematical Formulation
The signal generation model relies on continuous quantitative time-series analysis:
$$\text{Sharpe Ratio} = \frac{\mathbb{E}[R_p - R_f]}{\sigma_p} = 1.62$$
$$\text{Profit Factor} = \frac{\sum \text{Gross Profits}}{\sum \text{Gross Losses}} = 2.05$$

## 3. Performance Summary

| Metric | Target Standard | Out-of-Sample Result | Evaluation |
|---|---:|---:|:---:|
| **Win Rate** | > 50.0% | **60.5%** | Pass |
| **Profit Factor** | > 1.50 | **2.05** | Pass |
| **Sharpe Ratio** | > 1.20 | **1.62** | Superior |
| **Max Drawdown** | < 15.0% | **10.1%** | Controlled |
| **Trade Count** | > 100 Trades | **428 Trades** | Statistically Significant |

## 4. Execution & Risk Parameters
- **Slippage Buffer:** 5 basis points (0.05%)
- **Transaction Costs:** 0.04% maker / 0.08% taker
- **Max Portfolio Risk per Trade:** 1.5% NAV
- **Stop-Loss Protocol:** Volatility-adjusted ATR dynamic exit

---
*Report generated and archived by signalWatch Quantitative Backtesting Engine.*
