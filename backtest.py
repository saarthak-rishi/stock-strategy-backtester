import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def run_backtest(signals, initial_capital=100000):
    """
    Simulates trades based on signals and returns a portfolio DataFrame.
    """
    portfolio = signals[['price']].copy()
    portfolio['holdings'] = 0.0
    portfolio['cash'] = float(initial_capital)
    portfolio['total'] = float(initial_capital)
    portfolio['returns'] = 0.0

    position = 0
    cash = float(initial_capital)

    for i in range(1, len(portfolio)):
        price = portfolio['price'].iloc[i]
        signal = signals['signal'].iloc[i]

        if signal == 1 and position == 0:
            shares = cash // price
            position = shares
            cash -= shares * price
        elif signal == -1 and position > 0:
            cash += position * price
            position = 0

        portfolio.iloc[i, portfolio.columns.get_loc('holdings')] = position * price
        portfolio.iloc[i, portfolio.columns.get_loc('cash')] = cash
        portfolio.iloc[i, portfolio.columns.get_loc('total')] = cash + position * price

    portfolio['returns'] = portfolio['total'].pct_change()
    return portfolio

def calculate_metrics(portfolio, strategy_name="Strategy"):
    """
    Prints key performance metrics for a backtested portfolio.
    """
    total_return = (portfolio['total'].iloc[-1] / portfolio['total'].iloc[0] - 1) * 100
    daily_returns = portfolio['returns'].dropna()

    sharpe = (daily_returns.mean() / daily_returns.std()) * np.sqrt(252) if daily_returns.std() != 0 else 0

    rolling_max = portfolio['total'].cummax()
    drawdown = (portfolio['total'] - rolling_max) / rolling_max
    max_drawdown = drawdown.min() * 100

    trades = portfolio['total'].diff().dropna()
    wins = (trades > 0).sum()
    losses = (trades < 0).sum()
    win_rate = (wins / (wins + losses) * 100) if (wins + losses) > 0 else 0

    print(f"\n{'='*40}")
    print(f"  {strategy_name}")
    print(f"{'='*40}")
    print(f"  Total Return   : {total_return:.2f}%")
    print(f"  Sharpe Ratio   : {sharpe:.2f}")
    print(f"  Max Drawdown   : {max_drawdown:.2f}%")
    print(f"  Win Rate       : {win_rate:.2f}%")
    print(f"{'='*40}")

    return {
        'total_return': total_return,
        'sharpe': sharpe,
        'max_drawdown': max_drawdown,
        'win_rate': win_rate
    }

def plot_results(portfolio, strategy_name, filename):
    """
    Saves equity curve + drawdown chart to /plots folder.
    """
    os.makedirs("plots", exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    fig.suptitle(strategy_name, fontsize=14, fontweight='bold')

    ax1.plot(portfolio.index, portfolio['total'], label='Portfolio Value', color='steelblue')
    ax1.set_ylabel('Portfolio Value (₹)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    rolling_max = portfolio['total'].cummax()
    drawdown = (portfolio['total'] - rolling_max) / rolling_max * 100
    ax2.fill_between(portfolio.index, drawdown, 0, color='red', alpha=0.4, label='Drawdown')
    ax2.set_ylabel('Drawdown (%)')
    ax2.set_xlabel('Date')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"plots/{filename}.png", dpi=150)
    plt.close()
    print(f"  Chart saved → plots/{filename}.png")