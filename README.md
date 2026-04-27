# Stock Price Analysis & Backtested Trading Strategy

Backtesting 3 quantitative trading strategies on the Nifty 50 index using Python.

## Strategies Implemented
- **Moving Average Crossover** — 20/50 day MA crossover signals
- **RSI Strategy** — Buy on oversold (<30), sell on overbought (>70)
- **Momentum Strategy** — Breakout above rolling high / breakdown below rolling low

## Performance Metrics
Each strategy is evaluated on:
- Total Return
- Sharpe Ratio
- Maximum Drawdown
- Win Rate

## Stack
`Python` · `yfinance` · `pandas` · `numpy` · `matplotlib`

## How to Run
```bash
pip install yfinance pandas matplotlib numpy
python main.py
```

<img width="1800" height="1200" alt="momentum" src="https://github.com/user-attachments/assets/29c64706-bdf3-4f44-90e7-53581a32d0a9" />


Charts are saved to `/plots`. Raw data saved to `/data`.

## Sample Output
![alt text](rsi.png)
![alt text](ma_crossover.png)
![alt text](momentum-1.png)
