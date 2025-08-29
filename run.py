import numpy as np
import pandas as pd
from collections import deque
from utils.price_simulator import simulate_prices
from utils.market_book_simulator import simulate_market_book
from utils.market_maker import get_bid_ask
from utils.execute_trades import execute_trades
from utils.pnl import compute_unrealized_pnl
from typing import Optional, Dict

def run_simulation(
    T: int = 390, 
    S0: float = 100, 
    sigma: float = 0.001,
    trade_qty: int = 50, 
    spread: float = 0.001,
    cost_per_share: float = 0.0, 
    use_avellaneda: bool = False, 
    prices: Optional[pd.Series] = None
) -> pd.DataFrame:
    
    inventory = deque()
    realized_pnl = 0

    inventory_history = []
    mm_bid_history = []
    mm_ask_history = []
    mid_price_history = []
    mtm_pnl_history = []
    realized_pnl_history = []

    if prices is None:
        prices = simulate_prices(T=T, S0=S0, sigma=sigma)

    for t, price in enumerate(prices):

        bids, asks, market_bid, market_ask, mid_price = simulate_market_book(price, lambda_bid = 100, lambda_ask = 100, spread_ratio = spread, vol_ratio = 0.0005)

        inventory_qty = sum(qty for qty,_ in inventory)

        if use_avellaneda:
            mm_bid, mm_ask = get_bid_ask_avellaneda(mid_price, inventory_qty, t/T, 1.0)
        else:
            mm_bid, mm_ask = get_bid_ask(mid_price,inventory_qty,sigma=sigma)


        inventory, realized_pnl, bids, asks = execute_trades(inventory,mm_bid,mm_ask,bids,asks,cost_per_share=cost_per_share)

        # record history
        inventory_history.append(sum(q for q, _ in inventory))
        mm_bid_history.append(mm_bid)
        mm_ask_history.append(mm_ask)
        mid_price_history.append(mid_price)
        mtm_pnl_history.append(realized_pnl + compute_unrealized_pnl(inventory, mid_price,cost_per_share=cost_per_share))
        realized_pnl_history.append(realized_pnl)

    # create DataFrame for plotting
    df = pd.DataFrame({
        'Price': prices,
        'MidPrice': mid_price_history,
        'MM_Bid': mm_bid_history,
        'MM_Ask': mm_ask_history,
        'Inventory': inventory_history,
        'MTM_PnL': mtm_pnl_history,
        'Realized_PnL': realized_pnl_history
    })

    return df
