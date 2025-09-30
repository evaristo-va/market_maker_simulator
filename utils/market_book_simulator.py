import numpy as np
import pandas as pd
from typing import List, Tuple

def simulate_market_book(
	P_ref: float,
	lambda_bid: int = 5,
	lambda_ask: int = 5,
	spread_ratio: float = 0.001,
	vol_ratio: float = 0.0005
	)-> Tuple[List[Tuple[float,int]],List[Tuple[float,int]],float,float,float]:

    n_bids = np.random.poisson(lambda_bid)
    n_asks = np.random.poisson(lambda_ask)

    spread_range = P_ref * spread_ratio
    vol = P_ref * vol_ratio

    if n_bids > 0:
        #bid_prices = P_ref - np.abs(np.random.normal(0, scale=spread_range/2,  size=n_bids))
        bid_prices = P_ref - np.random.rand(n_bids) * spread_range + np.random.normal(0,vol,size=n_bids)
        bid_qty = np.random.randint(1,100, size=n_bids)
        bids = list(zip(bid_prices,bid_qty))
        # sort bids in descending order
        bids.sort(key = lambda x:x[0], reverse=True)
        market_bid = bids[0][0]
    else:
        bids = []
        market_bid = P_ref

    if n_asks > 0:
        #ask_prices = P_ref + np.abs(np.random.normal(loc=0, scale=spread_range/2,  size=n_bids))
        ask_prices = P_ref + np.random.rand(n_asks) * spread_range - np.random.normal(0,vol,size=n_asks)
        # quantity of stock per bid and ask
        ask_qty = np.random.randint(1,100, size=n_asks)
        # Make list of tuples
        asks = list(zip(ask_prices,ask_qty))
        # sort asks in ascending order
        asks.sort(key = lambda x:x[0])
        market_ask = asks[0][0]
    else:
        asks = []
        market_ask = P_ref

    mid_price = (market_bid+market_ask)/2

    return bids, asks, market_bid, market_ask, mid_price
