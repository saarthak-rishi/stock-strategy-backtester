import pandas as pd
import numpy as np

def moving_average_crossover(df, short_window=20, long_window=50):
    """
    Signal: +1 when short MA crosses above long MA, -1 when below.
    """
    signals = pd.DataFrame(index=df.index)
    signals['price'] = df['Close']
    signals['short_ma'] = df['Close'].rolling(window=short_window).mean()
    signals['long_ma'] = df['Close'].rolling(window=long_window).mean()
    signals['signal'] = 0
    signals.loc[signals['short_ma'] > signals['long_ma'], 'signal'] = 1
    signals.loc[signals['short_ma'] <= signals['long_ma'], 'signal'] = -1
    signals['position'] = signals['signal'].diff()
    return signals

def rsi_strategy(df, period=14, overbought=70, oversold=30):
    """
    Signal: Buy when RSI < oversold, sell when RSI > overbought.
    """
    signals = pd.DataFrame(index=df.index)
    signals['price'] = df['Close']

    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    signals['rsi'] = 100 - (100 / (1 + rs))

    signals['signal'] = 0
    signals.loc[signals['rsi'] < oversold, 'signal'] = 1
    signals.loc[signals['rsi'] > overbought, 'signal'] = -1
    signals['position'] = signals['signal'].diff()
    return signals

def momentum_strategy(df, window=20):
    """
    Signal: Buy if price is above its N-day high, sell if below N-day low.
    """
    signals = pd.DataFrame(index=df.index)
    signals['price'] = df['Close']
    signals['rolling_high'] = df['Close'].rolling(window=window).max()
    signals['rolling_low'] = df['Close'].rolling(window=window).min()
    close = df['Close'].squeeze()
    signals['signal'] = 0
    signals.loc[close >= signals['rolling_high'], 'signal'] = 1
    signals.loc[close <= signals['rolling_low'], 'signal'] = -1
    signals['position'] = signals['signal'].diff()
    return signals