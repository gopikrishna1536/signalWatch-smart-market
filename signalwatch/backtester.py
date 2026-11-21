"""
Algorithmic Trading Strategy Backtesting Engine for SignalWatch.
Simulates order execution, tracks equity curves, and computes quantitative performance metrics.
"""
from typing import List, Optional, Dict, Any

class StrategyBacktester:
    def __init__(self, initial_capital: float = 10000.0, commission_rate: float = 0.001):
        if initial_capital <= 0:
            raise ValueError("Initial capital must be positive.")
        if commission_rate < 0 or commission_rate >= 1:
            raise ValueError("Commission rate must be between 0 and 1.")

        self.initial_capital = initial_capital
        self.commission_rate = commission_rate

    def run_backtest(self, prices: List[float], signals: List[Optional[str]]) -> Dict[str, Any]:
        """
        Runs a simulation on historical prices and corresponding signals ('BUY', 'SELL', 'HOLD').
        """
        if len(prices) != len(signals):
            raise ValueError("Prices and signals lists must have identical lengths.")
        if not prices:
            raise ValueError("Price series cannot be empty.")

        cash = self.initial_capital
        shares = 0
        entry_price = 0.0
        equity_curve: List[float] = []
        trades: List[Dict[str, Any]] = []

        for i, (price, sig) in enumerate(zip(prices, signals)):
            if price <= 0:
                raise ValueError("Asset prices must be strictly positive.")

            # Process Signal
            if sig == "BUY" and shares == 0:
                # Buy as many whole shares as possible
                available_for_shares = cash / (1.0 + self.commission_rate)
                shares_to_buy = int(available_for_shares // price)
                if shares_to_buy > 0:
                    cost = shares_to_buy * price
                    comm = cost * self.commission_rate
                    cash -= (cost + comm)
                    shares = shares_to_buy
                    entry_price = price

            elif sig == "SELL" and shares > 0:
                proceeds = shares * price
                comm = proceeds * self.commission_rate
                net_proceeds = proceeds - comm
                pnl = net_proceeds - (shares * entry_price * (1.0 + self.commission_rate))
                ret_pct = ((price - entry_price) / entry_price) * 100.0

                trades.append({
                    "entry_index": i - 1, # approximate
                    "exit_index": i,
                    "entry_price": entry_price,
                    "exit_price": price,
                    "shares": shares,
                    "pnl": round(pnl, 2),
                    "return_pct": round(ret_pct, 2)
                })

                cash += net_proceeds
                shares = 0
                entry_price = 0.0

            current_equity = cash + (shares * price)
            equity_curve.append(round(current_equity, 2))

        # Close any lingering open position at last price
        if shares > 0:
            last_price = prices[-1]
            proceeds = shares * last_price
            comm = proceeds * self.commission_rate
            net_proceeds = proceeds - comm
            pnl = net_proceeds - (shares * entry_price * (1.0 + self.commission_rate))
            ret_pct = ((last_price - entry_price) / entry_price) * 100.0

            trades.append({
                "entry_index": len(prices) - 2,
                "exit_index": len(prices) - 1,
                "entry_price": entry_price,
                "exit_price": last_price,
                "shares": shares,
                "pnl": round(pnl, 2),
                "return_pct": round(ret_pct, 2)
            })
            cash += net_proceeds
            shares = 0

        final_equity = round(cash, 2)
        total_return_pct = round(((final_equity - self.initial_capital) / self.initial_capital) * 100.0, 2)

        # Performance Metrics
        total_trades = len(trades)
        winning_trades = [t for t in trades if t["pnl"] > 0]
        losing_trades = [t for t in trades if t["pnl"] < 0]

        win_rate_pct = round((len(winning_trades) / total_trades) * 100.0, 2) if total_trades > 0 else 0.0

        gross_profit = sum(t["pnl"] for t in winning_trades)
        gross_loss = abs(sum(t["pnl"] for t in losing_trades))
        profit_factor = round(gross_profit / gross_loss, 2) if gross_loss > 0 else (99.0 if gross_profit > 0 else 0.0)

        # Maximum Drawdown calculation
        peak = self.initial_capital
        max_drawdown = 0.0
        for eq in equity_curve:
            if eq > peak:
                peak = eq
            dd = (peak - eq) / peak * 100.0
            if dd > max_drawdown:
                max_drawdown = dd

        return {
            "initial_capital": self.initial_capital,
            "final_equity": final_equity,
            "total_return_pct": total_return_pct,
            "total_trades": total_trades,
            "winning_trades": len(winning_trades),
            "losing_trades": len(losing_trades),
            "win_rate_pct": win_rate_pct,
            "profit_factor": profit_factor,
            "max_drawdown_pct": round(max_drawdown, 2),
            "trades": trades,
            "equity_curve": equity_curve
        }
