# Stock Price Analysis & Backtested Trading Strategy

Backtesting 3 quantitative trading strategies on the Nifty 50 index (2019–2024) using Python.

## Strategies
| Strategy | Logic |
|---|---|
| Moving Average Crossover | Buy when 20-day MA crosses above 50-day MA, sell when it crosses below |
| RSI | Buy when RSI < 30 (oversold), sell when RSI > 70 (overbought) |
| Momentum | Buy on breakout above 20-day high, sell on breakdown below 20-day low |

## Metrics Evaluated
- Total Return
- Sharpe Ratio
- Max Drawdown
- Win Rate

## Stack
`Python` · `yfinance` · `pandas` · `numpy` · `matplotlib`

## How to Run
```bash
pip install yfinance pandas matplotlib numpy
python main.py
```

## Sample Output — Momentum Strategy
![Momentum Strategy](plots/momentum.png)

