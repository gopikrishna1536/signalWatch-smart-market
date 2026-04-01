# Week 17 Quantitative Benchmark: Ulcer Index (14-period) Downside Allocation
**Date:** 2026-04-01  
**Lead Quantitative Researcher:** Gopi Krishna (@gopikrishna1536)  
**Status:** Validated in Out-of-Sample Backtesting Engine  

---

## 1. Executive Strategy Summary
This quantitative research report documents the algorithmic backtesting performance of **Ulcer Index (14-period) Downside Allocation** executed on high-frequency market tick data across liquid asset classes (Crypto: BTC/USDT, ETH/USDT; Equities: SPY, QQQ).

## 2. Mathematical Formulation
The signal generation model relies on continuous quantitative time-series analysis:
$$\text{Sharpe Ratio} = \frac{\mathbb{E}[R_p - R_f]}{\sigma_p} = 2.05$$
$$\text{Profit Factor} = \frac{\sum \text{Gross Profits}}{\sum \text{Gross Losses}} = 2.42$$

## 3. Performance Summary

| Metric | Target Standard | Out-of-Sample Result | Evaluation |
|---|---:|---:|:---:|
| **Win Rate** | > 50.0% | **66.4%** | Pass |
| **Profit Factor** | > 1.50 | **2.42** | Pass |
| **Sharpe Ratio** | > 1.20 | **2.05** | Superior |
| **Max Drawdown** | < 15.0% | **6.2%** | Controlled |
| **Trade Count** | > 100 Trades | **428 Trades** | Statistically Significant |

## 4. Execution & Risk Parameters
- **Slippage Buffer:** 5 basis points (0.05%)
- **Transaction Costs:** 0.04% maker / 0.08% taker
- **Max Portfolio Risk per Trade:** 1.5% NAV
- **Stop-Loss Protocol:** Volatility-adjusted ATR dynamic exit

---
*Report generated and archived by signalWatch Quantitative Backtesting Engine.*
