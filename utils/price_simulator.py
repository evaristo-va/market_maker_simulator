import numpy as np
import pandas as pd
import numpy as np

def simulate_prices(T: int = 390, S0: float = 100, mu: float = 0.0001, sigma: float = 0.001, dt: float = 1/390) -> pd.Series:
    prices = np.zeros(T)
    prices[0] = S0
    for t in range(1,T):
        # geometric brownian motion
        prices[t] = prices[t-1] * np.exp((mu - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*np.random.randn())
    
    return pd.Series(prices, name="Price")
