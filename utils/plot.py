import pandas as pd
import matplotlib.pyplot as plt

def plot_simulation(df: pd.Series) -> None:
    """
    Plot the results of the market-making simulation.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame returned from run_simulation()
    """

    # 1. Price dynamics and MM quotes
    plt.figure(figsize=(14,6))
    plt.plot(df['Price'], label='Simulated GBM Price')
    plt.plot(df['MidPrice'], label='Dynamic Mid Price', alpha=0.8)
    plt.plot(df['MM_Bid'], '--', label='MM Bid', color='green')
    plt.plot(df['MM_Ask'], '--', label='MM Ask', color='red')
    plt.xlabel('Time Step')
    plt.ylabel('Price')
    plt.title('Market-Making Simulation: Prices and MM Quotes')
    plt.legend()
    plt.show()

    # 2. Market Maker inventory
    plt.figure(figsize=(14,4))
    plt.plot(df['Inventory'], label='MM Inventory', color='purple')
    plt.xlabel('Time Step')
    plt.ylabel('Shares')
    plt.title('Market Maker Inventory Over Time')
    plt.legend()
    plt.show()

    # 3. Mark-to-market P&L
    plt.figure(figsize=(14,4))
    plt.plot(df['MTM_PnL'], label='MM MTM P&L', color='green')
    plt.xlabel('Time Step')
    plt.ylabel('PnL ($)')
    plt.title('Market Maker P&L Over Time')
    plt.legend()
    plt.show()

    # realized pnl
    plt.figure(figsize=(14,4))
    plt.plot(df['Realized_PnL'].cumsum(), label='Cumulative Realized PnL', color='blue')
    plt.xlabel('Time Step')
    plt.ylabel('Cumulative PnL ($)')
    plt.title('Cumulative Realized Profit Over Time')
    plt.legend()
    plt.show()

    # 4. MM Bid-Ask spread
    plt.figure(figsize=(14,4))
    spread = df['MM_Ask'] - df['MM_Bid']
    plt.plot(spread, label='MM Bid-Ask Spread', color='red')
    plt.xlabel('Time Step')
    plt.ylabel('Spread ($)')
    plt.title('Market Maker Bid-Ask Spread Over Time')
    plt.legend()
    plt.show()
