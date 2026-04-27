import yfinance as yf
import os
from strategies import moving_average_crossover, rsi_strategy, momentum_strategy
from backtest import run_backtest, calculate_metrics, plot_results

# ── Configuration ──────────────────────────────────────────
TICKER = "^NSEI"          # Nifty 50 index
START_DATE = "2019-01-01"
END_DATE = "2024-12-31"
INITIAL_CAPITAL = 100_000  # ₹1,00,000
# ───────────────────────────────────────────────────────────

def main():
    print(f"Fetching data for {TICKER} from {START_DATE} to {END_DATE}...")
    df = yf.download(TICKER, start=START_DATE, end=END_DATE, auto_adjust=True)

    if df.empty:
        print("No data returned. Check your ticker or internet connection.")
        return

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/nifty50.csv")
    print(f"Data saved → data/nifty50.csv ({len(df)} rows)")

    strategies = [
        ("Moving Average Crossover", moving_average_crossover(df), "ma_crossover"),
        ("RSI Strategy",             rsi_strategy(df),              "rsi"),
        ("Momentum Strategy",        momentum_strategy(df),         "momentum"),
    ]

    for name, signals, filename in strategies:
        portfolio = run_backtest(signals, initial_capital=INITIAL_CAPITAL)
        calculate_metrics(portfolio, strategy_name=name)
        plot_results(portfolio, strategy_name=name, filename=filename)

    print("\nAll strategies complete. Check the /plots folder for charts.")

if __name__ == "__main__":
    main()